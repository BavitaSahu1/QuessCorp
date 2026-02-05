from django.shortcuts import render, redirect
from django.http import HttpResponse
from hrm import db_connector
from django.db import connection
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import pytz
from greenrider import db_connector

## Fetching Current Date Time in UTC Format --
ist_timezone = pytz.timezone('Asia/Kolkata')
current_datetime_ist = datetime.now(ist_timezone)
current_datetime = current_datetime_ist.strftime("%Y-%m-%d %H:%M:%S")


def base_admin(request):
    return render(request, "base_admin.html")

def base_dashboard(request):
     return render(request,"base_dashboard.html")

def add_emp(request):
    return render(request, "add_emp.html")

@csrf_exempt
def saveEmployeeData(request):
    if request.method=='POST':
            First_Name = request.POST.get('f_name')
            Last_name = request.POST.get('l_name')
            Employee_ID = request.POST.get('emp_id')
            Department = request.POST.get('department')
            Email = request.POST.get('email')
            Fullname = (First_Name+' '+Last_name)

            con = db_connector.create_connection()
            if connection:
                my_cur=con.cursor()

                check_email = "SELECT emp_id,email_address from employee WHERE (email_address = '{}' or emp_id = {}) and deleted_at Is Null;".format(Email, Employee_ID)
                my_cur.execute(check_email)
                existing_Email = my_cur.fetchone()

                if existing_Email:
                    messages.error(request,"Employee ID or Email already exist")
                else:
                    insert_query = "insert into employee(full_name,emp_id,department,email_address,created_at) values('{}',{},'{}','{}','{}');".format(Fullname,Employee_ID,Department,Email,current_datetime) 
                                     
                    my_cur.execute(insert_query)
                    con.commit()

                    messages.success(request,"Data Saved Successfully...")
                my_cur.close()
                con.close()    
    return redirect('add_emp')


# dictfetchall for show data to all Pages --------------------------
@csrf_exempt
def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc ], row))
        for row in cursor.fetchall()
    ]


@csrf_exempt
def view_emp(request):
        cursor = connection.cursor()
        global a
        if request.method == 'POST':
            user_input1 = request.POST.get('a_name')
            user_input2 = request.POST.get('a_email')
            if user_input1 and user_input2:
                query1 = f"Select full_name, email_address, emp_id, department from employee where full_name = '{user_input1}' and email_address='{user_input2}' and deleted_at is Null;"
            else:
                query1 = f"Select full_name, email_address, emp_id, department from employee where full_name = '{user_input1}' or email_address='{user_input2}' and deleted_at is Null;"
            cursor.execute(query1)
            a=dictfetchall(cursor)
        else:  
            query2 = "Select full_name, email_address, emp_id, department from employee where deleted_at is Null;"
            cursor.execute(query2)
            a = dictfetchall(cursor)
        return render(request,"view_emp.html", {'data':a})


@csrf_exempt
def DeleteEmp(request):
        if request.method == 'POST':
            DeleteButton = request.POST.get('DeleteBtn')
            con = db_connector.create_connection()
            if connection:
                my_cur=con.cursor()
                # 
                my_cur.execute(f"SELECT full_name FROM employee WHERE emp_id='{DeleteButton}' and deleted_at Is Null;")
                emp_name = my_cur.fetchone()
                #
                query = "update employee set deleted_at = '{}' where emp_id = {} and deleted_at is Null;".format(current_datetime, DeleteButton) 
                query2 = "update attendance set deleted_at = '{}' where emp_id = {} and deleted_at is Null;".format(current_datetime, DeleteButton) 
                my_cur.execute(query)
                my_cur.execute(query2)
                con.commit()
                messages.success(request, f"{emp_name[0]}'s Employee Record Deleted. ")
        return redirect('view_emp')


@csrf_exempt
def view_attendance(request):
        cursor = connection.cursor()
        global a,b
        if request.method == 'POST':
           

            user_input = request.POST.get('att_date')
            if user_input:
                query1  = f"""SELECT 
                        emp.full_name,
                        emp.emp_id,
                        COALESCE(att.attendance_date, '') AS attendance_date,
                        COALESCE(att.check_in, '') AS in_time,
                        COALESCE(att.check_out, '') AS out_time,
                        COALESCE(att.attendance_status, '') AS emp_status
                        FROM employee AS emp
                        LEFT JOIN attendance AS att
                        ON emp.emp_id = att.emp_id
                        where att.attendance_date = '{user_input}'
                        and emp.deleted_at is Null
                        and att.deleted_at is Null;
                       """
            cursor.execute(query1)
            a=dictfetchall(cursor)
        else:  
            query2  = """SELECT 
                        emp.full_name,
                        emp.emp_id,
                        COALESCE(att.attendance_date, '') AS attendance_date,
                        COALESCE(att.check_in, '') AS in_time,
                        COALESCE(att.check_out, '') AS out_time,
                        COALESCE(att.attendance_status, '') AS emp_status
                        FROM employee AS emp
                        LEFT JOIN attendance AS att
                        ON emp.emp_id = att.emp_id
                        where emp.deleted_at is Null
                        and att.deleted_at is Null
                        ORDER BY att.attendance_date IS NULL, att.attendance_date DESC;
                       """
            cursor.execute(query2)
            a = dictfetchall(cursor)

        query_for_model = """SELECT DISTINCT emp_id, full_name FROM employee WHERE deleted_at IS NULL;"""
        cursor.execute(query_for_model)
        b = dictfetchall(cursor)
        return render(request,"view_attendance.html", {'data':a, 'model_data':b})




