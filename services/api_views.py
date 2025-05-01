from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from accounts.models import User
from .models import Spectacle, Seat, Ticket, Hall, ColumnSeats
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from .serializers import (
    SeatPublicSerializer, TicketDetailSerializer, TicketCreateSerializer,
    SeatUpdateSerializer, HallSerializer, ColumnSeatsSerializer, UserSerializer, SpectacleSerializer
)

@api_view(['GET'])
def get_spectacle_seats(request, id):
    spectacle = get_object_or_404(Spectacle, id=id)
    hall = spectacle.hall
    columns = hall.columns.prefetch_related('seats').all()
    seats = Seat.objects.filter(column__in=columns)
    serializer = SeatPublicSerializer(seats, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    serializer = TicketDetailSerializer(ticket)
    return Response(serializer.data)

@api_view(['GET'])
def all_tickets(request):
    tickets = Ticket.objects.select_related('spectacle', 'user').prefetch_related('seat')
    serializer = TicketDetailSerializer(tickets, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_ticket(request):
    serializer = TicketCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    ticket.delete()
    return Response({'success': 'Ticket deleted'})

@api_view(['PATCH'])
def update_seat_status(request, id):
    seat = get_object_or_404(Seat, id=id)
    serializer = SeatUpdateSerializer(seat, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def all_halls(request):
    halls = Hall.objects.all()
    serializer = HallSerializer(halls, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def hall_columns(request, hall_id):
    columns = ColumnSeats.objects.filter(hall_id=hall_id)
    serializer = ColumnSeatsSerializer(columns, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def spectacles_by_date(request):
    date = request.GET.get('date')
    spectacles = Spectacle.objects.filter(datetime_passing__date=date)
    serializer = SpectacleSerializer(spectacles, many=True)
    return Response(serializer.data)