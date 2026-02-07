import json
import secrets
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import (
    Restaurant, Staff, Table, Reservation,
)
from .serializers import (
    RestaurantSerializer, StaffSerializer, TableSerializer, ReservationSerializer,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# --- ViewSets for all main models ---

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly] # Use this to secure endpoints


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


# Simulated Token Database (In real life, this would be a Model)
# Key: Token String, Value: Username
ACTIVE_TOKENS = {}

@csrf_exempt # This tells Django "Don't check for a CSRF token here"
def custom_login_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        time.sleep(2.5)  # Simulate processing delay
        # Dummy Check (Replace with real logic)
        if username == "admin" and password == "password123":
            # 1. Generate a random token
            token = secrets.token_hex(20)
            # 2. Store it in our "database"
            ACTIVE_TOKENS[token] = username

            return JsonResponse({
                'message': 'Success',
                'token': token  # Send token to frontend
            }, status=200)

        return JsonResponse({'error': 'Invalid credentials'}, status=401)

@csrf_exempt # This tells Django "Don't check for a CSRF token here"
def get_user_subscriptions(request):
    # 1. Extract Token from Header
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Token '):
        return JsonResponse({'error': 'No token provided'}, status=403)

    provided_token = auth_header.split(' ')[1]

    # 2. Validate Token
    username = ACTIVE_TOKENS.get(provided_token)
    if not username:
        return JsonResponse({'error': 'Invalid or expired token'}, status=403)

    # 3. Return Data
    subscriptions = [
        {"id": "SUB-9921", "name": "QuantumSentinel Pro", "status": "Active", "cost": "$4,200.00"},
        {"id": "SUB-4410", "name": "NexusVortex Ingestion Node", "status": "Active", "cost": "$52,000.00"}
    ]
    return JsonResponse({"user": username, "subscriptions": subscriptions})