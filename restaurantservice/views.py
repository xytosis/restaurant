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

