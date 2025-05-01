from django.urls import path

from services import views

urlpatterns = [
    path('', views.index, name='home'),
    path('spectacles/', views.spectacles, name='spectacles'),
    path('details/<int:spectacle_id>/', views.spectacles_details, name='details'),
    path('buy-tickets/<int:spectacle_id>/', views.BuyTicketsView.as_view(), name='buy_tickets'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('my-tickets/', views.get_my_tickets, name='my_tickets')
]

from django.urls import path
from . import api_views
from django.urls import path, include

urlpatterns += [
    path('silk/', include('silk.urls', namespace='silk')),
    path('api/tickets/create/generic', views.create_ticket_generic, name='create_ticket_generic'),
    path('api/spectacles/<int:id>/seats/', api_views.get_spectacle_seats, name='api_spectacle_seats'),
    path('api/tickets/<int:id>/', api_views.ticket_detail, name='api_ticket_detail'),
    path('api/tickets/', api_views.all_tickets, name='api_all_tickets'),
    path('api/tickets/create/', api_views.create_ticket, name='api_create_ticket'),
    path('api/tickets/<int:id>/delete/', api_views.delete_ticket, name='api_delete_ticket'),
    path('api/seats/<int:id>/update/', api_views.update_seat_status, name='api_update_seat'),
    path('api/halls/', api_views.all_halls, name='api_all_halls'),
    path('api/halls/<int:hall_id>/columns/', api_views.hall_columns, name='api_hall_columns'),
    path('api/users/', api_views.all_users, name='api_all_users'),
    path('api/spectacles-by-date/', api_views.spectacles_by_date, name='api_spectacles_by_date'),
]
