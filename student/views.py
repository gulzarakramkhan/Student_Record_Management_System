from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout 
from django.http import HttpResponse
from .models import student
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")

def navbar(request):
    return render(request,"navbar.htm")

def login(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("uname", "")
        password = request.POST.get("password", "")

        # First check Django Admin/Staff login
        user = auth.authenticate(
            username=username,
            password=password
        )

        if user is not None and user.is_staff:
            auth.login(request, user)
            return redirect('adminhome')

        # Now check Student login
        try:
            stu = student.objects.get(
                username=username,
                password=password
            )

            request.session['student_id'] = stu.id
            return redirect('student_home')

        except student.DoesNotExist:
            error = "yes"

    return render(request, "login.html", {"error": error})

@login_required(login_url='login')
def adminhome(request):
    return render(request,"admin_home.html")

@login_required(login_url='login')
def add_stu(request):
    error = ""
    if request.method == "POST":
        n = request.POST.get('sname', '')
        e = request.POST.get('email', '')
        u = request.POST.get('uname', '')
        p = request.POST.get('password', '')
        cl = request.POST.get('college', '')
        city = request.POST.get('city', '')
        jd = request.POST.get('jdate', '')
        tf = request.POST.get('tfee', '')
        pf = request.POST.get('pfee', '')
        lf = request.POST.get('lfee', '')
        ph = request.POST.get('phone', '')
        tech = request.POST.get('technology', '')
        img = request.FILES.get('img')
        try:
            student.objects.create(
                name=n,
                email=e,
                username=u,
                password=p,
                college=cl,
                city_name=city,
                Joining_Date=jd,
                Total_fee=tf,
                Paid_fee=pf,
                left_fee=lf,
                phone=ph,
                Technology=tech,
                image=img,
            )
            error = "no"
        except Exception as e:
            print(e)
            return HttpResponse(str(e))
    return render(request, "add_student.html", {'error': error})

@login_required(login_url='login')
def show_stu(request):
    data=student.objects.all()
    d={'data':data}
    return render(request,"view_stu.html",d)

def search_stu(request):
    data=student.objects.all()
    return render(request,"search.html",{"data":data})

@login_required(login_url='login')
def edit_student(request,id):
    obj=student.objects.get(id=id)
    if request.method=="POST":
       obj.name=request.POST.get('name')
       obj.email=request.POST.get('email')
       obj.college=request.POST.get('college')
       obj.city_name=request.POST.get('city') or request.POST.get('city_name')
       obj.Joining_Date=request.POST.get('Joining_Date') or request.POST.get('jdate')
       obj.Total_fee=request.POST.get('Total_fee') or request.POST.get('tfee')
       obj.Paid_fee=request.POST.get('Paid_fee') or request.POST.get('pfee')
       obj.left_fee=request.POST.get('left_fee') or request.POST.get('lfee')
       obj.phone=request.POST.get('phone')
       obj.Technology=request.POST.get('technology') or request.POST.get('Technology')
       if request.FILES.get('image'):
           obj.image=request.FILES.get('image')
       obj.save()
       return redirect('view_stu')
    return render(request,"edit_student.html",{'obj':obj})

@login_required(login_url='login')
def delete_student(request,id):
    obj=student.objects.get(id=id)
    obj.delete()
    return redirect('view_stu')
    return render(request,"delete_student.html")
def search_stu(request):
    name = request.GET.get('name')

    if name:
        data = student.objects.filter(name__icontains=name)
    else:
        data = student.objects.all()

    return render(request, "search.html", {"data": data})

def stu_home(request):
    if 'student_id' not in request.session:
        return redirect('login')
    sid=request.session['student_id']
    stu=student.objects.get(id=sid)
    return render(request,"student_home.html",{'stu':stu})


@login_required(login_url='login')
def admin_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def admin_change_password(request):

    if request.method == "POST":

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        if not user.check_password(old_password):
            return render(request, "admin_change_password.html", {
                "error": "Old password is incorrect."
            })

        if new_password != confirm_password:
            return render(request, "admin_change_password.html", {
                "error": "New passwords do not match."
            })

        if len(new_password) < 6:
            return render(request, "admin_change_password.html", {
                "error": "Password must be at least 6 characters."
            })

        user.set_password(new_password)
        user.save()

        # User ko logout hone se bachata hai
        update_session_auth_hash(request, user)

        messages.success(request, "Password changed successfully!")

        return render(request, "admin_change_password.html")

    return render(request, "admin_change_password.html")

def show_profile(request):
       if 'student_id' not in request.session:
             return redirect('login')
       sid=request.session['student_id'] 
       stu=student.objects.get(id=sid)
       if request.method == "POST":
              stu.name=request.POST['name']
              stu.email=request.POST['email']
              stu.phone=request.POST['phone']
              stu.city=request.POST['city']
              stu.image=request.FILES['image']
              stu.save()
       return render(request,'show_profile.html',{'stu':stu})