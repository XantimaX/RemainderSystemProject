from sqlalchemy import String,Column, Integer,Date,ForeignKey
from sqlalchemy.orm import Mapped,relationship
from dbms_config import session, Base
from flask_login import UserMixin, LoginManager
from app import login
from typing import List

@login.user_loader
def load_user(id):
    return session.query(User).get(int(id))

class User(Base,UserMixin):
    __tablename__ = "user"
    user_id : Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    user_name : Mapped[String] = Column(String(100), nullable=False)
    password_hash : Mapped[String] = Column(String(50))
    email_id : Mapped[String] = Column(String(50), nullable=False)

    reminder : Mapped[List["Reminder"]] = relationship("Reminder", back_populates="user", )


class Reminder(Base):
    __tablename__ = "reminder"
    reminder_id : Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    course_name : Mapped[String] = Column(String(50), nullable = False)
    component_name : Mapped[String] = Column(String(50) ,nullable = False)
    date : Mapped[Date] = Column(Date,nullable = False)
    user_id :Mapped[int] = Column(Integer, ForeignKey("user.user_id"))

    user : Mapped[User] = relationship("User", back_populates="reminder")



