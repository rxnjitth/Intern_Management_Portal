from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import *
from .forms import TaskReportForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import date
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
import pandas as pd
from django.http import HttpResponse



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
        return redirect('login')

    today = date.today()
    already_submitted = TaskReport.objects.filter(intern=request.user, date=today).exists()

    if request.method == 'POST':
        if already_submitted:
            messages.warning(request, "⚠️ You’ve already submitted today’s task.")
            return redirect('intern_dashboard')

        form = TaskReportForm(request.POST)
        if form.is_valid():
            task_report = form.save(commit=False)
            task_report.intern = request.user
            task_report.date = today
            task_report.save()
            messages.success(request, "✅ Daily task report submitted successfully.")
            return redirect('intern_dashboard')
    else:
        form = TaskReportForm()

    task_reports = TaskReport.objects.filter(intern=request.user).order_by('-date')
    submission_count = task_reports.count()

    # Initialize values
    intern_app = None
    duration_str = "0 months"

    try:
        intern_app = InternApplication.objects.get(clg_mailid=request.user.email)
        if intern_app.course_duration:
            duration_str = intern_app.course_duration.duration
    except InternApplication.DoesNotExist:
        pass

    # DEBUG LOGS
    print("📌 Duration String from DB:", duration_str)

    # Calculate total days
    total_days = duration_to_days(duration_str)
    print("📌 Total Days Calculated:", total_days)

    # Progress
    progress = round((submission_count / total_days) * 100, 2) if total_days else 0

    # Certificate status
    is_certified = intern_app.is_certified if intern_app else False

    return render(request, 'intern_dashboard.html', {
        'form': form,
        'task_reports': task_reports,
        'progress': progress,
        'submission_count': submission_count,
        'total_days': total_days,
        'intern_app': intern_app,
        'is_certified': is_certified,
    })


# ✅ ADMIN DASHBOARD
@login_required
def admin_dashboard(request):
    if get_user_role(request.user) != 'ADMIN':
        return redirect('login')  # Unauthorized access check

    total_interns = UserRole.objects.filter(role='INTERN').count()
    pending_applications = InternApplication.objects.filter(is_approved=False, is_rejected=False).count()
    
    # ✅ Only those who completed + certified
    certified_interns = InternApplication.objects.filter(is_completed=True, is_certified=True).count()

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
import re

def duration_to_days(duration_str):
    duration_str = duration_str.lower().strip()

    # Only a number? Treat as days
    if duration_str.isdigit():
        return int(duration_str)

    # Match "2 months", "3 weeks", "10 days"
    match = re.match(r'(\d+)\s*(day|days|week|weeks|month|months)', duration_str)
    if match:
        value, unit = match.groups()
        value = int(value)
        if 'month' in unit:
            return value * 30
        elif 'week' in unit:
            return value * 7
        elif 'day' in unit:
            return value

    # Default fallback
    return 0



