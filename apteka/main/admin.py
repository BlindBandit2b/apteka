from django.contrib import admin
from .models import Svoistvo, Category, DrugItem, DrugItemSvoistvo

class DrugItemSvoistvoInLine(admin.TabularInline): 
    model = DrugItemSvoistvo
    extra = 4

@admin.register(Svoistvo)
class SvoistvoAdmin(admin.ModelAdmin):
    list_display= ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(DrugItem)
class DrugItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category',
                    'available', 'price', 'discount',
                    'created_at', 'updated_at')
    list_filter = ('available', 'category')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)
    inlines = [DrugItemSvoistvoInLine]