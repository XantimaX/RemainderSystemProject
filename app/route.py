from app import app,login
from flask import render_template, redirect, request,url_for,session,send_from_directory,flash,get_flashed_messages,jsonify
from app.forms import Upload
from handout_reader import handout_reader_pdf,handout_reader_word
from sorting import sort_dates
from re import search
from excel_sheet_generator import create_excel_sheet
from app.forms import RegisterForm, LoginForm
from dbms_methods import add_user, search_user,give_reminder_records,add_reminder_record
from flask_login import current_user, login_user, logout_user,login_required
from datetime import datetime, date
import json

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    if current_user.is_authenticated :
        return redirect(url_for("index"))
    login_form = LoginForm()
    if login_form.validate_on_submit() :
        user = search_user(login_form.username.data)
        if user :
            if user.check_password(login_form.password.data) :
                login_user(user)
                next_url = request.args.get("next")
                return redirect(next_url or url_for("index"))
            flash("Invalid Password")
        else :
            flash("User not found")
    else :
        print(login_form.errors)

    return render_template("login.html", login_form=login_form )

@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit() :
        if (add_user(register_form)) :
            flash("Account Created Successfully ! Please Login", "success")
        else :
            flash("Error : Username already exists", "error")

    else :
        print(register_form.errors)

    return render_template("register.html", register_form = register_form)

@app.route("/logout")
def logout() :
    logout_user()
    return redirect(url_for("index"))

@app.route("/reminder_view")
@login_required
def reminder_view():
    reminder_records = give_reminder_records(current_user)
    return render_template("reminder.html", reminder_records=reminder_records, current_date = date.today())

@app.route("/upload_menu" , methods = ["GET", "POST"])
def upload_menu() :
    upload = Upload()
    if upload.validate_on_submit():
        redirect(url_for("upload"))

    return render_template("upload.html", upload=upload)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    details = []
    files = request.files.getlist("file")
    for file in files :
        if file.filename == "" :
            continue
        filename = file.filename
        filepath = rf"{app.config['UPLOAD_FOLDER']}\{filename}"
        file.save(filepath)

        if filename.split(".")[-1] == "pdf" :
            details.extend(handout_reader_pdf(filepath))
        elif filename.split(".")[-1] == "docx" :
            details.extend(handout_reader_word(filepath))

    session["details"] = details
    return redirect(url_for("create_or_download"))

@app.route("/create_or_download", methods=["GET", "POST"])
def create_or_download():
    details = session.get("details", [])
    details = sort_dates(details)

    invalid_index = len(details)
    for index,detail in enumerate(details) :
        if (not(search("\d\d/\d\d/\d\d\d?\d?",detail[2]))) :
            invalid_index = index
            break

    return render_template("create_or_download.html", valid_details=details[:invalid_index], invalid_details=details[invalid_index:])


@app.route("/component_adder", methods = ["POST"])
def add_component():
    data = request.json
    valid_list = data["valid_course"]
    details = session["details"]

    for i in valid_list :
        for j in details :
            if i[0] == j[0] and i[1] == j[1] :
                j[2] = i[2]
                break


    session["details"] = details 
       
    return redirect(url_for("create_or_download"))
    
@app.route("/reminder", methods = ["POST"])
@login_required
def add_reminders():
    data = request.json
    details = data["details"]
    for detail in details :
        add_reminder_record(detail,current_user)
    return jsonify({'message': 'Reminders added successfully!'})

@app.route("/download_excel")
def download_excel():
    valid_details = session.get("valid_details",[])
    filename = create_excel_sheet(valid_details)
    return send_from_directory(app.config["DOWNLOAD_FOLDER"],filename)


