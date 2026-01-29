# QuessCorp - Task is Give by QuessCorp Vendor Company - for Grenn Rider company


## HRM Lite – Admin Panel (Deployed on Railway)

### 🔗 Live Project URL

👉 [https://quesscorp-production-90ab.up.railway.app/]

## 📌 Project Overview

HRM Lite is a **simple Human Resource Management (HRM) Admin Panel** developed to manage employees and their attendance records.
This project focuses on core HR functionalities with a clean dashboard and easy navigation.
It is deployed on **Railway** and currently works **without authentication (login is not required)**.


## 📊 Dashboard Features

The dashboard provides a quick overview of employee and attendance data using summary cards and tables:

* **Total Employees Count**
* **Present Employees Count (Current Day)**
* **Absent Employees Count (Current Day)**

### Recently Marked Attendance Table

Displays:

* Employee Name
* Department
* Attendance Status (Present / Absent)

## 📂 Side Menu Navigation

The side menu contains quick links to the following pages:

* **Dashboard**
* **Attendance Page**
* **Employee View Page**
* **Add Employee Form**

Each menu item redirects to its respective page where complete data can be viewed or managed.


## 👤 Employee Management

### ➕ Add Employee

* New employees can be added using the **Add Employee Form**
* Employee details are saved directly to the database

### 📋 View Employee Page

* Displays details of **all employees**
* Admin can **delete existing employees**
* Includes **three filters**:

  * **Dynamic Filter (Database Level)**

    * Filter by **Employee Name**
    * Filter by **Employee Email**
  * **Static Filter (JavaScript Based)**

    * Works only on the currently displayed UI data


## 🕒 Attendance Management

### Attendance Page Features

Displays attendance-related data such as:

* Employee Name
* Employee ID
* In-Time
* Out-Time
* Attendance Date
* Status

### Filters on Attendance Page

* **Dynamic Filter (Database Level)**

  * Filter attendance records by **Date**
* **Static Filter (UI Level)**

  * Search any value but works only on currently visible data

### Mark Attendance

* Each employee record has an **Attendance Button**
* Admin can mark:

  * **Current day attendance**
  * **Previous day attendance**

## 🔐 Authentication

* This is a **complete HRM Admin Panel**
* **No login or authentication is required** (intentionally kept simple)

## 🛠 Tech Stack 
* Python
* Django
* HTML, CSS, JavaScript, Bootstrap, jquery, font-awesome, popper
* MySQL Database
* Railway (Deployment)