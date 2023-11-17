from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import Jobs,UsersProfile,Applications
import vonage
from django.contrib.auth.decorators import login_required

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.conf import settings

import os

# Create your views here.
def index(request):
    print(request.user.username)
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')

def courses(request):
    return render(request, 'courses.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def sign_up(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        new_user=User.objects.create_user(username=username,email=email,password=password)
        new_user.save()
        return redirect('login')
    else:
        return render(request, 'auth/sign_up.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render(request, 'auth/login.html')

    else:
        return render(request, 'auth/login.html')

def python(request):
    return render(request, 'courses/python.html')


#admin
@login_required(login_url='adminlogin')
def admin_index(request):
    return render(request,'admin/admin_index.html')


def admin_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if (user is not None) and user.is_staff:
            login(request,user)
            return redirect('adminindex')
        else:
            return render(request,'admin/login.html')
    else:
        return render(request,'admin/login.html')
    
@login_required(login_url='adminlogin')
def jobs(request):
    jobs=Jobs.objects.all()
    if request.method=='POST':
        job_title=request.POST['job_title']
        company_name=request.POST['company_name']
        location=request.POST['location']
        mode=request.POST['mode']
        description=request.POST['description']
        experience_required=request.POST['experience_required']
        skills_required=request.POST['skills_required']
        starting_salary=request.POST['starting_salary']
        ending_salary=request.POST['ending_salary']
        languages=request.POST['languages']
        # resume=request.FILES.get('resume')
        new_job=Jobs(job_title=job_title,
                     company_name=company_name,
                     location=location,
                     mode=mode,
                     description=description,
                     experience_required=experience_required,
                     skills_required=skills_required,
                     starting_salary=starting_salary,
                     ending_salary=ending_salary,
                     languages=languages,
                     )
        new_job.save()
        return render(request,'admin/job_post.html',{'jobs':jobs})
    else:
        return render(request,'admin/job_post.html',{'jobs':jobs})

 
def edit_profile(request):
        current_user=request.user
        if request.method=='POST':
            fullname=request.POST['name']
            photo=request.FILES.get('photo')
            phone1=request.POST['phone1']
            phone2=request.POST['phone2']
            email=request.POST['email']
            current_address=request.POST['current_address']
            permanant_address=request.POST['permanant_address']
            education=request.POST['education']
            skills=request.POST['skills']
            # Experience=request.POST['experience']
            certifications=request.POST['certifications']
            resume=request.FILES.get('resume')
            user_profile=UsersProfile(fullname=fullname,
                                    profile_user=current_user,
                                    photo=photo,
                                    email=email,
                                    phone1=phone1,
                                    phone2=phone2,
                                    current_address=current_address,
                                    permanant_address=permanant_address,
                                    Education=education,
                                    skills=skills,
                                    certifications=certifications,
                                    resume=resume,
                                    )
            user_profile.save()
            # return render(request,'editProfile.html')
            return redirect('profile')
        else:
            return render(request,'editProfile.html')
        
@login_required(login_url='login')
def profile(request):
    current_user=request.user
    try:
        profile=UsersProfile.objects.get(profile_user=current_user)
    except:
        profile=None
    # print(profile.resume.url)
    # print('helloooo')
    return render(request,'profile.html',{'profile':profile})

@login_required(login_url='adminlogin')
def users_list(request):
    candidates=UsersProfile.objects.all()
    return render(request,'admin/usersList.html',{'candidates':candidates})

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def jobs_available(request):
    jobs=Jobs.objects.all()
    current_user=request.user
    applied_jobs=Applications.objects.filter(candidate=current_user)
    print(len(applied_jobs))
    return render(request,'jobs.html',{'jobs':jobs,'applied_jobs':applied_jobs})

@login_required(login_url='/custom-login/')
def apply_job(request,i):
    job=Jobs.objects.get(id=i)
    candidate=request.user
    new_applications=Applications(candidate=candidate,job=job)
    new_applications.save()
    print('successfully applied for the job')
    return redirect('jobsavailable')
    
@login_required(login_url='adminlogin')
def user_profile(request,i):
    p=UsersProfile.objects.get(id=i)
    u=p.profile_user
    jobs=Applications.objects.filter(candidate=u)
    return render(request,'user_profile.html',{'jobs':jobs})


def verify1(request):
    current_user=request.user
    global profile
    profile=UsersProfile.objects.get(profile_user=current_user)
    phone=profile.phone1
    global client
    global verify
    client = vonage.Client(key="479aaf01", secret="V3w3NMQNjnZqDKYS")
    verify = vonage.Verify(client)

    response = verify.start_verification(number=phone, brand="AcmeInc")
    global REQUEST_ID
    REQUEST_ID=response['request_id']

    if response["status"] == "0":
        print("Started verification request_id is %s" % (response["request_id"]))
        return render(request,'verify.html')
    else:
        print("Error: %s" % response["error_text"])
        return redirect('profile')
    


def verify2(request):
    CODE=request.POST['code']

    response = verify.check(REQUEST_ID, code=CODE)

    if response["status"] == "0":
        profile.phone1_verified=True
        profile.save()
        print("Verification successful, event_id is %s" % (response["event_id"]))
        return redirect('profile')
    else:
        print("Error: %s" % response["error_text"])
        msg='invalid otp'
        return render(request,'verify.html',{'msg':msg})
    
# views.py




