from datetime import datetime, timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from accounts.models import User
from services.utils import generate_qr_code


class Hall(models.Model):
    number_hall = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])

    class Meta:
        verbose_name = "Hall"
        verbose_name_plural = "Halls"

    def __str__(self):
        return f"Hall {self.number_hall}"


class ColumnSeats(models.Model):
    number_column = models.IntegerField(validators=[MinValueValidator(1)])
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='columns')

    class Meta:
        verbose_name = "Column Seat"
        verbose_name_plural = "Column Seats"

    def __str__(self):
        return f"Column {self.number_column} in Hall {self.hall.number_hall}"


class Seat(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('booked', 'Booked')
    ]
    column = models.ForeignKey(ColumnSeats, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=10)
    number = models.PositiveIntegerField()
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='available')

    class Meta:
        verbose_name = "Seat"
        verbose_name_plural = "Seats"

    def __str__(self):
        return f"{self.row} Seat {self.number} (Column {self.column.number_column} in Hall {self.column.hall.number_hall})"


class Spectacle(models.Model):
    title = models.CharField(max_length=60)
    image = models.ImageField(upload_to='media/img/spectacles', null=True)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration = models.IntegerField(validators=[MinValueValidator(0)])
    datetime_passing = models.DateTimeField()
    theater_director = models.CharField(max_length=125)
    hall = models.OneToOneField(Hall, on_delete=models.DO_NOTHING, related_name='spectacles')
    age_limit = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=6)

    def __str__(self):
        return f"{self.title}"


class Ticket(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    spectacle = models.ForeignKey(Spectacle, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr_code_image = generate_qr_code(
                f'Ticket for {self.spectacle.title} at seat {self.seat.row} {self.seat.number}')
            self.qr_code.save(f'qr_code_{self.id}.png', qr_code_image, save=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        unique_together = ('seat', 'spectacle')

    def __str__(self):
        return f"Ticket for {self.spectacle.title} at {self.seat.row} Seat {self.seat.number}"