@csrf_exempt
def dashboard(request):
    cursor = connection.cursor()
    global a,b,c,d 
    query1 = "select count(*) AS employee_id from employee where deleted_at is Null;"
    query2 = "select count(*) AS present_employee from attendance where attendance_status = 'Present' and attendance_date = CURDATE() and deleted_at is Null;"
    query3 = "select count(*) AS absent_employee from attendance where attendance_status = 'Absent' and attendance_date = CURDATE() and deleted_at is Null;"
    query4 = """SELECT emp.full_name,
       emp.department,
       att.attendance_status,
       att.attendance_date,
       att.check_in
FROM employee emp
RIGHT JOIN attendance att
  ON att.emp_id = emp.emp_id
where emp.deleted_at is Null
and att.deleted_at is Null
ORDER BY 
  CAST(att.attendance_date AS DATE) DESC,
  CAST(att.check_in AS TIME) DESC
  limit 5;
"""
    cursor.execute(query1)
    a = dictfetchall(cursor)
    cursor.execute(query2)
    b = dictfetchall(cursor)
    cursor.execute(query3)
    c = dictfetchall(cursor)
    cursor.execute(query4)
    d = dictfetchall(cursor)
    print(f"count of employee = {a}")
    print(f"count of employee = {b}")
    print(f"count of employee = {c}")
    return render(request,"dashboard.html", {'data1':a, 'data2':b, 'data3':c, 'data4':d})


@csrf_exempt
def MarkAttendance(request):
    global a 
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        date = request.POST.get("attendance_date")
        in_time = request.POST.get("in_time")
        out_time = request.POST.get("out_time")
        status = request.POST.get("emp_status") 

        cursor = connection.cursor()
        query1 = "SELECT emp_id, full_name FROM employee WHERE deleted_at is Null;"
        cursor.execute(query1)

        query2 = f"select emp_id, attendance_date from attendance where emp_id = {emp_id} and attendance_date = '{date}' and deleted_at is Null;"
        cursor.execute(query2)
        check_attendance = dictfetchall(cursor)
        if check_attendance:
            messages.error(request,f"Attendance already exists for Employee ID '{check_attendance[0]['emp_id']}' "
            f"on the selected date {check_attendance[0]['attendance_date']}. "
            f"Duplicate entry is not allowed.")
        else:
            query3 = "insert into attendance(emp_id,attendance_date,attendance_status,check_in,check_out,created_at) values({},'{}','{}','{}','{}','{}')".format(emp_id,date,status,in_time,out_time,current_datetime)
            cursor.execute(query3)
            connection.commit()
            messages.success(request, f"Attendance marked successfully...")

    return redirect("view_attendance")


@csrf_exempt
def EditAttStatus(request):
        global a,b
        if request.method == 'POST':
            emp_id = request.POST.get('editBtn')
            att_date = request.POST.get('editBtn2')
            cursor = connection.cursor()
            # cmd = "SELECT * FROM employee WHERE emp_id = {} and deleted_at is Null;".format(emp_id)
            cmd2 = "SELECT * FROM attendance WHERE emp_id = {} and attendance_date = '{}' and deleted_at is Null;".format(emp_id,att_date)
            # cursor.execute(cmd)
            # a = dictfetchall(cursor)
            cursor.execute(cmd2)
            b = dictfetchall(cursor)
        return render(request,"EditAttStatus.html", {'data2':b})


@csrf_exempt
def UpdateAttendance(request):
    if request.method == 'POST': 
        EmpID = request.POST.get('emp_id')         
        AttendanceDate = request.POST.get('attendance_date')
        InTime = request.POST.get('in_time')
        OutTime = request.POST.get('out_time')
        AttendanceStatus = request.POST.get('attendance_status')


        cursor = connection.cursor()
        cursor.execute(f"SELECT full_name FROM employee WHERE emp_id = {EmpID} and deleted_at is Null;")
        emp_name = cursor.fetchone()

        query = f"select emp_id, attendance_date from attendance where emp_id = {EmpID} and attendance_date = '{AttendanceDate}' and deleted_at is Null;"
        cursor.execute(query)
        check_attendance = dictfetchall(cursor)
        if check_attendance:
            messages.error(request,f"Attendance already exists for Employee ID {check_attendance[0]['emp_id']} "
        f"on the selected date {check_attendance[0]['attendance_date']}. "
        f"Duplicate entry is not allowed.")
        else:

            cmd = "insert into attendance(emp_id, attendance_date, check_in, check_out, attendance_status) values({},'{}','{}','{}','{}')".format(EmpID, AttendanceDate, InTime, OutTime, AttendanceStatus) 
            cursor.execute(cmd)
            connection.commit()
            messages.success(request, f"Attendance Details Updated for {emp_name[0]}")
    return redirect('view_attendance')

