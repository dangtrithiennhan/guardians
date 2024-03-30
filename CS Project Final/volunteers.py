from flask import Blueprint, Flask, render_template, url_for, session
import settings 

con = settings.get_database_connection()
volunteers = Blueprint('volunteers', __name__)

@volunteers.route("/volunteers.html")
def volunteer_list():
    if not settings.check_valid_session() :
       return render_template('login.html', message="Please login to your account") 
    else :
       username = session['user'];
       cur=con.cursor()
       vols=cur.execute("SELECT  v.first_name||' ' ||v.last_name, v.primary_phone_number, v.email_address, c.centre_name, b.batch_name from god_volunteers v, god_volunteers l, god_batches b, god_centres c where v.city_unit_code = l.city_unit_code and upper(l.email_address) = upper('"+username+"') and v.batch_code = b.batch_code(+) and b.centre_code = c.centre_code(+) order by v.first_name||' ' ||v.last_name").fetchall()
       cur.close()
       headers = ['Volunteer Name', 'Phone Number', 'E-mail Address' , 'Centre Name', 'Batch Name']
       return render_template('volunteers.html', name=session['name'], role=session['role'], pages=settings.generate_page_list(), headers=headers, tableData=vols)

