from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import UserRole, InternApplication, CourseDuration
from .forms import TaskReportForm
from .models import TaskReport
from django.contrib.auth.decorators import login_required

def custom_login(request):
    form = AuthenticationForm()
    courses = CourseDuration.objects.all()  # ✅ Send course list to template

    if request.method == 'POST':
        if 'username' in request.POST:  # ✅ Login form submitted
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    try:
                        user_role = UserRole.objects.get(user=user).role
                    except UserRole.DoesNotExist:
                        messages.error(request, "User role not found.")
                        return redirect('login')
                    login(request, user)
                    if user_role == 'ADMIN':
                        return redirect('admin_dashboard')
                    elif user_role == 'INTERN':
                        return redirect('intern_dashboard')
                    else:
                        messages.error(request, "Invalid role.")
                        return redirect('login')
                else:
                    form.add_error(None, "Invalid credentials")
            else:
                messages.error(request, "Login failed. Please check credentials.")

        elif 'name' in request.POST:  # ✅ Intern application form submitted
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
                messages.error(request, f"Error submitting form: {str(e)}")

    return render(request, 'login.html', {'form': form, 'courses': courses})



@login_required
def intern_dashboard(request):
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

    # Task submissions by intern
    task_reports = TaskReport.objects.filter(intern=request.user).order_by('-date')
    submission_count = task_reports.count()

    # Get course duration for this intern
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


    
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def duration_to_days(duration_str):
    """Convert duration like '3 months' to total days (assuming 30 days/month)."""
    try:
        months = int(duration_str.split()[0])
        return months * 30  # Approximate each month as 30 days
    except (ValueError, IndexError):
        return 0

def custom_logout(request):
    logout(request)
    return redirect('login')
    