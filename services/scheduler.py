import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from django_apscheduler.jobstores import DjangoJobStore


def start_scheduler():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theater.settings')
    import django
    django.setup()

    from services.models import Seat

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')
    scheduler.add_executor(ThreadPoolExecutor(20), 'default')
    scheduler.start()

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

    scheduler.release_reserved_seats = release_reserved_seats
    scheduler.delete_session_seats = delete_session_seats

    return scheduler
