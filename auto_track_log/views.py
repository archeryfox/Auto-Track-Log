import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm, UserForm
from .models import Vehicle, User, CostCalculation, ServiceSchedule, Role


def base(request):
    return render(request, 'base.html')

def user_dashboard(request):
    allowed_pages = request.session.get('allowed_pages', [])

    return render(request, 'user_dashboard.html', {'allowed_pages': allowed_pages})

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            password = form.cleaned_data['password']
            try:
                role = Role.objects.filter(name='user').first()
                if role is None:
                    role = Role.objects.create(name='user', description='Default User Role')
            except Role.DoesNotExist:
                # Обработка случая, когда роль не существует
                return render(request, 'registration.html', {'form': form, 'error_message': 'Role does not exist'})
            user = User.objects.create(login=login, name=name, surname=surname, password=password, role=role)
            request.session['allowed_pages'] = ['vehicle-list', 'cost-calculation-list', 'service-schedule-list']
            request.session['role'] = role.name
            return render(request, 'user_dashboard.html', context={'role':user.role.name, 'user': user})
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = get_object_or_404(User, login=username, password=password)
            if user is not None:
                # Save allowed pages to session
                request.session['allowed_pages'] = ['vehicle-list', 'cost-calculation-list', 'service-schedule-list']

                allowed_pages = request.session.get('allowed_pages', [])
                return render(request, 'user_dashboard.html', context={'role':user.role.name, 'allowed_pages': allowed_pages, 'user': user})
            else:
                return redirect('login_url')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



class VehicleListView(TemplateView):
    template_name = r'vehicle_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.all()  # Получаем все транспортные средства из базы данных
        return context


class CostCalculationListView(TemplateView):
    model = CostCalculation
    template_name = 'cost_calculation_list.html'  # Имя вашего HTML-шаблона для списка расчетов затрат
    context_object_name = 'cost_calculations'  # Имя переменной контекста в шаблоне
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cost_calculations'] = CostCalculation.objects.all()  # Получаем все транспортные средства из базы данных
        return context

class ServiceScheduleListView(TemplateView):
    model = ServiceSchedule
    template_name = 'service_schedule_list.html'  # Имя вашего HTML-шаблона для списка графиков обслуживания
    context_object_name = 'service_schedules'  # Имя переменной контекста в шаблоне


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_detail(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'user_detail.html', {'user': user})

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

def user_update(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

def user_delete(request, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect('user_list')

class VehicleCreateView(CreateView):
    model = Vehicle
    template_name = 'vehicle_form.html'
    fields = ['brand', 'model', 'num', 'year_of_release', 'colour', 'engine_power', 'fuel_rate', 'mileage']
    success_url = reverse_lazy('vehicle_list')


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicle_detail.html'  # имя вашего шаблона для деталей
    context_object_name = 'vehicle'  # имя объекта, который будет передан в шаблон

class VehicleUpdateView(UpdateView):
    model = Vehicle
    fields = ['brand', 'model', 'num', 'year_of_release', 'colour', 'engine_power', 'fuel_rate', 'mileage']
    success_url = reverse_lazy('vehicle_list')

class VehicleDeleteView(DeleteView):
    model = Vehicle

    success_url = reverse_lazy('vehicle_list')

class CostCalculationDetailView(DetailView):
    model = CostCalculation
    template_name = 'cost_calculation_detail.html'
    context_object_name = 'cost_calculation'

class CostCalculationCreateView(CreateView):
    model = CostCalculation
    template_name = 'cost_calculation_form.html'
    fields = ['vehicle', 'maintenance_costs', 'fuel_costs']
    success_url = reverse_lazy('cost-calculation-list')

class CostCalculationUpdateView(UpdateView):
    model = CostCalculation
    template_name = 'cost_calculation_form.html'
    fields = ['vehicle', 'maintenance_costs', 'fuel_costs']

class CostCalculationDeleteView(DeleteView):
    model = CostCalculation
    template_name = 'cost_calculation_confirm_delete.html'
    success_url = reverse_lazy('cost-calculation-list')


class ServiceScheduleDetailView(DetailView):
    model = ServiceSchedule
    template_name = 'service_schedule_detail.html'
    context_object_name = 'service_schedule'

class ServiceScheduleCreateView(CreateView):
    model = ServiceSchedule
    template_name = 'service_schedule_form.html'
    fields = ['vehicle', 'start_date', 'end_date', 'work_scope']

class ServiceScheduleUpdateView(UpdateView):
    model = ServiceSchedule
    template_name = 'service_schedule_form.html'
    fields = ['vehicle', 'start_date', 'end_date', 'work_scope']

class ServiceScheduleDeleteView(DeleteView):
    model = ServiceSchedule
    template_name = 'service_schedule_confirm_delete.html'
    success_url = reverse_lazy('service-schedule-list')
