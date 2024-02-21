from django.contrib import admin
from auto_track_log.models import *

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'num', 'year_of_release', 'colour', 'engine_power', 'fuel_rate', 'mileage']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['login', 'password', 'name', 'surname', 'role']

@admin.register(CostCalculation)
class CostCalculationAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'maintenance_costs', 'fuel_costs']

@admin.register(ServiceSchedule)
class ServiceScheduleAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'start_date', 'end_date', 'work_scope']