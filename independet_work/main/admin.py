from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

# Register your models here.

class ProductImageInline(admin.TabularInline):
    
    model = Productimage
    extra = 1
    readonly_fields = ('get_image_preview',)

    def get_image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width = "100" />')
        return 'Нет фото'
    
    get_image_preview.short_description = 'Превью'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('get_main_photo', 
                    'name_item',
                    'category', 
                    'price', 
                    'availability',
                    'scent', 
                    )
    
    list_editable = ('price',
                     'availability',
                     )
    
    search_fields = ('name_item',
                    'category__name_category', 
                    'scent__name_scent',  
                    )
    
    list_filter = ('category', 
                    'scent', 
                    'availability', 
                    )
    
    prepopulated_fields = {'slug': ('name_item',)}

    inlines = [ProductImageInline]

    save_on_top = True

    def get_main_photo(self, obj):
        main_img = obj.product.filter(main_img=True).first() or obj.product.first()
        if main_img and main_img.image:
            return mark_safe(f'<img src="{main_img.image.url}" width="50" style="border-radius:5px;" />')
        return "❌"
    
    get_main_photo.short_description = 'Фото'


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    
    list_display = ('id',
                    'name_client',
                    'product',
                    'status',
                    'created_at',
                    )
    
    list_filter =('status',
                  'created_at',
                  )
    
    search_fields = ('name_client',
                     'contact_info',
                     'product__name_item',)
    
    readonly_fields = ('product',
                       'created_at',
                    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {'slug': ('name_category',)}


@admin.register(Scent)
class ScentAdmin(admin.ModelAdmin):
    
    list_display = ('name_scent',
                    'notes',
                    )