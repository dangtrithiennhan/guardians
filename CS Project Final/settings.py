from flask import Flask, render_template, url_for, session, redirect

#Import for Oracle Autonomous Database on the Cloud
import oracledb

dbc = None

#Get a database connection
def get_database_connection():
     global dbc
     reconnect = False;
     if dbc is None : 
        reconnect = True;
     else :
        try : 
          dbc.getCursor().execute("SELECT * from dual").fetchone();
        except Exception as e:
          reconnect = True;
    
     if reconnect :    
     	dbc= oracledb.connect(
     		user="thiennhan",
     		password="KrishLinh123!",
     		dsn="kvtq93bgoyg8wtqx_high",
     		config_dir="/Users/krmahade/D/Wallet",
     		wallet_location="/Users/krmahade/D/Wallet",
     		wallet_password="KrishLinh123!")
     return dbc


#Global Page List
def generate_page_list():
    global pages 
    pages = [
        {"name": "Profile", "url": url_for('profile.profile_list'), "icon": "fas fa-home"
         },
        {"name": "Child Care Institutions", "url": url_for('institutions.institute_list'), "icon": "fas fa-school"
        },
        {"name": "City Volunteers", "url": url_for('volunteers.volunteer_list'), "icon": "fas fa-users"
         },
        {"name": "Batch Students", "url": url_for('students.student_list'), "icon": "fas fa-users"
         },
        {"name": "Attendance History", "url": url_for('history.attendance_list'), "icon": "fas fa-list"
         },
        {"name": "Register Attendance", "url": url_for('register_attendance.attendance'), "icon": "fas fa-pen"
         },
        {"name": "About Us", "url": url_for('about'), "icon": "fas fa-info"
         },
        {"name": "Logout", "url": url_for('logout'), "icon": "fas fa-power-off"
         },
    ]
    return pages

#Check if valid user session
def check_valid_session():
    if 'user' not in session :
       print('User not logged in, redirect to login page')
       return False
    else :
       return True 
   

