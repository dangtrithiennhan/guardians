from flask import Blueprint, Flask, render_template, url_for, session
import settings 

con = settings.get_database_connection()
students = Blueprint('students', __name__)

@students.route("/students.html")
def student_list():
    if not settings.check_valid_session() :
       return render_template('login.html', message="Please login to your account") 
    else :
       username = session['user'];
       cur=con.cursor()
       vols=cur.execute("SELECT  s.first_name||' ' ||s.last_name, l.lookup_value, to_char(s.birth_date,'dd-Mon-yyyy'), s.school_grade||'' from god_volunteers v, god_students s, god_lookups l where upper(v.email_address) = upper('"+username+"') and v.batch_code = s.batch_code and s.gender = l.lookup_code(+) and l.lookup_type(+) = 'GENDER' order by v.first_name||' ' ||v.last_name").fetchall()
       cur.close()
       headers = ['Student Name', 'Gender', 'Date of Birth' , 'School Grade']
       return render_template('students.html', name=session['name'], role=session['role'], pages=settings.generate_page_list(), headers=headers, tableData=vols)

