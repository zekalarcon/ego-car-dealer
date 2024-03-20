from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('cars/', views.Cars.as_view(), name='cars'),
    path('cars/categories/', views.Categories.as_view(), name='car_categories'),
    path('cars/colors/', views.Colors.as_view(), name='car_colors'),
    path('cars/<slug:category_slug>/<slug:car_title_slug>/', views.CarDetail.as_view(), name='car_detail'),
    path('cars/search/', views.Search.as_view(), name='car_search'),
    path('cars/crud/', views.CarCRUD.as_view(), name='crud'),
    path('cars/category/', views.create_category, name='create_category'),
    path('cars/color/', views.create_color, name='create_color'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
