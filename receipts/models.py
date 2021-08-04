from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Store(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Receipt(models.Model):
    date = models.DateField()
    amount = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount) + " is spent in " + self.store.name + " ."


def get_image_filename(instance, filename):
    receipt_id = instance.receipt.id
    return 'receipt_images/{}-{}'.format(receipt_id, filename)


class Images(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')


@receiver(pre_delete, sender=Images)
def img_delete(sender, instance, *args, **kwargs):
    """
    Clean old image files from media directory
    """
    try:
        instance.image.delete(save=False)
    except:
        pass




