from django.db import models
from io import BytesIO
from django.utils import timezone
from PIL import Image
from django.core.files import File
from django.utils.text import slugify
import os

def get_created_func(date):
    try:
        fmt = "%d %b %Y at %H:%M %p"
        utc = date
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz.strftime(fmt)
    except:
        return '-'
        
def resize_image_func(image, selected, title, year, size=(500,500)):
    img = Image.open(image)
    img.resize(size)
    thumb_io = BytesIO()
    img.save(thumb_io, 'webp', optimize=True, quality=85)

    if selected == 'main':
        image_resized = File(thumb_io, name='main-' + title + str(year) + '.webp')
    if selected == 'secondary':
        image_resized = File(thumb_io, name='secondary-' + title + str(year) + '.webp')
    if selected == 'slider':
        image_resized = File(thumb_io, name='slider-' + title + str(year) + '.webp')
    if selected == 'feature':
        image_resized = File(thumb_io, name='feature-' + title + str(year) + '.webp')
    return image_resized

def make_thumbnail_func(image, selected, title, year, size=(300,300)):
    img = Image.open(image)
    img.thumbnail(size)
    thumb_io = BytesIO()
    img.save(thumb_io, 'webp', optimize=True, quality=50)

    if selected == 'main':
        thumbnail = File(thumb_io, name='main-thumbnail-' + title + str(year) + '.webp')
    if selected == 'secondary':
        thumbnail = File(thumb_io, name='secondary-thumbnail-' + title + str(year) + '.webp')
    if selected == 'slider':
        thumbnail = File(thumb_io, name='slider-thumbnail-' + title + str(year) + '.webp')
    if selected == 'feature':
        thumbnail = File(thumb_io, name='feature-thumbnail-' + title + str(year) + '.webp')
    return thumbnail

class Category(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('name',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'
    

class Color(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
  
    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Car(models.Model):

    DOORS = (
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    ENGINE = (
        ('nafta', 'nafta'),
        ('diesel', 'diesel'),
        ('electrico', 'electrico')
    )

    available = models.BooleanField(default=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=300, unique=True)
    secondary_title = models.CharField(max_length=300 , null=True, blank=True)
    description_title = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    year = models.IntegerField(default=0)
    color = models.ForeignKey(Color, null=True, on_delete=models.SET_NULL)
    doors = models.IntegerField(choices=DOORS)
    engine = models.CharField(max_length=100,choices=ENGINE)
    price = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    main_image = models.FileField(upload_to = 'cars/main_images', max_length=200, null=True, blank=True)
    main_thumbnail = models.ImageField(upload_to='cars/main_thumbnail_images/', max_length=200, null=True, blank=True)
    secondary_image = models.FileField(upload_to = 'cars/secondary_images', max_length=200, null=True, blank=True)
    secondary_thumbnail = models.ImageField(upload_to='cars/secondary_thumbnail_images/', max_length=200, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.main_image:
            if self.main_image.name.endswith('.webp'):
                self.main_thumbnail = make_thumbnail_func(self.main_image, 'main', self.title, self.year)
            else:
                self.main_image = self.resize_image(self.main_image, 'main')            
                self.main_thumbnail = make_thumbnail_func(self.main_image, 'main', self.title, self.year)         
        if self.secondary_image:
            if self.secondary_image.name.endswith('.webp'):    
                self.secondary_thumbnail = make_thumbnail_func(self.secondary_image, 'secondary', self.title, self.year)     
            else:
                self.secondary_image = self.resize_image(self.secondary_image, 'secondary')   
                self.secondary_thumbnail = make_thumbnail_func(self.secondary_image, 'secondary', self.title, self.year)
 
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_main_image(self):
        if self.main_image:
            return 'http://127.0.0.1:8000' + self.main_image.url
        return ''
        
    def get_secondary_image(self):
        if self.secondary_image:
            return 'http://127.0.0.1:8000' + self.secondary_image.url
        return ''
    
    def resize_image(self, image, selected, size=(500,500)):
        return resize_image_func(image, selected, self.title, self.year)
    
    def get_main_thumbnail(self):
        
        if self.main_thumbnail:
            return 'http://127.0.0.1:8000' + self.main_thumbnail.url
        else:
            return ''

    def get_secondary_thumbnail(self):
        if self.secondary_thumbnail:
            return 'http://127.0.0.1:8000' + self.secondary_thumbnail.url
        else:
            return ''
    
    def get_created(self):
        return get_created_func(self.created)


class Slider(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to = 'cars/slider_images', blank=True, null=True, max_length=200)
    thumbnail = models.ImageField(upload_to= 'cars/slider_thumbnail_images/', blank=True, null=True, max_length=200)
    created = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'Sliders'

    def save(self, *args, **kwargs):
        if self.image.name.endswith('.webp'):
            self.thumbnail = make_thumbnail_func(self.image, 'slider', self.car.title, self.car.year)
        else:
            self.image = self.resize_image(self.image)
            self.thumbnail = make_thumbnail_func(self.image, 'slider', self.car.title, self.car.year)
        
        return super().save(*args, **kwargs)
           
    def __str__(self):
        return str(self.car.title)  

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def resize_image(self, image, size=(500,500)):
        return resize_image_func(image,'slider', self.car.title, self.car.year)
      
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            return ''
    
    def get_created(self):
        return get_created_func(self.created)

class Feature(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to = 'cars/feature_images', max_length=200, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='cars/feature_thumbnail_images/', blank=True, null=True, max_length=200)
    created = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'

    def save(self, *args, **kwargs):
        if self.image.name.endswith('.webp'):
            self.thumbnail = make_thumbnail_func(self.image,'feature', self.car.title, self.car.year)
        else:
            self.image = self.resize_image(self.image)
            self.thumbnail = make_thumbnail_func(self.image,'feature', self.car.title, self.car.year)
        
        return super().save(*args, **kwargs)
           
    def __str__(self):
        return str(self.car)  

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def resize_image(self, image, size=(500,500)):
        return resize_image_func(image,'feature', self.car.title, self.car.year)

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            return ''

    def get_created(self):
        return get_created_func(self.created)