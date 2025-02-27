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
