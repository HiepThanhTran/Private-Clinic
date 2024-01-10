from datetime import datetime

from flask import request
from flask_admin import AdminIndexView, expose, Admin, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from private_clinic import services
from private_clinic.app import app, db
from private_clinic.models import (AccountRoleEnum, Account, User, Regulation, ExaminationList, Medicine, MedicineType, MedicineUnit,
                                   Packages)


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render(template='admin/index.html',
                           total_revenues=services.count_revenue(),
                           revenue_stats=services.stats_revenue_per_month(),
                           total_medicines=services.count_medicines_sold(),
                           medicine_stats=services.stats_medicine_per_month(),
                           examination_schedules=services.get_examination_schedules_list_sort_by_created_date())


class AuthenticatedAdmin(ModelView):
    create_modal = True
    edit_modal = True
    details_modal = True
    can_edit = True
    can_create = True
    can_delete = True
    can_export = True
    can_view_details = True
    can_set_page_size = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == AccountRoleEnum.ADMIN


class MyAnalyticsView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/analytics.html',
                           revenue_stats=services.stats_revenue_per_month(),
                           examination_stats=services.stats_examination_per_month(),
                           medicine_stats=services.stats_medicine_usage_per_month(month=datetime.now().month))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == AccountRoleEnum.ADMIN


class AccountView(AuthenticatedAdmin):
    column_list = ['id', 'username', 'slug', 'role']
    column_searchable_list = ['username']
    column_sortable_list = ['id']
    column_export_exclude_list = ['password', 'avatar']


class UserView(AuthenticatedAdmin):
    column_list = ['id', 'gender', 'dob', 'account_id']
    column_searchable_list = ['first_name', 'last_name', 'email']
    column_sortable_list = ['id', 'first_name', 'last_name']
    column_export_exclude_list = ['account_id']


class RegulationView(AuthenticatedAdmin):
    column_list = ['id', 'regulation_name', 'regulation_code', 'status']
    column_searchable_list = ['regulation_name', 'regulation_code']
    column_sortable_list = ['id', 'regulation_name', 'regulation_code']


class ExaminationListView(AuthenticatedAdmin):
    column_list = ['id', 'examination_date', 'nurse_id']
    column_sortable_list = ['id', 'examination_date']


class MedicineView(AuthenticatedAdmin):
    column_list = ['id', 'medicine_name', 'price', 'amount', 'medicine_type_id', 'medicine_unit_id']
    column_searchable_list = ['medicine_name']
    column_sortable_list = ['id', 'medicine_name', 'price', 'amount']
    column_filters = ['price', 'amount', 'medicine_type_id', 'medicine_unit_id']

    create_modal_template = '/admin/model/modals/create_modal_medicine.html'

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        self._template_args['medicine_type_list'] = services.get_medicine_type_list()
        self._template_args['medicine_unit_list'] = services.get_medicine_unit_list()
        return super(MedicineView, self).create_view()


class MedicineTypeView(AuthenticatedAdmin):
    column_list = ['id', 'type_of_medicine']
    column_searchable_list = ['type_of_medicine']
    column_sortable_list = ['id', 'type_of_medicine']


class MedicineUnitView(AuthenticatedAdmin):
    column_list = ['id', 'unit_name']
    column_searchable_list = ['unit_name']
    column_sortable_list = ['id', 'unit_name']


class PackagesView(AuthenticatedAdmin):
    column_list = ['id', 'packages_name', 'price']
    column_searchable_list = ['packages_name']
    column_sortable_list = ['id', 'packages_name', 'price']
    column_filters = ['price']


admin = Admin(app=app, template_mode='bootstrap4', index_view=MyAdminView())

admin.add_view(MyAnalyticsView(name='Analytics', url='/admin/analytics', endpoint='analytics'))
admin.add_view(AccountView(Account, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(ExaminationListView(ExaminationList, db.session))
admin.add_view(MedicineView(Medicine, db.session))
admin.add_view(MedicineTypeView(MedicineType, db.session))
admin.add_view(MedicineUnitView(MedicineUnit, db.session))
admin.add_view(PackagesView(Packages, db.session))
admin.add_view(RegulationView(Regulation, db.session))
