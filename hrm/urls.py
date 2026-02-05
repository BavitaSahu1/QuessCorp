from django.contrib import admin
from django.urls import path
from hrm import views

urlpatterns = [
    path('base_admin',views.base_admin,name="base_admin"),
    path('base_dashboard',views.base_dashboard,name="base_dashboard"),
    path('',views.dashboard,name="dashboard"),
    path('add_emp',views.add_emp,name="add_emp"),
    path('saveEmployeeData',views.saveEmployeeData,name="saveEmployeeData"),
    path('view_emp',views.view_emp,name="view_emp"),
    path('DeleteEmp',views.DeleteEmp,name="DeleteEmp"),
    path('view_attendance',views.view_attendance,name="view_attendance"),
    path('EditAttStatus',views.EditAttStatus,name="EditAttStatus"),
    path('UpdateAttendance',views.UpdateAttendance,name="UpdateAttendance"),  
    path('MarkAttendance',views.MarkAttendance,name="MarkAttendance"),  
]
