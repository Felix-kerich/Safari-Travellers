from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
class MemberManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class Member(AbstractBaseUser, PermissionsMixin):
    fname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, null=True)
    amount_paid = models.CharField(max_length=100,null=True, blank=True)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    seatNumber = models.CharField(max_length=100,null=True, blank=True)
    vehicle = models.CharField(max_length=100,null=True, blank=True)
    is_paid =  models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'username'
    groups = models.ManyToManyField(
        Group,
        verbose_name= ('groups'),
        blank=True,
        help_text= (
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='members'  # Custom related name to avoid clashes
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name= ('user permissions'),
        blank=True,
        help_text= ('Specific permissions for this user.'),
        related_name='members'  # Custom related name to avoid clashes
    )

    def __str__(self):
        return f'{self.username}'
class BusesAvailable(models.Model):
    BusName = models.CharField(max_length=100)
    From = models.CharField(max_length=100, null=True, blank=True)
    BusDestination = models.CharField(max_length=100,null=True, blank=True)
    BusArrivalTime = models.DateTimeField()
    BusArrivalDate = models.DateTimeField()
    Amount = models.CharField(max_length=100, null=True, blank=True)
    NuberOfSeats = models.CharField(max_length=100, null=True, blank=True)

    def time_until_arrival(self):
        current_time = timezone.now()
        time_until_arrival = self.BusArrivalTime - current_time
        return time_until_arrival
    def __str__(self):
        return self.BusName

class Notifications(models.Model):
    BusName = models.CharField(max_length=100,null=True, blank=True)
    From = models.CharField(max_length=100, null=True, blank=True)
    BusDestination = models.CharField(max_length=100,null=True,blank=True)
    message = models.CharField(max_length=100, null=True, blank=True)
    generalNotification = models.CharField(max_length=100, null=True, blank=True)
class MpesaTransaction(models.Model):
    MerchantRequestID = models.CharField(max_length=50)
    CheckoutRequestID = models.CharField(max_length=50)
    ResultCode = models.CharField(max_length=10)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    MpesaReceiptNumber = models.CharField(max_length=50)
    PhoneNumber = models.CharField(max_length=15)


    def __str__(self):
        return f"{self.MpesaReceiptNumber} - {self.Amount}"
