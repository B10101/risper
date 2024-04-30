# urls.py in items app
from django.urls import path
from . import views
from .views import AdminEquipmentListView
from .views import AddEquipmentView
from .views import UpdateEquipmentView
from .views import InventoryReportView
from .views import AddItemView
from .views import home
from .views import ItemCancelReservationView
from .views import ItemReserveFromHistoryView








app_name = "item"
urlpatterns = [
    path('', home, name='home'),
    path('index/', views.ListAndCreate.as_view(), name='index'),
    path('create/', views.ListAndCreate.as_view(), name='create'),
    path('delete-item/<pk>/', views.ItemDeleteView.as_view(), name='delete'),
    path('item/<pk>/', views.ListAndDetail.as_view(), name='details'),
    path('search/', views.ItemSearchView.as_view(), name='search'),  # Add this line for search functionality
    # path('reserve/<pk>/', views.ReserveItemView.as_view(), name='reserve'),  #for reserving items
    path('reserve/<pk>/', views.ItemReservationView.as_view(), name='reserve'),  #for reserving items
    path('admin/equipment/', AdminEquipmentListView.as_view(), name='admin_equipment_list'),
    path('admin/add/', AddEquipmentView.as_view(), name='add_equipment'),
    path('admin/update/<int:pk>/', UpdateEquipmentView.as_view(), name='update_equipment'),
    path('inventory/report/', InventoryReportView.as_view(), name='inventory_report'),
    path('add/', AddItemView.as_view(), name='add_item'),
    path('cancel-reservation/<pk>/', ItemCancelReservationView.as_view(), name='cancel_reservation'),
    path('reserve-from-history/<pk>/', ItemReserveFromHistoryView.as_view(), name='reserve_from_history'),

    
]


