from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

MONTHS = ([('%s' % d, d) for d in range(1,12)])
YEARS = ([('%s' % d, d) for d in range(2012, 2015)])

class Profile(models.Model):
    user = models.ForeignKey(User)
    address = models.CharField(verbose_name='Street Address', max_length=255)
    address2 = models.CharField(verbose_name='Address line2', max_length=255)
    sex = models.CharField(verbose_name='Sex', choices=GENDER_CHOICES, max_length=1)
    postal_code = models.CharField(verbose_name='Postal code', max_length=6)
    age = models.IntegerField(verbose_name='Age', default=17)
    phone1 = models.CharField(verbose_name='Primary phone', max_length=12)
    phone2 = models.CharField(verbose_name='Alternate phone', max_length=12)


class Card(models.Model):
    profile = models.ForeignKey(Profile)
    cardholder = models.CharField(verbose_name="Card's holder name", max_length=64)
    valid_thru_yr = models.IntegerField(verbose_name='Valid thru', choices=YEARS)
    valid_thru_mo = models.IntegerField(verbose_name='Valid thru', choices=MONTHS)




 # definition of UserProfile from above
 # ...

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)