from app import app
from flask import render_template, redirect, request,url_for,session,send_from_directory
from app.forms import Upload
from handout_reader import handout_reader_pdf,handout_reader_word
from sorting import sort_dates
from re import search
from excel_sheet_generator import create_excel_sheet
@app.route("/")
def index():
    return render_template("home.html")

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
        filename = file.filename
        filepath = rf"{app.config['UPLOAD_FOLDER']}\{filename}"
        file.save(filepath)

        if filename.split(".")[-1] == "pdf" :
            details.extend(handout_reader_pdf(filepath))
        elif filename.split(".")[-1] == "docx" :
            details.extend(handout_reader_word(filepath))

    details = sort_dates(details)
    session["details"] = details
    return redirect(url_for("create_or_download"))

@app.route("/create_or_download", methods=["GET", "POST"])
def create_or_download():
    details = session.get("details", [])
    invalid_index = len(details)
    for index,detail in enumerate(details) :
        if (not(search("\d\d/\d\d/\d\d\d?\d?",detail[2]))) :
            invalid_index = index
            break

    session["valid_details"] = details[:invalid_index]
    return render_template("create_or_download.html", valid_details=details[:invalid_index], invalid_details=details[invalid_index:])


@app.route("/download_excel")
def download_excel():
    valid_details = session.get("valid_details",[])
    filename = create_excel_sheet(valid_details)
    return send_from_directory(app.config["DOWNLOAD_FOLDER"],filename)


