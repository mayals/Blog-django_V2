from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile


# -----------------# signal to create profile object  # -----------------------------------------------#
@receiver(post_save, sender=get_user_model())
def create_profile(sender, **kwarg):
    if kwarg['created']:
        Profile.objects.create(user=kwarg['instance'])


# another correct way of writting signal
#post_save.connect(create_profile, sender=User)