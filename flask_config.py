import os

base_dir = os.path.abspath(os.path.dirname(__file__))
class Config:
     SECRET_KEY = os.environ.get('SECRET KEY') or 'default'
     UPLOAD_FOLDER = r"C:\Users\oldem\Desktop\Handout_Upload"
     DOWNLOAD_FOLDER = r"C:\Users\oldem\PycharmProjects\RemainderSystemProject\excel_sheets"
     # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'app.db')