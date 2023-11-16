from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import Jobs,UsersProfile,Applications
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

def python(request):
    return render(request, 'courses/python.html')


#admin
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

def profile(request):
    current_user=request.user
    profile=UsersProfile.objects.get(profile_user=current_user)
    return render(request,'profile.html',{'profile':profile})

def users_list(request):
    candidates=UsersProfile.objects.all()
    return render(request,'admin/usersList.html',{'candidates':candidates})

def user_logout(request):
    logout(request)
    return redirect('index')

def jobs_available(request):
    jobs=Jobs.objects.all()
    current_user=request.user
    applied_jobs=Applications.objects.filter(candidate=current_user)
    print(len(applied_jobs))
    return render(request,'jobs.html',{'jobs':jobs,'applied_jobs':applied_jobs})

def apply_job(request,i):
    job=Jobs.objects.get(id=i)
    candidate=request.user
    new_applications=Applications(candidate=candidate,job=job)
    new_applications.save()
    print('successfully applied for the job')
    return redirect('jobsavailable')
    
def user_profile(request,i):
    p=UsersProfile.objects.get(id=i)
    jobs=Jobs.objects.filter(candidate=p.profile_user)
    return render(request,'user_profile.html',{'jobs':jobs})