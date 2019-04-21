#from django.db import models
from __future__ import unicode_literals
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .util import UserManager

# Create your models here.
degrees = (
    ('CS', 'Computer Science'),
    ('CV', 'Civil Engineering'),
    ('BBA', 'Business Adminstration'),
    ('EE', 'Elctrical Engineering'),
    ('AF', 'Account & Finance'),
)

class User(AbstractBaseUser, PermissionsMixin):
    
    roll_num = models.CharField(_('Roll Number'),max_length=7, unique=True)
    degree = models.CharField(_('degree'),choices=degrees, max_length=25)
    email = models.EmailField(_('email address'))
    is_staff = models.BooleanField(
        _('Staff Status'), default=True,
        help_text=_('Designates whether the user can log into this admin '
                    'site.')
    )
    
    #first_name = models.CharField(_('first name'), max_length=30, blank=True)
    #last_name = models.CharField(_('last name'), max_length=30, blank=True)
    #date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    #is_active = models.BooleanField(_('active'), default=True)
    #avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'roll_num'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


    
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        return self.roll_num