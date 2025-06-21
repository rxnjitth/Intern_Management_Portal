from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import *
from .forms import TaskReportForm
from django.contrib.auth.decorators import login_required


# 🔧 Helper Function
def get_user_role(user):
    try:
        return UserRole.objects.get(user=user).role
    except UserRole.DoesNotExist:
        return None


# ✅ LOGIN + INTERN APPLY VIEW
def custom_login(request):
    form = AuthenticationForm()
    courses = CourseDuration.objects.all()

    if request.method == 'POST':
        if 'username' in request.POST:  # Login form
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user:
                    role = get_user_role(user)
                    if not role:
                        messages.error(request, "User role not found.")
                        return redirect('login')
                    login(request, user)
                    return redirect('admin_dashboard' if role == 'ADMIN' else 'intern_dashboard')
                else:
                    form.add_error(None, "Invalid credentials")
            else:
                messages.error(request, "Login failed. Please check credentials.")

        elif 'name' in request.POST:  # Intern Application form
            try:
                course_id = request.POST.get('course_duration')
                course_duration = CourseDuration.objects.get(id=course_id)
                InternApplication.objects.create(
                    name=request.POST.get('name'),
                    roll_no=request.POST.get('roll_no'),
                    department=request.POST.get('department'),
                    cgpa=request.POST.get('cgpa'),
                    arrears=request.POST.get('arrears'),
                    gender=request.POST.get('gender'),
                    clg_mailid=request.POST.get('clg_mailid'),
                    course_duration=course_duration
                )
                messages.success(request, "Intern application submitted successfully.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Error submitting form: {e}")

    return render(request, 'login.html', {'form': form, 'courses': courses})


# ✅ INTERN DASHBOARD
@login_required
def intern_dashboard(request):
    if get_user_role(request.user) != 'INTERN':
        return redirect('login')  # Unauthorized access check

    if request.method == 'POST':
        form = TaskReportForm(request.POST)
        if form.is_valid():
            task_report = form.save(commit=False)
            task_report.intern = request.user
            task_report.save()
            messages.success(request, "Daily task report submitted successfully.")
            return redirect('intern_dashboard')
    else:
        form = TaskReportForm()

    task_reports = TaskReport.objects.filter(intern=request.user).order_by('-date')
    submission_count = task_reports.count()

    try:
        intern_app = InternApplication.objects.get(clg_mailid=request.user.email)
        duration_str = intern_app.course_duration.duration if intern_app.course_duration else "0 months"
    except InternApplication.DoesNotExist:
        duration_str = "0 months"

    total_days = duration_to_days(duration_str)
    progress = round((submission_count / total_days) * 100, 2) if total_days else 0

    return render(request, 'intern_dashboard.html', {
        'form': form,
        'task_reports': task_reports,
        'progress': progress,
    })


# ✅ ADMIN DASHBOARD
@login_required
def admin_dashboard(request):
    if get_user_role(request.user) != 'ADMIN':
        return redirect('login')  # Unauthorized access check

    total_interns = UserRole.objects.filter(role='INTERN').count()
    pending_applications = InternApplication.objects.filter(is_approved=False, is_rejected=False).count()

    certified_interns = InternApplication.objects.filter(is_approved=True).count()

    return render(request, 'admin_dashboard.html', {
        'total_interns': total_interns,
        'pending_applications': pending_applications,
        'certified_interns': certified_interns,
    })


# ✅ LOGOUT
def custom_logout(request):
    logout(request)
    return redirect('login')


# ✅ HELPER: Convert "3 months" to 90 days
def duration_to_days(duration_str):
    try:
        months = int(duration_str.split()[0])
        return months * 30
    except (ValueError, IndexError):
        return 0

from django.contrib.auth.models import User

@login_required
def all_interns_view(request):
    if get_user_role(request.user) != 'ADMIN':
        return redirect('login')

    intern_roles = UserRole.objects.filter(role='INTERN').select_related('user')
    interns = [role.user for role in intern_roles]

    return render(request, 'all_interns.html', {
        'interns': interns
    })

@login_required
def intern_detail_view(request, user_id):
    if get_user_role(request.user) != 'ADMIN':
        return redirect('login')

    intern_user = get_object_or_404(User, id=user_id)
    try:
        application = InternApplication.objects.get(clg_mailid=intern_user.email)
    except InternApplication.DoesNotExist:
        application = None

    task_reports = TaskReport.objects.filter(intern=intern_user).order_by('-date')
    submission_count = task_reports.count()
    total_days = duration_to_days(application.course_duration.duration) if application and application.course_duration else 0
    progress = round((submission_count / total_days) * 100, 2) if total_days else 0

    return render(request, 'intern_detail.html', {
        'intern': intern_user,
        'application': application,
        'task_reports': task_reports,
        'submission_count': submission_count,
        'total_days': total_days,
        'progress': progress,
    })



@login_required
def mark_certification(request, user_id, action):
    if get_user_role(request.user) != 'ADMIN':
        return redirect('login')

    intern_user = get_object_or_404(User, id=user_id)
    try:
        application = InternApplication.objects.get(clg_mailid=intern_user.email)
        if action == 'approve':
            application.is_approved = True
        elif action == 'reject':
            application.is_approved = False
        application.save()
        messages.success(request, f'Intern certification {"approved" if action == "approve" else "rejected"} successfully.')
    except InternApplication.DoesNotExist:
        messages.error(request, "Application not found.")
    
    return redirect('intern_detail', user_id=user_id)


def internship_applications(request):
    applications = InternApplication.objects.filter(is_approved=False, is_rejected=False)
    return render(request, 'internship_applications.html', {'applications': applications})

@login_required
def internship_applications_list(request):
    applications = InternApplication.objects.all().order_by('-id')
    return render(request, 'internship_applications.html', {
        'applications': applications
    })

def internship_applications_detail(request, id):
    app = get_object_or_404(InternApplication, id=id)
    return render(request, 'application_detail.html', {'app': app})


@login_required
def approve_application(request, app_id):
    application = get_object_or_404(InternApplication, id=app_id)

    # Check if already approved
    if application.is_approved:
        messages.info(request, "This intern is already approved.")
        return redirect('internship_applications')

    # Create user if not exists
    user, created = User.objects.get_or_create(
        username=application.roll_no,
        defaults={'email': application.clg_mailid}
    )

    if created:
        user.set_password('intern@2025')  # 🔐 Default password (changeable later)
        user.save()

    # Assign user role
    from .models import UserRole
    UserRole.objects.get_or_create(user=user, role='INTERN')

    # Mark approved
    application.is_approved = True
    application.save()

    messages.success(request, f"{application.name} is now approved as an intern!")
    return redirect('internship_applications')

@login_required
def reject_application(request, app_id):
    application = get_object_or_404(InternApplication, id=app_id)

    if application.is_approved:
        messages.error(request, "Already approved. Can't reject now.")
    else:
        application.is_rejected = True
        application.save()
        messages.warning(request, f"{application.name}'s application was rejected.")

    return redirect('internship_applications')
