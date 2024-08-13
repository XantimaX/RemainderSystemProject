from dbms_config import session
from app.models import  User,Reminder
from app import db
from sqlalchemy import and_
from sqlalchemy.exc import  IntegrityError
from datetime import date,datetime
def add_user(form):

    new_user = User(user_name = form.username.data, email_id = form.email.data)
    new_user.password_hash = new_user.set_password(form.password.data)
    try :
        db.session.add(new_user)
        db.session.commit()
        return True
    except IntegrityError :
        db.session.rollback()
        return False

def search_user(username):
    user = db.session.query(User).filter(User.user_name == username).one_or_none()
    return user

def give_reminder_records(current_user) :
    remove_expired_reminder_records(current_user)

    user_id = current_user.user_id
    reminder_records = db.session.query(User).get(user_id).reminder

    return reminder_records

def remove_expired_reminder_records(current_user):
    current_date = datetime.today().date()
    db.session.query(Reminder).filter(and_(Reminder.user_id == current_user.user_id ,Reminder.date < current_date)).delete()
    db.session.commit()

def add_reminder_record(reminder_detail, current_user):

    date_arr = reminder_detail[2].split("/")
    date_arr[2] = date_arr[2] if len(date_arr[2]) == 4 else "20" + date_arr[2]

    course_name,component_name = reminder_detail[0], reminder_detail[1]
    component_date = date(int(date_arr[2]),int(date_arr[1]),int(date_arr[0]))
    records = db.session.query(Reminder).filter(and_(Reminder.user_id == current_user.user_id, Reminder.course_name == course_name , Reminder.component_name == component_name , Reminder.date == component_date)).all()

    if db.session.query(Reminder).filter(and_(Reminder.user_id == current_user.user_id, Reminder.course_name == course_name , Reminder.component_name == component_name , Reminder.date == component_date)).one_or_none():
        print("Already Present")
        return

    reminder_record = Reminder(course_name = course_name, component_name = component_name, date = component_date, user_id = current_user.user_id)
    db.session.add(reminder_record)
    db.session.commit()

    remove_expired_reminder_records(current_user)