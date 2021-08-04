import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from PIL import Image


def get_image_filename(instance, filename):
    user_name = instance.user.username
    f_name, f_ext = os.path.splitext(filename)
    return 'profile_photo/{}{}'.format(user_name, f_ext)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile.jpg',
                              verbose_name='Change Avatar',
                              upload_to=get_image_filename)

    def __str__(self):
        return '{} Profile'.format(self.user.username)

    def __repr__(self):
        return '{} Profile(id={})'.format(self.user.username, self.id)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)  # open image

        # resize image
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)  # resize image
            img.save(self.image.path)


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """When a user is created, a default profile is created and saved automatically """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



