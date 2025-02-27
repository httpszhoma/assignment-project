from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

User = get_user_model()


@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data['phone_number']
            password = data['password']
            email = data['email']

            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'error': 'Phone number already exists'}, status=400)

            user = User.objects.create(
                phone_number=phone_number,
                password=make_password(password),
                email=email
            )
            return JsonResponse({'message': 'User created successfully'}, status=201)
        except KeyError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data['phone_number']
            password = data['password']

            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid phone number or password'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def logout_view(request):
    logout(request)
    next_page = request.GET.get('next', '/')
    return redirect(next_page)
