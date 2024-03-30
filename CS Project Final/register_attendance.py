from flask import Blueprint, Flask, render_template, url_for, request, redirect, session
from datetime import datetime
import settings 

con = settings.get_database_connection()
register_attendance = Blueprint('register_attendance', __name__)

@register_attendance.route("/register_attendance.html", methods =["GET", "POST"])
def attendance():
    if not settings.check_valid_session() :
       return render_template('login.html', message="Please login to your account") 
    else :
       print("***$**")
       username = session['user']
       attendance_date = request.form.get("attendance_date");
       if not attendance_date :
         attendance_date = '1900-01-01'
       cur=con.cursor()
       vols=cur.execute("SELECT  c.centre_code, c.centre_name, b.batch_code, b.batch_name, a.attendance_date, a.comments from god_volunteers v, god_batches b, god_centres c, god_attendance a  where upper(v.email_address) = upper('"+username+"') and v.batch_code = b.batch_code and b.centre_code = c.centre_code and v.volunteer_code = a.volunteer_code(+) and v.batch_code = a.batch_code(+) and a.attendance_date(+) = to_date('"+attendance_date+"','yyyy-mm-dd') and rownum=1").fetchall()
       cur.close()
       return render_template('register_attendance.html',  name=session['name'], role=session['role'], pages=settings.generate_page_list(), formData=vols)



@register_attendance.route("/attendance_submit", methods =["GET", "POST"])
def attendance_save():
    username = session['user']
    message = None
    volunteerCode = None
    batchCode = None
    attendance_date = request.form.get("class_date");
    comments = request.form.get("comments");

    ##Get form values to update##
    cur=con.cursor()
    vols=cur.execute("SELECT  v.volunteer_code, v.batch_code, a.attendance_date, a.comments from god_volunteers v, god_attendance a  where upper(v.email_address) = upper('"+username+"') and v.volunteer_code = a.volunteer_code(+) and v.batch_code = a.batch_code(+) and a.attendance_date(+) = to_date('"+attendance_date+"','yyyy-mm-dd') and rownum=1").fetchall()
    cur.close()
    
    row = vols[0]; 
    volunteerCode = row[0]
    batchCode = row[1]
    date = datetime.strptime(attendance_date,"%Y-%m-%d")
    if row[2] :
        message = "ERROR: Attendance exists for the entered date (%s)" % str(date.strftime("%d-%m-%Y"))
    elif (date > datetime.today()) : 
        message = "ERROR: Cannot record attendance for a date in future (%s)" % str(date.strftime("%d-%m-%Y"))
    else :
        cur=con.cursor()
        cur.execute("INSERT INTO god_attendance values ('"+volunteerCode+"',to_date('"+attendance_date+"','yyyy-mm-dd'),'"+batchCode+"','"+comments+"')")
        con.commit()
        cur.close()
        message = "Attendance has been recorded"

    cur=con.cursor()
    vols=cur.execute("SELECT  c.centre_code, c.centre_name, b.batch_code, b.batch_name, a.attendance_date, a.comments from god_volunteers v, god_batches b, god_centres c, god_attendance a  where upper(v.email_address) = upper('"+username+"') and v.batch_code = b.batch_code and b.centre_code = c.centre_code and v.volunteer_code = a.volunteer_code(+) and v.batch_code = a.batch_code(+) and a.attendance_date(+) = to_date('"+attendance_date+"','yyyy-mm-dd') and rownum=1").fetchall()
    cur.close()
    return render_template('register_attendance.html',  name=session['name'], role=session['role'], pages=settings.generate_page_list(), formData=vols, message=message)