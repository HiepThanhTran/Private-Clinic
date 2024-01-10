from datetime import datetime
from enum import Enum as DbEnum

from flask_login import UserMixin
from slugify import slugify
from sqlalchemy import Column, String, Boolean, Enum, DateTime, ForeignKey, BigInteger, Double, Integer
from sqlalchemy import event
from sqlalchemy.orm import relationship

from private_clinic.app import db, app


class AccountRoleEnum(DbEnum):
    PATIENT = 1
    DOCTOR = 2
    NURSE = 3
    STAFF = 4
    ADMIN = 5


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now(), nullable=False)
    updated_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class Account(BaseModel, UserMixin):
    __tablename__ = 'accounts'

    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    slug = Column(String(50), nullable=False, unique=True)
    active = Column(Boolean, default=True, nullable=False)
    is_confirmed = Column(Boolean, nullable=False, default=False)
    confirmed_on = Column(DateTime, nullable=True)
    avatar = Column(String(255),
                    default='https://res.cloudinary.com/dtthwldgs/image/upload/v1704344793/robot-head-avatar-design-cartoon-robot-head'
                            '-icon-vector-removebg-preview_lb3smh.png')
    role = Column(Enum(AccountRoleEnum), default=AccountRoleEnum.PATIENT, nullable=False)

    user = relationship('User', backref='account', lazy=True, uselist=False)

    def __str__(self):
        return self.username

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)


event.listen(Account.username, 'set', Account.slugify, retval=False)


class User(BaseModel):
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(String(10))
    dob = Column(DateTime)
    address = Column(String(100))
    phone_number = Column(String(11), unique=True)
    email = Column(String(50), nullable=False, unique=True)
    account_id = Column(BigInteger, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False, unique=True)

    patient = relationship('Patient', backref='user', lazy=True, uselist=False)
    employee = relationship('Employee', backref='user', lazy=True, uselist=False)

    @property
    def full_name(self):
        return self.last_name + ' ' + self.first_name

    def __str__(self):
        return self.full_name


class Patient(db.Model):
    __tablename__ = 'patients'

    id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    insurance_id = Column(String(20), unique=True)

    bills = relationship('Bill', backref='patient', lazy=True)
    medical_bills = relationship('MedicalBill', backref='patient', lazy=True)
    examination_schedule_list = relationship('ExaminationSchedule', backref='patient', lazy=True)


class Employee(db.Model):
    __tablename__ = 'employees'

    id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    salary = Column(Double, default=0)
    salary_coefficient = Column(Double, default=1)

    admin = relationship('Administrator', backref='employee', lazy=True, uselist=False)
    cashier = relationship('Cashier', backref='employee', lazy=True, uselist=False)
    doctor = relationship('Doctor', backref='employee', lazy=True, uselist=False)
    nurse = relationship('Nurse', backref='employee', lazy=True, uselist=False)


class Administrator(db.Model):
    __tablename__ = 'administrators'

    id = Column(BigInteger, ForeignKey('employees.id'), primary_key=True)
    inauguration_day = Column(DateTime, nullable=False)

    regulations = relationship('Regulation', backref='administrator', lazy=True)


class Cashier(db.Model):
    __tablename__ = 'cashiers'

    id = Column(BigInteger, ForeignKey('employees.id'), primary_key=True)
    skills = Column(String(100))

    bills = relationship('Bill', backref='cashier', lazy=True)


class Nurse(db.Model):
    __tablename__ = 'nurses'

    id = Column(BigInteger, ForeignKey('employees.id'), primary_key=True)
    educational_attainment = Column(String(100), nullable=False)


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = Column(BigInteger, ForeignKey('employees.id'), primary_key=True)
    specialist = Column(String(100), nullable=False)
    years_of_experience = Column(Integer, nullable=False)

    medical_bills = relationship('MedicalBill', backref='doctor', lazy=True)


class Regulation(BaseModel):
    __tablename__ = 'regulations'

    regulation_name = Column(String(50), nullable=False, unique=True)
    regulation_code = Column(String(50), nullable=False, unique=True)
    description = Column(String(100))
    status = Column(Boolean, nullable=False, default=True)
    admin_id = Column(BigInteger, ForeignKey('administrators.id'), nullable=False)

    def __str__(self):
        return self.regulation_name


