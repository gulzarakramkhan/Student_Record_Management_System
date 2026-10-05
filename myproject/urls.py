"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.template.backends import django
from django.urls import path
from student.views import home
from student.views import *
from django.conf import settings
from django.conf.urls.static import static
from student.views import home,about,login,navbar,adminhome,add_stu,show_stu,edit_student,delete_student,admin_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('about/',about,name='about'),
    path('login/',login,name='login'),
    path('navbar/',navbar,name='navbar'),
    path('adminhome/',adminhome,name='adminhome'),
    path('addstudent',add_stu,name='addstudent'),
    path('view_stu',show_stu,name='view_stu'),
    path('edit_stu/<int:id>',edit_student,name='edit_student'),
    path('delete_stu/<int:id>',delete_student,name='delete_student'),
    path('search_stu',search_stu,name='search_stu'),
    path('logout/', admin_logout,name="admin_logout"),
    path('change_path',admin_change_password,name='change_pass'),
    path('student_home',stu_home,name='student_home'),
    path('show_profile',show_profile,name='show_profile'),
    

]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
