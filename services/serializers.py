from rest_framework import serializers
from django.utils.timezone import now
from accounts.models import User
from .models import Spectacle, Seat, Ticket, Hall, ColumnSeats


class SeatPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'row', 'number', 'status', 'column']


class SeatUpdateSerializer(serializers.ModelSerializer):
    def validate_status(self, value):
        from .models import SeatStatus
        if value not in [choice[0] for choice in SeatStatus.choices()]:
            raise serializers.ValidationError("Invalid seat status.")
        return value

    class Meta:
        model = Seat
        fields = ['status']


class TicketDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'seat', 'spectacle', 'price']


class TicketCreateSerializer(serializers.ModelSerializer):
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate(self, data):
        if data['seat'].status != 'available':
            raise serializers.ValidationError("Seat must be available to book a ticket.")
        return data

    class Meta:
        model = Ticket
        fields = '__all__'


class HallSerializer(serializers.ModelSerializer):
    def validate_number_hall(self, value):
        if not (1 <= value <= 6):
            raise serializers.ValidationError("Hall number must be between 1 and 6.")
        return value

    class Meta:
        model = Hall
        fields = '__all__'


class ColumnSeatsSerializer(serializers.ModelSerializer):
    def validate_number_column(self, value):
        if value <= 0:
            raise serializers.ValidationError("Column number must be positive.")
        return value

    class Meta:
        model = ColumnSeats
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        if value and not value.endswith("@gmail.com"):
            raise serializers.ValidationError("Only Gmail addresses are allowed.")
        return value

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'email', 'is_staff', 'is_active', 'date_joined']


class SpectacleSerializer(serializers.ModelSerializer):
    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be positive.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_datetime_passing(self, value):
        if value <= now():
            raise serializers.ValidationError("Spectacle time must be in the future.")
        return value

    def validate_age_limit(self, value):
        if not (0 <= value <= 100):
            raise serializers.ValidationError("Age limit must be between 0 and 100.")
        return value

    class Meta:
        model = Spectacle
        fields = '__all__'