class Bill(BaseModel):
    __tablename__ = 'bills'

    medicine_money = Column(Double, nullable=False)
    pre_examination = Column(Double, nullable=False)
    total_price = Column(Double, nullable=False)
    examination_date = Column(DateTime, nullable=False)
    cashier_id = Column(BigInteger, ForeignKey('cashiers.id'), nullable=False)
    patient_id = Column(BigInteger, ForeignKey('patients.id'), nullable=False)
    medical_bill_id = Column(BigInteger, ForeignKey('medical_bills.id'), nullable=False, unique=True)


class ExaminationList(BaseModel):
    __tablename__ = 'examination_list'

    examination_date = Column(DateTime, nullable=False)
    nurse_id = Column(BigInteger, ForeignKey('nurses.id'), nullable=False)

    examination_schedule_list = relationship('ExaminationSchedule', backref='examination_list', lazy=True)


class ExaminationSchedule(BaseModel):
    __tablename__ = 'examination_schedule'

    dob = Column(DateTime, nullable=False)
    status = Column(Boolean, default=False)
    email = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)
    address = Column(String(100), nullable=False)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    phone_number = Column(String(11), nullable=False)
    examination_date = Column(DateTime, nullable=False)
    examination_list_id = Column(BigInteger, ForeignKey('examination_list.id'))
    patient_id = Column(BigInteger, ForeignKey('patients.id', ondelete='CASCADE'))


class Medicine(BaseModel):
    __tablename__ = 'medicines'

    medicine_name = Column(String(20), nullable=False, unique=True)
    description = Column(String(100))
    slug = Column(String(50), nullable=False)
    price = Column(Double, nullable=False, default=0)
    amount = Column(Integer, default=0)
    image = Column(String(255))
    direction_for_use = Column(String(100))
    medicine_type_id = Column(BigInteger, ForeignKey('medicine_type.id'), nullable=False)
    medicine_unit_id = Column(BigInteger, ForeignKey('medicine_unit.id'), nullable=False)

    medical_bills = relationship('Prescription', backref='medicines', lazy=True)

    def __str__(self):
        return self.medicine_name

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)


event.listen(Medicine.medicine_name, 'set', Medicine.slugify, retval=False)


class MedicineType(BaseModel):
    __tablename__ = 'medicine_type'

    type_of_medicine = Column(String(20), nullable=False, unique=True)

    medicines = relationship('Medicine', backref='medicine_type', lazy=True)

    def __str__(self):
        return self.type_of_medicine


class MedicineUnit(BaseModel):
    __tablename__ = 'medicine_unit'

    unit_name = Column(String(20), nullable=False, unique=True)

    medicines = relationship('Medicine', backref='medicine_unit', lazy=True)

    def __str__(self):
        return self.unit_name


class MedicalBill(BaseModel):
    __tablename__ = 'medical_bills'

    symptoms = Column(String(100))
    diagnostic = Column(String(100))
    is_pay = Column(Boolean, default=False)
    examination_date = Column(DateTime, nullable=False)
    patient_id = Column(BigInteger, ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey('doctors.id'), nullable=False)
    packages_id = Column(BigInteger, ForeignKey('packages.id'), nullable=False)

    bill = relationship('Bill', backref='medical_bill', lazy=True, uselist=False)
    medicines = relationship('Prescription', backref='medical_bills', lazy=True)


class Prescription(BaseModel):
    __tablename__ = 'prescriptions'

    note = Column(String(100))
    amount = Column(Integer, nullable=False)
    medicine_id = Column(BigInteger, ForeignKey('medicines.id'), primary_key=True)
    medical_bill_id = Column(BigInteger, ForeignKey('medical_bills.id'), primary_key=True)


class Packages(BaseModel):
    __tablename__ = 'packages'

    packages_name = Column(String(20), nullable=False, unique=True)
    price = Column(Double, nullable=False, default=0)
    slug = Column(String(50), nullable=False)

    medical_bills = relationship('MedicalBill', backref='packages', lazy=True)

    def __str__(self):
        return self.packages_name

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)


event.listen(Packages.packages_name, 'set', Packages.slugify, retval=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
