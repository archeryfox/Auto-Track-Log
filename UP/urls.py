"""
URL configuration for UP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from auto_track_log import views
from auto_track_log.views import *

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('registration/', registration_view, name='registration_url'),
    path('', login_view, name='login_url'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('vehicle/create/', VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicle/<int:pk>/update/', VehicleUpdateView.as_view(), name='vehicle_update'),
    path('vehicle/<int:pk>/delete/', VehicleDeleteView.as_view(), name='vehicle_delete'),
    path('vehicle/<int:pk>/', VehicleDetailView.as_view(), name='vehicle_detail'),
    path('admin/vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('admin/cost_calculations/', CostCalculationListView.as_view(), name='cost-calculation-list'),
    path('admin/service_schedules/', ServiceScheduleListView.as_view(), name='service-schedule-list'),
    path('a/', admin.site.urls),
    path('detail/<int:user_id>/', views.user_detail, name='user_detail'),
    path('create/', views.user_create, name='user_create'),
    path('update/<int:user_id>/', views.user_update, name='user_update'),
    path('delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('cost_calculations/<int:pk>/', CostCalculationDeleteView.as_view(), name='cost-calculation-detail'),
    path('cost_calculations/create/', CostCalculationCreateView.as_view(), name='cost-calculation-create'),
    path('cost_calculations/update/<int:pk>/', CostCalculationUpdateView.as_view(), name='cost-calculation-update'),
    path('cost_calculations/delete/<int:pk>/', CostCalculationDeleteView.as_view(), name='cost-calculation-delete'),
    path('service-schedule/<int:pk>/', ServiceScheduleDetailView.as_view(), name='service-schedule-detail'),
    path('service-schedule/create/', ServiceScheduleCreateView.as_view(), name='service-schedule-create'),
    path('service-schedule/<int:pk>/update/', ServiceScheduleUpdateView.as_view(), name='service-schedule-update'),
    path('service-schedule/<int:pk>/delete/', ServiceScheduleDeleteView.as_view(), name='service-schedule-delete'),

]
