import json
from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import View

from services.forms import SearchForm, PaymentForm
from services.models import Spectacle, Seat, Ticket
from services.scheduler import start_scheduler
from services.tasks import release_reserved_seats, delete_session_seats


def index(request):
    return render(request, 'services/home.html')


def spectacles(request):
    search_query = ''
    db_spectacles = Spectacle.objects.all()
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            title = search_form.cleaned_data['title']
            search_query = title
            db_spectacles = Spectacle.objects.filter(title__icontains=title)
    else:
        search_form = SearchForm()
    context = {'spectacles': db_spectacles,
               "search_form": search_form,
               "search_query": search_query}
    return render(request, 'services/spectacles.html', context)


def spectacles_details(request, spectacle_id):
    db_spectacle = Spectacle.objects.get(pk=spectacle_id)
    context = {'spectacle': db_spectacle}
    return render(request, 'services/detail.html', context)


class BuyTicketsView(View):
    @staticmethod
    def post(request, spectacle_id):
        spectacle = get_object_or_404(Spectacle, id=spectacle_id)
        try:
            data = json.loads(request.body)
            selected_seat_ids = data.get('selected_seats', [])
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if len(selected_seat_ids) > 5:
            return JsonResponse({'error': 'You can select a maximum of 5 tickets.'}, status=400)

        seats = Seat.objects.filter(id__in=selected_seat_ids, status='available')
        if seats.count() != len(selected_seat_ids):
            return JsonResponse({'error': 'Some seats are no longer available.'}, status=400)

        total_price = len(seats) * spectacle.price
        seats.update(status='reserved')

        scheduler = start_scheduler()

        request.session['selected_seat_ids'] = selected_seat_ids
        request.session['spectacle_id'] = spectacle_id
        request.session['total_price'] = str(total_price)

        job_id = f"release_reserved_seats_{datetime.now().timestamp()}"
        scheduler.add_job(release_reserved_seats, 'date', run_date=datetime.now() + timedelta(minutes=3),
                          args=[selected_seat_ids], id=job_id, replace_existing=True)

        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        scheduler.add_job(delete_session_seats, 'date', run_date=datetime.now() + timedelta(minutes=3),
                          args=[session_key], id=f"delete_session_seats_{session_key}", replace_existing=True)

        return JsonResponse({'success': 'Seats reserved. Proceed to payment.'})


class PaymentView(View):
    @staticmethod
    def get(request):
        if 'selected_seat_ids' not in request.session:
            return redirect('spectacles')

        form = PaymentForm()
        total_price = request.session.get('total_price')
        return render(request, 'services/payment.html', {'form': form, 'total_price': total_price})

    @staticmethod
    def post(request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            selected_seat_ids = request.session.get('selected_seat_ids')
            spectacle_id = request.session.get('spectacle_id')
            user = request.user

            tickets = []
            for seat_id in selected_seat_ids:
                seat = Seat.objects.get(id=seat_id)
                spectacle = Spectacle.objects.get(pk=spectacle_id)

                if Ticket.objects.filter(seat=seat, spectacle=spectacle).exists():
                    continue
                ticket = Ticket.objects.create(
                    seat=seat,
                    spectacle=spectacle,
                    price=spectacle.price,
                    user=user
                )
                seat.status = 'booked'
                seat.save()
                tickets.append(ticket)

            if tickets:
                subject = 'Your Ticket Confirmation'
                html_content = render_to_string('services/my_tickets.html', {'tickets': tickets, 'user': user})
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(subject, text_content, 'your-email@gmail.com', [user.email])
                email.attach_alternative(html_content, "text/html")

                # Прикрепление QR-кодов
                for ticket in tickets:
                    if ticket.qr_code:
                        email.attach_file(ticket.qr_code.path)

                email.send()

            del request.session['selected_seat_ids']
            del request.session['spectacle_id']
            del request.session['total_price']

            return redirect('my_tickets')
        return JsonResponse({'error': 'Payment failed. Please try again.'}, status=400)


@login_required
def get_my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'services/my_tickets.html', {'tickets': tickets})
