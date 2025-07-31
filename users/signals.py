from django.contrib.auth.models import User,Group
from django.dispatch import receiver
from django.db.models.signals import m2m_changed,pre_save,post_delete,post_save
from events.models import Event
from django.core.mail import send_mail
from users.models import UserProfile

@receiver(m2m_changed, sender=Event.attendees.through)
def send_rsvp_email(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = instance.attendees.get(pk=user_id)
            send_mail(
                'RSVP Confirmation',
                f'Thank you {user.username} for RSVPing to "{instance.name}".',
                'noreply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender,instance, created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    

