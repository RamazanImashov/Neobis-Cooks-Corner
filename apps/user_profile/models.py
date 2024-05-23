from django.db import models
from django.contrib.auth import get_user_model
import os, uuid
from django.dispatch import receiver
from django.db.models.signals import post_save


User = get_user_model()


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(instance.directory_string_var, filename)


class UserProfile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id аккаунта", related_name="user")
    username = models.CharField(max_length=50, verbose_name="Имя пользователя")
    description = models.TextField(verbose_name="Опимание профиля", blank=True, null=True)
    profile_image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    subscriptions = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)
    directory_string_var = f'user-profile'

    def __str__(self):
        return f"{self.username} {self.user_id}"

    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print(f"User {instance.email} was created: {created}")
    if created:
        UserProfile.objects.create(user_id=instance, username=instance.username)
