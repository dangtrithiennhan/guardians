from flask import Flask, render_template, url_for, request, redirect, session

#Import for common settings
import settings

#Modular functionality
from profile import profile
from volunteers import volunteers
from students import students
from institutions import institutions
from history import history
from institution_details import institution_details
from register_attendance import register_attendance
 
app = Flask(__name__)
app.secret_key = 'ItShouldBeAnythingButSecret'  
app.register_blueprint(profile)
app.register_blueprint(volunteers)
app.register_blueprint(students)
app.register_blueprint(institutions)
app.register_blueprint(history)
app.register_blueprint(institution_details)
app.register_blueprint(register_attendance)

print('Starting..')
print('Checking database connection')
con = settings.get_database_connection()
print('Database connected!')

@app.route('/login', methods = ['POST', 'GET'])
@app.route('/', methods = ['POST', 'GET'])
@app.route('/login.html', methods = ['POST', 'GET'])
def login():
    message = ""
     
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')  
        cur=con.cursor()
        user=cur.execute("SELECT TO_CHAR(assigned_pin), v.first_name||' '||v.last_name name, l.lookup_value rolename from god_volunteers v, god_lookups l where upper(v.email_address) = upper('"+username+"') and v.volunteer_type = l.lookup_code (+) and l.lookup_type (+) = 'VOLUNTEER_TYPE' AND ROWNUM = 1").fetchone()
        cur.close()

        if user != None and len(user) > 0 and user[0] == password:
            session['user'] = username
            session['name'] = user[1]
            session['role'] = user[2]
            print('Valid user..')
            return redirect("/profile.html")
            print('Done..') 

        if username != None or password != None:
            message = "Invalid username or password"
 
    #if the username or password does not matches, redirect to login page 
    return render_template("login.html", message=message)

@app.route('/logout.html', methods = ['POST', 'GET'])
@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    session.pop('user')
    session.pop('name')
    session.pop('role')
    return render_template("login.html", message="You have been logged out")
  

@app.route("/about_us.html")
def about():
    if not settings.check_valid_session() :
       return redirect(url_for('login')) 
    else :
       pages = settings.generate_page_list()
       return render_template('about_us.html', name=session['name'], role=session['role'], pages=pages)

#Step -7(run the app)
if __name__ == '__main__':
    app.run(debug=True)
