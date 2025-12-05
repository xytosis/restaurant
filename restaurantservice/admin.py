from django.contrib import admin
from .models import (
    Staff, Table, Reservation, Restaurant
)


# Register models with basic defaults
admin.site.register(Staff)
admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(Restaurant)