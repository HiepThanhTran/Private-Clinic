import hashlib

import cloudinary.uploader
from sqlalchemy import func

from private_clinic.app import db
from private_clinic.models import Account, User, Patient, Employee, Administrator, Cashier, Nurse, Doctor, ExaminationSchedule, \
    ExaminationList, MedicalBill, AccountRoleEnum, MedicineType, MedicineUnit, Medicine, Packages, Prescription, Bill


def authenticate(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        print(password)

        return Account.query.filter(Account.username.__eq__(username.strip()), Account.password.__eq__(password)).first()


def check_examination_schedule_by_time(time):
    return db.session.query(ExaminationSchedule.query.filter(func.TIME(ExaminationSchedule.examination_date) == time).exists()).scalar()


def check_duplicate_email(email, current_user_id):
    return db.session.query(User.query.filter(User.id != current_user_id, User.email == email).exists()).scalar()


def check_duplicate_phone_number(phone_number, current_user_id):
    return db.session.query(User.query.filter(User.id != current_user_id, User.phone_number == phone_number).exists()).scalar()


def check_duplicate_insurance_id(insurance_id, current_user_id):
    return db.session.query(Patient.query.filter(Patient.id != current_user_id, Patient.insurance_id == insurance_id).exists()).scalar()


def count_examination_schedule_by_date(date):
    return ExaminationSchedule.query.filter(func.DATE(ExaminationSchedule.examination_date) == date).count()


def count_medicines_sold():
    return db.session.query(func.sum(Prescription.amount).label('total_amount')).all()


def count_revenue():
    return db.session.query(func.sum(Bill.total_price).label('total_revenue')).all()


def stats_medicine_per_month():
    return db.session.query(func.extract('month', Bill.examination_date).label('month'),
                            func.sum(Prescription.amount).label('total_amount')) \
        .join(Prescription, Prescription.medical_bill_id == Bill.medical_bill_id) \
        .join(MedicalBill, Bill.medical_bill_id == MedicalBill.id) \
        .group_by(func.extract('month', Bill.examination_date)).all()


def stats_medicine_usage_per_month(month=None, medicine_name=None):
    result = db.session.query(func.extract('month', Bill.examination_date).label('month'),
                              Medicine.medicine_name,
                              MedicineUnit.unit_name,
                              Medicine.amount,
                              func.sum(Prescription.amount).label('usage_count')) \
        .select_from(Medicine) \
        .join(Prescription, Prescription.medicine_id == Medicine.id, isouter=True) \
        .join(MedicalBill, MedicalBill.id == Prescription.medical_bill_id, isouter=True) \
        .join(Bill, Bill.medical_bill_id == MedicalBill.id, isouter=True) \
        .join(MedicineUnit, MedicineUnit.id == Medicine.medicine_unit_id, isouter=True) \
        .group_by(func.extract('month', Bill.examination_date).label('month'), Medicine.medicine_name)

    if month:
        result = result.filter(func.extract('month', Bill.examination_date).label('month') == month)

    if medicine_name:
        result = result.filter(Medicine.medicine_name.contains(medicine_name))

    return result.all()


def stats_revenue_per_month(month=None):
    result = db.session.query(func.extract('month', Bill.examination_date).label('month'), func.sum(Bill.total_price).label('total_revenue')) \
        .group_by(func.extract('month', Bill.examination_date))

    if month:
        result = result.filter(func.extract('month', Bill.examination_date).label('month') == month)

    return result.all()


def stats_examination_per_month():
    return db.session.query(ExaminationList.examination_date, func.count(Patient.id).label('total_examinations'), func.sum(Bill.total_price).label('revenue')) \
        .select_from(ExaminationList) \
        .join(ExaminationSchedule, ExaminationSchedule.examination_list_id == ExaminationList.id) \
        .join(Patient, ExaminationSchedule.patient_id == Patient.id) \
        .join(Bill, Bill.patient_id == Patient.id) \
        .group_by(ExaminationList.examination_date).all()


def create_account(username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    account = Account(username=username.strip(), password=password)

    for field_name, field_value in kwargs.items():
        if field_value:
            setattr(account, field_name, field_value)

    db.session.add(account)
    db.session.commit()

    return account


def create_user(first_name, last_name, email, account_id):
    user = User(first_name=first_name.strip(), last_name=last_name.strip(), email=email.strip(), account_id=account_id)

    db.session.add(user)
    db.session.commit()

    return user


def create_patient(patient_id):
    patient = Patient(id=patient_id)

    db.session.add(patient)
    db.session.commit()

    return patient


def create_employee(employee_id):
    employee = Employee(id=employee_id)

    db.session.add(employee)
    db.session.commit()

    return employee


def create_administrator(administrator_id, inauguration_day):
    administrator = Administrator(id=administrator_id, inauguration_day=inauguration_day)

    db.session.add(administrator)
    db.session.commit()

    return administrator


def create_cashier(cashier_id):
    cashier = Cashier(id=cashier_id)

    db.session.add(cashier)
    db.session.commit()

    return cashier


def create_nurse(nurse_id, educational_attainment):
    nurse = Nurse(id=nurse_id, educational_attainment=educational_attainment)

    db.session.add(nurse)
    db.session.commit()

    return nurse


def create_doctor(doctor_id, specialist, years_of_experience):
    doctor = Doctor(id=doctor_id, specialist=specialist, years_of_experience=years_of_experience)

    db.session.add(doctor)
    db.session.commit()

    return doctor


def create_examination_schedule(patient_id, examination_date, **kwargs):
    examination_schedule = ExaminationSchedule(
        first_name=kwargs['first_name'].strip(),
        last_name=kwargs['last_name'].strip(),
        gender=kwargs['gender'].strip(),
        dob=kwargs['dob'],
        address=kwargs['address'].strip(),
        email=kwargs['email'].strip(),
        phone_number=kwargs['phone_number'].strip(),
        patient_id=patient_id,
        examination_date=examination_date)

    db.session.add(examination_schedule)
    db.session.commit()

    return examination_schedule


def create_examination_list(examination_date, nurse_id, examination_schedule_id_list):
    examination_list = ExaminationList(examination_date=examination_date, nurse_id=nurse_id)

    db.session.add(examination_list)
    db.session.commit()

    for examination_schedule_id in examination_schedule_id_list:
        update_examination_schedule(int(examination_schedule_id), status=True, examination_list_id=examination_list.id)

    return examination_list


def create_medicine(**kwargs):
    medicine = Medicine()

    for field_name, field_value in kwargs.items():
        if field_value:
            if field_name == 'image':
                field_value = cloudinary.uploader.upload(field_value)['secure_url']
            setattr(medicine, field_name, field_value)

    db.session.add(medicine)
    db.session.commit()

    return medicine


def create_medical_bill(symptoms, diagnostic, examination_date, patient_id, doctor_id, packages_id, amount, medicine_id_list):
    medical_bill = MedicalBill(
        symptoms=symptoms,
        diagnostic=diagnostic,
        examination_date=examination_date,
        patient_id=patient_id,
        doctor_id=doctor_id,
        packages_id=packages_id)

    db.session.add(medical_bill)
    db.session.commit()

    for i in range(0, len(amount)):
        create_prescription(amount=amount[i], medicine_id=medicine_id_list[i], medical_bill_id=medical_bill.id)

    return medical_bill


def create_prescription(amount, medicine_id, medical_bill_id):
    prescription = Prescription(amount=amount, medicine_id=medicine_id, medical_bill_id=medical_bill_id)

    db.session.add(prescription)
    db.session.commit()

    return prescription


def create_bill(patient_id, examination_date, pre_examination, medicine_money, total_price, medical_bill_id, cashier_id):
    bill = Bill(
        patient_id=patient_id,
        examination_date=examination_date,
        pre_examination=pre_examination,
        medicine_money=medicine_money,
        total_price=total_price,
        medical_bill_id=medical_bill_id,
        cashier_id=cashier_id
    )

    medical_bill = MedicalBill.query.get(medical_bill_id)
    medical_bill.is_pay = True

    db.session.add(bill)
    db.session.commit()

    return bill


def update_account_password(account_id, new_password):
    new_password = str(hashlib.md5(new_password.strip().encode('utf-8')).hexdigest())

    account = Account.query.get(account_id)
    account.password = new_password
    db.session.commit()

    return account


def update_profile_user(user_id, **kwargs):
    user = User.query.get(user_id)

    for field_name, field_value in kwargs.items():
        if field_value:
            if field_name == 'insurance_id':
                user.patient.insurance_id = field_value
            elif field_name == 'avatar':
                user.account.avatar = cloudinary.uploader.upload(field_value)['secure_url']
            else:
                setattr(user, field_name, field_value)

    db.session.commit()
    return user


def update_examination_schedule(examination_schedule_id, **kwargs):
    examination_schedule = ExaminationSchedule.query.get(examination_schedule_id)

    for field_name, field_value in kwargs.items():
        if field_value:
            setattr(examination_schedule, field_name, field_value)

    db.session.commit()
    return examination_schedule


def get_role_list():
    return [role for role in AccountRoleEnum]


def get_medicine_type_list():
    return MedicineType.query.all()


def get_medicine_unit_list():
    return MedicineUnit.query.all()


def get_packages_list():
    return Packages.query.all()


def get_bill_list():
    return Bill.query.all()


def get_examination_schedules_list():
    return ExaminationSchedule.query.order_by(ExaminationSchedule.id.asc()).all()


def get_examination_schedules_list_sort_by_created_date():
    return ExaminationSchedule.query.order_by(ExaminationSchedule.created_date.desc()).all()


def get_medical_bills_list():
    return MedicalBill.query.order_by(MedicalBill.id.asc()).all()


def get_medicines_list():
    return Medicine.query.filter(Medicine.amount > 0).order_by(Medicine.medicine_name.asc()).all()


def get_patients_list():
    return (Patient.query.join(User, Patient.id == User.id)
            .join(Account, Account.id == User.account_id)
            .filter(Account.confirmed_on.is_(True), Account.active.is_(True))
            .order_by(Patient.id.asc()).all())


def get_details_bill():
    return db.session.query(
        Medicine.id,
        Medicine.medicine_name,
        MedicineUnit.unit_name,
        Medicine.direction_for_use,
        Prescription.amount,
        Prescription.medical_bill_id,
        Medicine.price.label('medicine_price'),
        Packages.price.label('package_price')) \
        .join(Prescription, Prescription.medicine_id == Medicine.id) \
        .join(MedicineUnit, MedicineUnit.id == Medicine.medicine_unit_id) \
        .join(MedicalBill, MedicalBill.id == Prescription.medical_bill_id) \
        .join(Packages, Packages.id == MedicalBill.packages_id).all()


def get_examination_schedules_list_by_date(date):
    return ExaminationSchedule.query.filter(func.DATE(ExaminationSchedule.examination_date) == date,
                                            ExaminationSchedule.status.is_(False)).all()


def get_account_by_id(account_id):
    return Account.query.get(account_id)


def get_account_by_username(username):
    return Account.query.filter_by(username=username).first()


def get_account_by_email(email):
    return Account.query.join(User).filter_by(email=email).first()


def get_account_by_phone_number(phone_number):
    return Account.query.join(User).filter_by(phone_number=phone_number).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
