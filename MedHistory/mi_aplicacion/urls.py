# mi_aplicacion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_view, name='create'),
    path('buscar/', views.buscar, name='buscar'),
    path('detalle/<int:id>/', views.detalle, name='detalle'),
    path('actualizar/<int:id>/', views.actualizar, name='actualizar'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
]
