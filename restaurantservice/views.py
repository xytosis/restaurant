import json
import secrets
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import (
    Restaurant, Staff, Table, Reservation, UserToken,
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


@csrf_exempt
def custom_login_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        time.sleep(2.5)
        # Dummy check for demo purposes
        if username == "admin" and password == "password123":
            # SAVE TO DATABASE
            token_obj = UserToken.generate_for_user(username)

            return JsonResponse({
                'message': 'Handshake Successful',
                'token': token_obj.token  # Send the DB-backed token to frontend
            }, status=200)

        return JsonResponse({'error': 'Unauthorized: Neural match failed'}, status=401)


def get_user_subscriptions(request):
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Token '):
        return JsonResponse({'error': 'Header: Authorization Token missing'}, status=403)

    provided_token = auth_header.split(' ')[1]

    # --- QUERY POSTGRES ---
    try:
        # We look for the token in the DB table
        token_record = UserToken.objects.get(token=provided_token)
        username = token_record.username
    except UserToken.DoesNotExist:
        # If Heroku restarts, the record is still in Postgres!
        return JsonResponse({'error': 'Invalid or expired token'}, status=403)

    # Return the "Corporate Crap" data
    subscriptions = [
        {"id": "SUB-99", "name": "Global Traffic Proxy", "status": "Active", "cost": "$1,400.00"},
        {"id": "SUB-10", "name": "Edge Compute (Tokyo)", "status": "Active", "cost": "$8,200.00"}
    ]
    return JsonResponse({"user": username, "subscriptions": subscriptions})