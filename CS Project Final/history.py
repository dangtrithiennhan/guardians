from flask import Blueprint, Flask, render_template, url_for, session
import settings 

con = settings.get_database_connection()
history = Blueprint('history', __name__)

@history.route("/attendance_history.html")
def attendance_list():
    if not settings.check_valid_session() :
       return render_template('login.html', message="Please login to your account") 
    else :
       username = session['user'];
       cur=con.cursor()
       vols=cur.execute("SELECT  to_char(a.attendance_date,'dd-Mon-yyyy'), b.batch_name, c.centre_name, a.comments from god_volunteers v, god_attendance a, god_batches b, god_centres c where upper(v.email_address) = upper('"+username+"') and v.volunteer_code = a.volunteer_code and a.batch_code = b.batch_code and b.centre_code = c.centre_code(+) and rownum <=10 order by a.attendance_date desc").fetchall()
       cur.close()
       headers = ['Attendance Date', 'Batch Name' , 'Centre Name', 'Comments']
       return render_template('attendance_history.html', name=session['name'], role=session['role'], pages=settings.generate_page_list(), headers=headers, tableData=vols, deleteLink="Y")


@history.route("/attendance_delete/<string:attendance_date>",methods = ['GET', 'POST'])
def delete(attendance_date):
    if not settings.check_valid_session() :
       return render_template('login.html', message="Please login to your account") 
    else :
       if attendance_date :
         deleteLink = "Y"
         username = session['user'];
         cur=con.cursor()
         cur.execute("DELETE FROM god_attendance WHERE attendance_date = to_date('"+attendance_date+"', 'dd-Mon-yyyy') AND volunteer_code = (select volunteer_code from god_volunteers v  where upper(v.email_address) = upper('"+username+"'))")
         con.commit()
         cur.close()
         msg="Attendance deleted for "+ attendance_date
         cur=con.cursor()
         vols=cur.execute("SELECT  to_char(a.attendance_date,'dd-Mon-yyyy'), b.batch_name, c.centre_name, a.comments from god_volunteers v, god_attendance a, god_batches b, god_centres c where upper(v.email_address) = upper('"+username+"') and v.volunteer_code = a.volunteer_code and a.batch_code = b.batch_code and b.centre_code = c.centre_code(+) and rownum <=10 order by a.attendance_date desc").fetchall()
         cur.close()
         headers = ['Attendance Date', 'Batch Name' , 'Centre Name', 'Comments']
         return render_template('attendance_history.html', name=session['name'], role=session['role'], pages=settings.generate_page_list(), headers=headers, tableData=vols, deleteLink="Y", message=msg)
