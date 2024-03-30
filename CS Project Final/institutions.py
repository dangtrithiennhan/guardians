from flask import Blueprint, Flask, render_template, url_for, session
import settings 

con = settings.get_database_connection()
institutions = Blueprint('institutions', __name__)

@institutions.route("/institutions.html")
def institute_list():
    if not settings.check_valid_session() :
       return render_template('login.html', message="Please login to your account") 
    else :
       username = session['user'];
       editLink = None;
       print('******')
       print(session['role']);
       role = session['role'];
       if "Admin" == role:
         editLink = "./institution_details.html?centre_code={{row[loop.index0]}}"

       print('******')
       print(editLink);
       cur=con.cursor()
       vols=cur.execute("SELECT  c.centre_code, c.centre_name, c.primary_phone_number, c.email_address, c.address from god_volunteers v, god_centres c where v.city_unit_code = c.city_unit_code and upper(v.email_address) = upper('"+username+"') order by c.centre_name").fetchall()
       cur.close()
       headers = ['Centre Code', 'Centre Name', 'Phone Number', 'E-mail Address',  'Address']
       return render_template('institutions.html', name=session['name'], role=session['role'], pages=settings.generate_page_list(), headers=headers, tableData=vols, editLink = editLink)

