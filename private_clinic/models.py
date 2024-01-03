from app import db, app
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as DbEnum
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, Boolean, Enum, DateTime, ForeignKey, BigInteger, Double, Integer


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
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    avatar = Column(String(100))
    role = Column(Enum(AccountRoleEnum), default=AccountRoleEnum.PATIENT, nullable=False)

    user = relationship('User', backref='account', lazy=True, uselist=False)

    def __str__(self):
        return self.userame


class User(BaseModel):
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(String(10), default='OTHER', nullable=False)
    dob = Column(DateTime, nullable=False)
    address = Column(String(100))
    phone_number = Column(String(11), nullable=False)
    email = Column(String(50))
    account_id = Column(BigInteger, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False, unique=True)

    patient = relationship('Patient', backref='user', lazy=True, uselist=False)
    employee = relationship('Employee', backref='user', lazy=True, uselist=False)

    @property
    def get_full_name(self):
        return self.last_name + self.first_name

    def __str__(self):
        return self.get_full_name


class Patient(db.Model):
    __tablename__ = 'patients'

    id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    insurance_id = Column(String(20), nullable=False, unique=True)

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


class Cashier(Employee):
    __tablename__ = 'cashiers'

    id = Column(BigInteger, ForeignKey('employees.id'), primary_key=True)
    skills = Column(String(100))

    bills = relationship('Bill', backref='cashier', lazy=True)


class Nurse(Employee):
    __tablename__ = 'nurses'

    id = Column(BigInteger, ForeignKey('employees.id'), primary_key=True)
    educational_attainment = Column(String(100), nullable=False)


class Doctor(Employee):
    __tablename__ = 'doctors'

    id = Column(BigInteger, ForeignKey('employees.id'), primary_key=True)
    specialist = Column(String(100), nullable=False)
    years_of_experience = Column(Integer, nullable=False)

    medical_bills = relationship('MedicalBill', backref='doctor', lazy=True)
    examination_schedule_list = relationship('ExaminationSchedule', backref='doctor', lazy=True)


class Regulation(BaseModel):
    __tablename__ = 'regulations'

    regulation_name = Column(String(50), nullable=False, unique=True)
    description = Column(String(100))
    note = Column(String(100))
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

    examination_date = Column(DateTime, nullable=False, default=datetime.now())
    nurse_id = Column(BigInteger, ForeignKey('nurses.id'), nullable=False)

    examination_schedule_list = relationship('ExaminationSchedule', backref='examination_list', lazy=True)


class ExaminationSchedule(BaseModel):
    __tablename__ = 'examination_schedule'

    note = Column(String(100))
    patient_id = Column(BigInteger, ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey('doctors.id'), nullable=False)
    examination_list_id = Column(BigInteger, ForeignKey('examination_list.id'), nullable=False)


medicine_types = db.Table('medicine_types',
                          Column('medicine_id', BigInteger, ForeignKey('medicines.id'), primary_key=True),
                          Column('medicine_type_id', BigInteger, ForeignKey('medicine_type.id'), primary_key=True))


class Medicine(BaseModel):
    __tablename__ = 'medicines'

    medicine_name = Column(String(20), nullable=False, unique=True)
    description = Column(String(100))
    note = Column(String(100))
    price = Column(Double, nullable=False, default=0)
    amount = Column(Integer, default=0)
    image = Column(String(100))
    direction_for_use = Column(String(100))
    medicine_unit_id = Column(BigInteger, ForeignKey('medicine_unit.id'), nullable=False)

    medicine_types = relationship('MedicineType', secondary='medicine_types', lazy='subquery', backref=backref('medicines', lazy=True))
    medical_bills = relationship('MedicalBill', backref='medicines', lazy=True)

    def __str__(self):
        return self.medicine_name


class MedicineType(BaseModel):
    __tablename__ = 'medicine_type'

    type_of_medicine = Column(String(20), nullable=False, unique=True)

    def __str__(self):
        return self.type_of_medicine


class MedicineUnit(BaseModel):
    __tablename__ = 'medicine_unit'

    unit_name = Column(String(20), nullable=False, unique=True)

    medicines = relationship('Medicine', backref='medicine_unit', lazy=True)

    def __str__(self):
        return self.unit_name


medicalbill_packages = db.Table('medicalbill_packages',
                                Column('medical_bill_id', BigInteger, ForeignKey('medical_bills.id'), primary_key=True),
                                Column('packages_id', BigInteger, ForeignKey('packages.id'), primary_key=True))


class MedicalBill(BaseModel):
    __tablename__ = 'medical_bills'

    diagnostic = Column(String(100))
    symptoms = Column(String(100))
    examination_date = Column(DateTime, nullable=False)
    patient_id = Column(BigInteger, ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey('doctors.id'), nullable=False)

    packages = relationship('Packages', secondary='medicalbill_packages', lazy='subquery', backref=backref('medical_bills', lazy=True))
    bill = relationship('Bill', backref='medical_bill', lazy=True, uselist=False)
    medicines = relationship('Prescription', backref='medical_bills', lazy=True)


class Prescription(BaseModel):
    __tablename__ = 'prescriptions'

    amount = Column(Integer, nullable=False)
    note = Column(String(100))
    medicine_id = Column(BigInteger, ForeignKey('medicines.id'), primary_key=True)
    medical_bill_id = Column(BigInteger, ForeignKey('medical_bills.id'), primary_key=True)


class Packages(BaseModel):
    __tablename__ = 'packages'

    packages_name = Column(String(20), nullable=False, unique=True)
    price = Column(Double, nullable=False, default=0)

    def __str__(self):
        return self.packages_name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
