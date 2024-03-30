from flask import Blueprint, Flask, render_template, url_for, session
import settings 

con = settings.get_database_connection()
profile = Blueprint('profile', __name__)

@profile.route("/profile.html")
def profile_list():
    if not settings.check_valid_session() :
       return render_template('login.html', message="Please login to your account") 
    else :
       username = session['user'];
       print(username)
       cur=con.cursor()
       vols=cur.execute("SELECT  v.volunteer_code, v.first_name, nvl(v.middle_name,' '), nvl(v.last_name,' '), l.lookup_value, c.city_unit_name, cn.centre_name, b.batch_name, v.email_Address, v.primary_phone_number, v.alternate_phone_number, to_char(v.birth_date,'dd-Mon-yyyy'), to_char(v.hire_date,'dd-Mon-yyyy'), v.address  from god_volunteers v, god_city_units c, god_batches b, god_centres cn, god_lookups l  where upper(v.email_address) = upper('"+username+"') and v.city_unit_code = c.city_unit_code(+) and v.batch_code = b.batch_code(+) and b.centre_code = cn.centre_code(+) and v.volunteer_type = l.lookup_code (+) and l.lookup_type (+) = 'VOLUNTEER_TYPE'").fetchall()
       cur.close()
       labels = ['Volunteer Code', 'First Name', 'Middle Name', 'Last Name', 'Volunteer Type', 'City', 'Centre', 'Batch', 'E-mail Address', 'Phone Number', 'Alternate Phone Number', 'Birth Date', 'Hire Date', 'Address']
       return render_template('profile.html',  name=session['name'], role=session['role'], pages=settings.generate_page_list(), labels=labels, formData=vols)

