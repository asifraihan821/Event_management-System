from django.contrib.auth.models import User,Group
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_delete,post_save


@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        user_group,created = Group.objects.get_or_create(name = 'User')
        instance.groups.add(user_group)
        instance.save()
        


