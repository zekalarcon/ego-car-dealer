from django.contrib import admin
from .models import Category, Color, Car, Slider, Feature

admin.site.register(Category)
admin.site.register(Color)

class SliderAdmin(admin.TabularInline):
    model = Slider

class FeatureAdmin(admin.TabularInline):
    model = Feature

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [SliderAdmin, FeatureAdmin]
    list_display = ['title', 'category', 'year', 'price', 'color', 'doors', 'engine', 'id']
    list_filter = ('category', 'color', 'doors', 'year', 'engine')
    search_fields = ('title', 'secondary_title', 'price' )
    ordering = ['created']
    exclude = ('slug',)

    class Meta:
       model = Car

