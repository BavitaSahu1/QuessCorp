from django.shortcuts import render,redirect
from django.http import HttpResponse
from hrm import db_connector
from django.db import connection
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, "index.html")

def base_admin(request):
    return render(request, "base_admin.html")

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

                check_email = "SELECT emp_id,email_address from employee WHERE email_address = '{}' or emp_id = {}".format(Email, Employee_ID)
                my_cur.execute(check_email)
                existing_Email = my_cur.fetchone()

                if existing_Email:
                    messages.error(request,"Employee ID or Email already exist")
                else:
                    insert_query = "insert into employee(full_name,emp_id,department,email_address) values('{}','{}','{}','{}')".format(Fullname,Employee_ID,Department,Email) 
                                     
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
                query1 = f"Select full_name, email_address, emp_id, department from employee where full_name = '{user_input1}' and email_address='{user_input2}'"
            else:
                query1 = f"Select full_name, email_address, emp_id, department from employee where full_name = '{user_input1}' or email_address='{user_input2}'"
            cursor.execute(query1)
            a=dictfetchall(cursor)
        else:  
            query2 = "Select full_name, email_address, emp_id, department from employee"
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
                my_cur.execute(f"SELECT full_name FROM employee WHERE emp_id='{DeleteButton}'")
                emp_name = my_cur.fetchone()
                # 
                query = "Delete from employee where emp_id='{}'".format(DeleteButton)
                query2 = "Delete from attendance where emp_id='{}'".format(DeleteButton)
                my_cur.execute(query)
                my_cur.execute(query2)
                con.commit()
                messages.success(request, f"{emp_name[0]}'s Employee Record Deleted. ")
        return redirect('view_emp')


@csrf_exempt
def view_attendance(request):
        cursor = connection.cursor()
        global a
        if request.method == 'POST':
            user_input = request.POST.get('att_date')
            if user_input:
                query1  = f"""SELECT 
                        emp.full_name,
                        emp.emp_id,
                        COALESCE(att.attendance_date, '') AS attendance_date,
                        COALESCE(att.in_time, '') AS in_time,
                        COALESCE(att.out_time, '') AS out_time,
                        COALESCE(att.emp_status, '') AS emp_status
                        FROM employee AS emp
                        LEFT JOIN attendance AS att
                        ON emp.emp_id = att.emp_id
                        where att.attendance_date = '{user_input}';
                       """
            cursor.execute(query1)
            a=dictfetchall(cursor)
        else:  
            query2  = """SELECT 
                        emp.full_name,
                        emp.emp_id,
                        COALESCE(att.attendance_date, '') AS attendance_date,
                        COALESCE(att.in_time, '') AS in_time,
                        COALESCE(att.out_time, '') AS out_time,
                        COALESCE(att.emp_status, '') AS emp_status
                        FROM employee AS emp
                        LEFT JOIN attendance AS att
                        ON emp.emp_id = att.emp_id;
                       """
            cursor.execute(query2)
            a = dictfetchall(cursor)
        return render(request,"view_attendance.html", {'data':a})


@csrf_exempt
def EditAttStatus(request):
        global a,b
        if request.method == 'POST':
            emp_id = request.POST.get('editBtn')
            cursor = connection.cursor()
            cmd = "SELECT * FROM employee WHERE emp_id = {}".format(emp_id)
            cursor.execute(cmd)
            a = dictfetchall(cursor)
        return render(request,"EditAttStatus.html", {'data':a})



@csrf_exempt
def UpdateAttendance(request):
    if request.method == 'POST': 
        EmpID = request.POST.get('emp_id')         
        AttendanceDate = request.POST.get('attendance_date')
        InTime = request.POST.get('in_time')
        OutTime = request.POST.get('out_time')
        AttendanceStatus = request.POST.get('attendance_status')


        cursor = connection.cursor()
        cursor.execute(f"SELECT full_name FROM employee WHERE emp_id = {EmpID}")
        emp_name = cursor.fetchone()

        query = f"select emp_id, attendance_date from attendance where emp_id = {EmpID} and attendance_date = '{AttendanceDate}';"
        cursor.execute(query)
        check_attendance = dictfetchall(cursor)
        if check_attendance:
            messages.error(request,f"Attendance already exists for Employee ID {check_attendance[0]['emp_id']} "
        f"on the selected date {check_attendance[0]['attendance_date']}. "
        f"Duplicate entry is not allowed.")
        else:

            cmd = "insert into attendance(emp_id, attendance_date, in_time, out_time, emp_status) values({},'{}','{}','{}','{}')".format(EmpID, AttendanceDate, InTime, OutTime, AttendanceStatus) 
            cursor.execute(cmd)
            connection.commit()
            messages.success(request, f"Attendance Details Updated for {emp_name[0]}")
    return redirect('view_attendance')



def base_dashboard(request):
     return render(request,"base_dashboard.html")


@csrf_exempt
def dashboard(request):
    cursor = connection.cursor()
    global a,b,c,d 
    query1 = "select count(*) AS employee_id from employee;"
    query2 = "select count(*) AS present_employee from attendance where emp_status = 'Present' and attendance_date = CURDATE();"
    query3 = "select count(*) AS absent_employee from attendance where emp_status = 'Absent' and attendance_date = CURDATE();"
    query4 = """SELECT emp.full_name,
       emp.department,
       att.emp_status,
       att.attendance_date,
       att.in_time
FROM employee emp
RIGHT JOIN attendance att
  ON att.emp_id = emp.emp_id
ORDER BY 
  CAST(att.attendance_date AS DATE) DESC,
  CAST(att.in_time AS TIME) DESC
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
