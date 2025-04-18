from rest_framework import serializers

from accounts.models import User
from .models import Spectacle, Seat, Ticket, Hall, ColumnSeats


class SeatPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'row', 'number', 'status', 'column']

class TicketDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'seat', 'spectacle', 'price']

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class SeatUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['status']

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

class ColumnSeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnSeats
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'email', 'is_staff', 'is_active', 'date_joined']

class SpectacleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spectacle
        fields = '__all__'
