import django_rq
from .models import Seat


def release_reserved_seats(seat_ids):
    seats = Seat.objects.filter(id__in=seat_ids, status='reserved')
    seats.update(status='available')


def delete_session_seats(session_key):
    from django.contrib.sessions.models import Session

    try:
        session = Session.objects.get(session_key=session_key)
        session_data = session.get_decoded()
        if 'selected_seat_ids' in session_data:
            del session_data['selected_seat_ids']
            session.session_data = Session.objects.encode(session_data)
            session.save()
    except Session.DoesNotExist:
        pass
