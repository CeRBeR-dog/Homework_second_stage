from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.staticfiles.storage import staticfiles_storage

# Create your models here.

class Category(models.Model):

    name_category = models.CharField(max_length=100,
                            verbose_name='Категория товара',
                            null=False,
                            blank=False,
                            )
    
    slug = models.SlugField(max_length=100,
                            unique=True,
                            verbose_name='URL',
                            )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name_category


class Scent(models.Model):

    name_scent = models.CharField(max_length=100,
                            verbose_name='Название аромата',
                            null=False,
                            blank=False,
                            )
    
    notes = models.TextField(verbose_name='Описание нот',
                                    blank=True,
                                    )
    
    class Meta:
        verbose_name = 'Аромат'
        verbose_name_plural = 'Ароматы'

    def __str__(self):
        return self.name_scent


class Product(models.Model):

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products',
                                 verbose_name='Категория',
                                 )
    
    scent = models.ForeignKey(Scent,
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='product',
                              verbose_name='Аромат',
                              )

    name_item = models.CharField(max_length=100,
                            verbose_name='Имя товара',
                            null=False,
                            blank=False,
                            )
    
    slug = models.SlugField(max_length=100,
                            unique=True,
                            verbose_name='URL',
                            )
    
    # photo = models.ImageField(upload_to='products/%Y/%m/%d/',
    #                           blank=True,
    #                           null=True,
    #                           verbose_name='Фото товара',
    #                           )
    
    price = MoneyField(max_digits=10,
                       decimal_places=2,
                       default_currency='BYN',
                       verbose_name='Цена товара',
                       )
    
    availability = models.BooleanField(verbose_name='В наличии',
                                       default=True,
                                       )
    
    description = models.TextField(verbose_name='Описание товара',
                                    blank=True,
                                    )
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-id']

    def __str__(self):
        return self.name_item
    
    #заглушка на отсутсвующие фото
    @property
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return staticfiles_storage.url('images/no_photo.jpg')


class Productimage(models.Model):

    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='product',
                                verbose_name='Товара',
                                )
    
    image = models.ImageField(upload_to='products/%Y/%m/%d/',
                              blank=True,
                              null=True,
                              verbose_name='Фото товара',
                              )
    
    main_img = models.BooleanField(verbose_name='Главное фото',
                                   blank=True,
                                   )
    
    

class Lead(models.Model):

    choices_status = [
        ('new','новый'),
        ('in_progress','делается'),
        ('done','готово')
               ]
        
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='leads',
                                verbose_name='Название товара для заказа',
                                )
    
    name_client = models.CharField(max_length=50,
                            verbose_name='Имя заказчика',
                            null=False,
                            blank=False,
                            )
    
    contact_info = models.CharField(max_length=100,
                            verbose_name='Контакты заказчика',
                            null=False,
                            blank=False,
                            )
    
    status = models.CharField(choices=choices_status,
                              max_length=20,
                              verbose_name='Статус заказа',
                              )
    
    created_at = models.DateTimeField(verbose_name='Дата и время подачи заявки',
                                      auto_now_add=True,
                                      null=True,
                                      )
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f"Заявка #{self.id} от {self.name_client}"


