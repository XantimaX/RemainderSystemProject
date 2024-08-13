from sqlalchemy import String,Column, Integer,Date,ForeignKey
from sqlalchemy.orm import Mapped,relationship
from dbms_config import session
from flask_login import UserMixin, LoginManager
from app import login
from typing import List
from werkzeug.security import  generate_password_hash, check_password_hash
from app import db


class User(db.Model,UserMixin):
    __tablename__ = "user"
    user_id : Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    user_name : Mapped[String] = Column(String(100), nullable=False, unique=True)
    password_hash : Mapped[String] = Column(String(200))
    email_id : Mapped[String] = Column(String(50), nullable=False)

    reminder : Mapped[List["Reminder"]] = relationship("Reminder", back_populates="user",order_by="Reminder.date")

    def set_password(self,password):
        return generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def get_id(self):
        return str(self.user_id)

@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))

class Reminder(db.Model):
    __tablename__ = "reminder"
    reminder_id : Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    course_name : Mapped[String] = Column(String(50), nullable = False)
    component_name : Mapped[String] = Column(String(50) ,nullable = False)
    date : Mapped[Date] = Column(Date,nullable = False)
    user_id :Mapped[int] = Column(Integer, ForeignKey("user.user_id"))
    
    user : Mapped[User] = relationship("User", back_populates="reminder")


