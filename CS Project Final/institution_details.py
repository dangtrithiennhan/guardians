from flask import Blueprint, Flask, render_template, url_for, request, session
import settings 

con = settings.get_database_connection()
institution_details = Blueprint('institution_details', __name__)

@institution_details.route("/institution_details.html")
def institution():
    if not settings.check_valid_session() :
       return render_template('login.html', message="Please login to your account") 
    else :
       username = session['user']
       centre_code=request.args['centre_code']
       print(username)
       print(centre_code)
       cur=con.cursor()
       vols=cur.execute("SELECT  c.centre_code, c.centre_name, c.description, c.centre_type, c.primary_phone_number, c.alternate_phone_number, c.email_address, c.address, c.coordinator_flag, c.coordinator_phone_number, c.number_of_residents, c.number_of_classrooms, c.classroom_furniture_flag, c.writing_board_type, c.parking_type, c.water_dispenser_flag, c.stationery_flag, c.storage_flag, c.security_flag, c.power_backup_flag, c.medical_kit_flag, c.guest_toilet_flag, c.kitchen_flag, c.last_updated from god_volunteers v, god_centres c  where upper(v.email_address) = upper('"+username+"') and upper(v.volunteer_type) = 'ADMIN' and v.city_unit_code = c.city_unit_code and c.centre_code = upper('"+centre_code+"')").fetchall()
       cur.close()
       return render_template('institution_details.html',  name=session['name'], role=session['role'], pages=settings.generate_page_list(), formData=vols)


@institution_details.route("/institution_submit", methods =["GET", "POST"])
def institution_save():
    username = session['user']
 
    ##Get form values to update##
    centre_code = request.form.get("centre_code");
    centre_name = request.form.get("centre_name");
    description = request.form.get("description");
    centre_type = request.form.get("centre_type");
    primary_phone = request.form.get("primary_phone");
    alternate_phone = request.form.get("alternate_phone");
    email = request.form.get("email");
    address = request.form.get("address");
    coordinator = request.form.get("coordinator");
    coordinator_phone = request.form.get("coordinator_phone");
    residents = request.form.get("residents");
    classrooms = request.form.get("classrooms");
    furniture = request.form.get("furniture");
    board_type = request.form.get("board_type");
    parking_type = request.form.get("parking_type");
    water_dispenser = request.form.get("water_dispenser");
    stationery = request.form.get("stationery");
    storage = request.form.get("storage");
    security = request.form.get("security");
    power_backup = request.form.get("power_backup");
    medical_kit = request.form.get("medical_kit");
    guest_toilet = request.form.get("guest_toilet");
    kitchen = request.form.get("kitchen");
    #+ "', centre_type = '" + centre_type 
    cur=con.cursor()
    cur.execute("UPDATE god_centres set centre_name = '" + centre_name + "', description = '" + description + "', centre_type = '" + centre_type + "', primary_phone_number = '" + primary_phone + "', alternate_phone_number = '" + alternate_phone + "', email_address = '" + email + "', address = '" + address + "', coordinator_flag = '" + coordinator + "', coordinator_phone_number = '" + coordinator_phone + "', number_of_residents = '" + residents + "', number_of_classrooms = '" + classrooms + "', classroom_furniture_flag = '" + furniture + "', writing_board_type = '" + board_type + "', parking_type = '" + parking_type + "', water_dispenser_flag = '" + water_dispenser + "', stationery_flag = '" + stationery + "', storage_flag = '" + storage + "', security_flag = '" + security + "', power_backup_flag = '" + power_backup + "', medical_kit_flag = '" + medical_kit + "', guest_toilet_flag = '" + guest_toilet + "', kitchen_flag = '" + kitchen + "', last_updated = '" + username +"' where centre_code=upper('" +centre_code+ "')")
    cur.close()
    con.commit()
    
    cur=con.cursor()
    vols=cur.execute("SELECT  c.centre_code, c.centre_name, c.description, c.centre_type, c.primary_phone_number, c.alternate_phone_number, c.email_address, c.address, c.coordinator_flag, c.coordinator_phone_number, c.number_of_residents, c.number_of_classrooms, c.classroom_furniture_flag, c.writing_board_type, c.parking_type, c.water_dispenser_flag, c.stationery_flag, c.storage_flag, c.security_flag, c.power_backup_flag, c.medical_kit_flag, c.guest_toilet_flag, c.kitchen_flag, c.last_updated from god_volunteers v, god_centres c  where upper(v.email_address) = upper('"+username+"') and v.city_unit_code = c.city_unit_code and c.centre_code = upper('"+centre_code+"')").fetchall()
    cur.close()

    return render_template('institution_details.html',  name=session['name'], role=session['role'], pages=settings.generate_page_list(), formData=vols, message="Your changes are saved")

