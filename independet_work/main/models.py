from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.staticfiles.storage import staticfiles_storage

# Create your models here.

class Craftitem(models.Model):

    name = models.CharField(max_length=50,
                            verbose_name='Имя товара',
                            null=False,
                            blank=False,
                            )
    
    photo = models.ImageField(upload_to='photo_item',
                              blank=True,
                              null=True,
                              verbose_name='Фото товара',
                              )
    
    price = MoneyField(max_digits=10,
                       decimal_places=2,
                       default_currency='BYN',
                       verbose_name='Цена товара',
                       )
    
    availability = models.BooleanField(verbose_name='Наличие товара',
                                       null=True,
                                       blank=True,
                                       )
    
    description = models.TextField(verbose_name='Описание товара',
                                    blank=True,
                                    null=True,
                                    )
    
    class Meta:
        verbos_name = 'Товар',
        verbos_name_plural = 'Товары'


    # #заглушка на отсутсвующие фото
    # @property
    # def get_photo_url(self):
    #     if self.photo and self.photo.storage.exists(self.photo.name):
    #         return self.photo.url
    #     return staticfiles_storage.url('images/no_photo.jpg')