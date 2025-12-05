from django.db import models

class Restaurant(models.Model):
    """Basic information about the restaurant."""
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return self.name

class Staff(models.Model):
    """Employee details."""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='staff_members')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ROLE_CHOICES = [
        ('W', 'Waiter/Waitress'),
        ('C', 'Chef/Cook'),
        ('M', 'Manager'),
        ('H', 'Host/Hostess'),
    ]
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"

    class Meta:
        verbose_name_plural = "Staff"


class Table(models.Model):
    """Represents a physical table in the restaurant."""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField(default=2)
    STATUS_CHOICES = [
        ('A', 'Available'),
        ('O', 'Occupied'),
        ('R', 'Reserved'),
        ('C', 'Cleaning'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')

    def __str__(self):
        return f"Table {self.number} (Capacity: {self.capacity})"


class Reservation(models.Model):
    """Tracks a customer's booking for a table."""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reservations')
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=15)
    party_size = models.IntegerField()
    reservation_time = models.DateTimeField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Reservation for {self.customer_name} at {self.reservation_time.strftime('%Y-%m-%d %H:%M')}"
