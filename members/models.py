import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.fields.files import ImageField
from django.utils.translation import gettext_lazy as _

from farjad.settings import EDUCATION_CHOICES
from farjad.utils.utils_view import get_url, get_random, auto_save
from loan.models import Loan, LoanState

mobile_regex = RegexValidator(
    regex=r'^(09|(\+989))\d{9}$',
    message=_('Mobile number should start with 09 and should have 11 digits.'))


def generate_unique_login_code():
    code = get_random(5)
    while PhoneCodeMapper.objects.filter(code=code).exists():
        code = get_random(5)
    return code


def generate_invitation_unique_code():
    code = get_random(10)
    while Member.objects.filter(invitation_code=code).exists():
        code = get_random(10)
    return code


class MemberManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_fields)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, phone, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class PhoneCodeMapper(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=11, blank=False, null=False, unique=True,
                             validators=[mobile_regex],
                             error_messages={
                                 'unique': _("A user with that phone already exists."),
                             })


class Member(AbstractUser):
    username = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    phone = models.CharField(max_length=11, blank=False, null=False, unique=True,
                             validators=[mobile_regex],
                             error_messages={
                                 'unique': _("A user with that phone already exists."),
                             })
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = ImageField(upload_to='profile_pictures/', null=True, blank=True)
    profession = models.CharField(max_length=32)
    education = models.CharField(max_length=30, choices=EDUCATION_CHOICES)
    city = models.CharField(max_length=60)
    province = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    balance = models.IntegerField(default=1000, unique=False)
    invitation_code = models.CharField(max_length=10, blank=True, null=True)
    objects = MemberManager()
    invited_with = models.CharField(max_length=10, blank=True, null=True)

    @property
    def age(self):
        if self.birth_date is not None:
            return datetime.date.today() - self.birth_date
        return None

    @property
    def image_url(self):
        if self.profile_picture is not None and self.profile_picture != "":
            return self.profile_picture
        else:
            return get_url(None, 'members/icons/default_profile.png')

    @auto_save
    def increase_balance(self, amount):
        self.balance += amount

    @auto_save
    def decrease_balance(self, amount):
        self.balance -= amount

    @property
    def full_name(self):
        full_name = self.first_name + " " + self.last_name
        full_name = full_name.strip()
        if full_name == "":
            full_name = self.phone
        return full_name

    def get_invitation_code(self):
        if self.invitation_code is None:
            self.invitation_code = generate_invitation_unique_code()
            self.save()

        return self.invitation_code

    @property
    def new_loan_requests(self):
        return Loan.objects.all().filter(book__owner=self, state__state=LoanState.STATE_NEW)
