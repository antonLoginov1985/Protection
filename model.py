from flask_login import UserMixin
from sqlalchemy import (
    Column,
    Integer,
    Date,
    String,
    DECIMAL,
    TEXT,
    DateTime,
    Boolean
)
from datetime import datetime
# from app import db_sesssion, manager, Base
from app import db, manager


class Employees(db.Model):

    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    zup_code = Column(String(10), unique=True, nullable=False)
    last_name = Column(TEXT, nullable=False)
    first_name = Column(TEXT, nullable=False)
    middle_name = Column(TEXT, nullable=False)
    snils = Column(String(15), unique=True, nullable=False)
    hire_date = Column(DateTime)
    department_id = Column(Integer, db.ForeignKey(
        'departments.id'), nullable=False)
    position_id = Column(Integer, db.ForeignKey(
        'positions.id'), nullable=False)
    organization_id = Column(Integer, db.ForeignKey(
        'organization.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # reviews = db.relationship('Reviews', backref='market', lazy='dynamic')


class Department(db.Model):

    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    zup_code = Column(String(10), unique=True, nullable=False)
    name = Column(String)
    parent_id = Column(Integer, db.ForeignKey('departments.id'))
    # сhildren = db.relationship('Department', backref=db.relationship(
    #     'Department', remote_side=[id], foreign_keys=[parent_id]))
    сhildren = db.relationship('Department', backref='Department', remote_side=[
                               id], foreign_keys=[parent_id])


class Positions(db.Model):

    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    zup_code = Column(String(10), unique=True, nullable=False)
    name = Column(TEXT, nullable=False)


class Organization(db.Model):

    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True)
    zup_code = Column(String(10), unique=True, nullable=False)
    fullname = Column(TEXT, nullable=False)
    inn = Column(TEXT, nullable=False)
    kpp = Column(TEXT, nullable=False)


class Instructiontypes(db.Model):

    __tablename__ = 'instructiontypes'

    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=False)


class Place(db.Model):

    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=False)
    address = Column(TEXT)
    is_training = Column(Boolean)
    is_certification = Column(Boolean)


class Program(db.Model):

    __tablename__ = 'programs'

    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=False)
    bloсk_id = Column(Integer, db.ForeignKey(
        'bloсktraining.id'), nullable=False)


class Certificationtypes(db.Model):

    __tablename__ = 'certificationtypes'

    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=False)


class Bloсktraining(db.Model):

    __tablename__ = 'bloсktraining'

    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=False)


class Bloсkcertification(db.Model):

    __tablename__ = 'bloсkcertification'

    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=False)


class Typedocument(db.Model):

    __tablename__ = 'typedocuments'

    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=False)


class Typetraining(db.Model):

    __tablename__ = 'typetraining'

    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=False)


class Training(db.Model):

    __tablename__ = 'training'

    id = Column(Integer, primary_key=True)
    employees_id = Column(Integer, db.ForeignKey(
        'employees.id'), nullable=False)
    training_date = Column(DateTime)
    block_training_id = Column(Integer, db.ForeignKey(
        'bloсktraining.id'), nullable=False)
    program_id = Column(Integer, db.ForeignKey(
        'programs.id'), nullable=False)
    type_training_id = Column(Integer, db.ForeignKey(
        'typetraining.id'), nullable=False)
    place_id = Column(Integer, db.ForeignKey(
        'places.id'), nullable=False)
    type_document_id = Column(Integer, db.ForeignKey(
        'typedocuments.id'), nullable=False)
    date_document = Column(DateTime)
    number_document = Column(String(20))
    result = Column(Boolean)
    next_date = Column(DateTime)
    file_path = Column(TEXT)
    timestamp = Column(DateTime, default=datetime.utcnow)


class questions(db.Model):
    __tablename__ = "questions"
    qid = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False)
    question = db.Column(db.String, nullable=False)
    option1 = db.Column(db.String, nullable=True)
    option2 = db.Column(db.String, nullable=True)
    option3 = db.Column(db.String, nullable=True)
    option4 = db.Column(db.String, nullable=True)
    answer = db.Column(db.Integer, nullable=True)
    bcol = db.Column(db.String, nullable=True)
    is_last = Column(Boolean)


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String(128), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    psw = Column(String(255), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean)
    is_manager = Column(Boolean)

    def __repr__(self):
        return '<User %r>' % self.username

    # def is_authenticated(self):
    #     return True
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    # return db_sesssion.query(User).filter_by(id=user_id).one()

def get_place_with_address():
   
    return db_sesssion.query(Place).filter_by(Place.address != None).all()