@login_required
def all_interns_view(request):
    if get_user_role(request.user) != 'ADMIN':
        return redirect('login')

    intern_roles = UserRole.objects.filter(role='INTERN').select_related('user')
    
    intern_data = []
    for role in intern_roles:
        user = role.user
        try:
            application = InternApplication.objects.get(clg_mailid=user.email)
            name = application.name
        except InternApplication.DoesNotExist:
            name = user.username  # fallback
        
        intern_data.append({
            'id': user.id,
            'name': name,
            'email': user.email,
        })

    return render(request, 'all_interns.html', {
        'interns': intern_data
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

    user = get_object_or_404(User, id=user_id)
    try:
        application = InternApplication.objects.get(clg_mailid=user.email)
    except InternApplication.DoesNotExist:
        messages.error(request, "Intern application not found.")
        return redirect('all_interns')

    if action == 'approve':
        application.is_certified = True
        application.save()

        # ✅ Send Certification Approved Email
        send_mail(
            subject='🎓 IPS Internship Certificate Approved',
            message=f"""
Hi {application.name},

Congratulations! 🎉

You have successfully completed your internship course with the IPS Tech Community. Your performance and dedication have been reviewed and your certification has now been approved.

You are now eligible to download your internship certificate from the portal.

Regards,  
IPS Tech Community
""",
            from_email=None,
            recipient_list=[application.clg_mailid],
            fail_silently=False
        )

        messages.success(request, f"{application.name} has been certified successfully!")
    elif action == 'reject':
        application.is_certified = False
        application.save()
        messages.warning(request, f"{application.name}'s certification was rejected.")
    else:
        messages.error(request, "Invalid action.")

    return redirect('all_interns')



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

    if application.is_approved:
        messages.info(request, "This intern is already approved.")
        return redirect('internship_applications')

    # ✅ Mark as approved
    application.is_approved = True
    application.save()

    # ✅ Ensure user exists
    user, created = User.objects.get_or_create(
        username=application.roll_no,
        defaults={'email': application.clg_mailid}
    )

    if created:
        user.set_password('intern@2025')  # Default password
        user.save()

    # ✅ Assign INTERN role
    UserRole.objects.get_or_create(user=user, role='INTERN')

    # ✅ Send Approval Email with login info
    send_mail(
        subject="🎉 Internship Application Approved - IPS Tech Community",
        message=f"""
Hi {application.name},

Great news! 🎉

Your internship application to the IPS Tech Community has been **approved**.

You are now officially part of our intern program. Please log in using the credentials provided below and start your internship journey with us.

🔐 Login Credentials:
Username: {application.roll_no}
Password: intern@2025

We're thrilled to have you on board and look forward to your amazing contributions!

If you have any questions, feel free to reach out to our team.

Warm regards,  
IPS Tech Community Team
""",
        from_email='mranjith506@gmail.com',  # 🔁 Replace with your admin email
        recipient_list=[application.clg_mailid],
        fail_silently=False
    )

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

        # ❌ Send Rejection Email
        send_mail(
            subject="❌ Internship Application Rejected - IPS Tech Community",
            message=f"""
Hi {application.name},

Thank you for your interest in joining the IPS Tech Community internship program.

After reviewing your application, we regret to inform you that your application has not been approved at this time.

This decision does not reflect your potential, and we encourage you to apply again in the future with more details or after gaining additional experience.

We wish you the very best in your career journey.

Sincerely,  
IPS Tech Community Team
""",
            from_email='mranjith2506@gmail.com',  # 🔁 Replace with your admin email
            recipient_list=[application.clg_mailid],
            fail_silently=False
        )

        messages.warning(request, f"{application.name}'s application was rejected.")

    return redirect('internship_applications')



def download_certificate(request, user_id):
    user = get_object_or_404(User, id=user_id)
    app = get_object_or_404(InternApplication, clg_mailid=user.email)

    if not app.is_certified:
        messages.error(request, "Certificate not approved yet.")
        return redirect('intern_detail', user_id=user_id)

    return render(request, 'certificate.html', {'user': user, 'application': app})


@login_required
def certified_interns_list(request):
    interns = InternApplication.objects.filter(is_certified=True)
    return render(request, 'certified_interns.html', {'interns': interns})

@login_required
def certified_interns_view(request):
    if get_user_role(request.user) != 'ADMIN':
        return redirect('login')

    certified_interns = InternApplication.objects.filter(is_completed=True, is_certified=True)

    return render(request, 'certified_interns.html', {
        'certified_interns': certified_interns
    })





@login_required
def export_interns_excel(request):
    if get_user_role(request.user) != 'ADMIN':
        return redirect('login')

    # Collect intern data
    interns = InternApplication.objects.all().values(
        'name', 'roll_no', 'department', 'clg_mailid', 'cgpa', 'arrears',
        'course_duration__duration', 'is_approved', 'is_rejected', 'is_certified'
    )

    # Convert to DataFrame
    df = pd.DataFrame(interns)
    df.rename(columns={
        'name': 'Name',
        'roll_no': 'Roll Number',
        'department': 'Department',
        'clg_mailid': 'Email',
        'cgpa': 'CGPA',
        'arrears': 'Arrears',
        'course_duration__duration': 'Course Duration',
        'is_approved': 'Approved',
        'is_rejected': 'Rejected',
        'is_certified': 'Certified'
    }, inplace=True)

    # Convert booleans to Yes/No
    df['Approved'] = df['Approved'].apply(lambda x: 'Yes' if x else 'No')
    df['Rejected'] = df['Rejected'].apply(lambda x: 'Yes' if x else 'No')
    df['Certified'] = df['Certified'].apply(lambda x: 'Yes' if x else 'No')

    # Create HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=interns_data.xlsx'

    # Write DataFrame to Excel
    df.to_excel(response, index=False)

    return response








@login_required
def download_task_reports_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="task_reports.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    reports = TaskReport.objects.filter(intern=request.user).order_by('date')

    y = 800
    p.drawString(100, y, f"Task Reports for {request.user.username}")
    y -= 30

    for report in reports:
        line = f"{report.date} - {report.topic}"
        p.drawString(100, y, line)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response