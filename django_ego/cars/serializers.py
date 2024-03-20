from rest_framework import serializers
from .models import Category, Color, Car, Slider, Feature
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    '''
    Serializer class for car categories
    '''

    class Meta:
        model = Category
        fields = (
            "id",
            "name"
        )


class ColorSerializer(serializers.ModelSerializer):
    '''
    Serializer class for car colors
    '''

    class Meta:
        model = Color
        fields = (
            "id",
            "name"
        )


class CarSerializer(serializers.ModelSerializer):
    '''
    Serializer class for cars
    '''

    category = serializers.SerializerMethodField('get_category_name')
    color = serializers.SerializerMethodField('get_color_name')

    def get_category_name(self, obj):
        if obj:
            return obj.category.name
        return ""
    
    def get_color_name(self, obj):
        if obj:
            return obj.color.name
        return ""
    
    class Meta:
        model = Car
        fields = (
            "id",
            "available",
            "category",
            "title",
            "year",
            "price",
            "engine",
            "color",
            "doors",
            "main_image",
            "secondary_image",
            "get_main_image",
            "get_main_thumbnail",
            "get_created"
        )
    
    def create(self, car):
        """
        Overriding the default create method of the Model serializer.
        :param car: data containing all the details of car
        :return: returns a successfully created car id
        """
 
        car = Car.objects.create(**car)
        return car.id


class CarDetailSerializer(serializers.ModelSerializer):
    '''
    Serializer class for car detail
    '''

    slider = serializers.SerializerMethodField('get_slider')
    feature = serializers.SerializerMethodField('get_feature')
    category = serializers.SerializerMethodField('get_category_name')
    color = serializers.SerializerMethodField('get_color_name')

    def get_slider(self, obj):
        if obj.id:
            #print('obj', obj.id)
            slider = Slider.objects.filter(car=obj.id).all()
            serializer = SliderSerializer(slider, many=True)
            return serializer.data
        return ""
    
    def get_feature(self, obj):
        if obj.id:
            #print('obj', obj.id)
            features = Feature.objects.filter(car=obj.id).all()
            serializer = FeatureSerializer(features, many=True)
            return serializer.data
        return ""
    
    def get_category_name(self, obj):
        if obj:
            return obj.category.name
        return ""
    
    def get_color_name(self, obj):
        if obj:
            return obj.color.name
        return ""
    
    class Meta:
        model = Car
        fields = (
            "id",
            "available",
            "category",
            "title",
            "secondary_title",
            "description_title",
            "description",
            "year",
            "color",
            "doors",
            "engine",
            "price",
            "get_main_image",
            "get_main_thumbnail",
            "get_secondary_image",
            "get_secondary_thumbnail",
            "slider",
            "feature",
            "get_created"
        )


class SliderSerializer(serializers.ModelSerializer):
    '''
    Serializer class for car slider
    '''
    
    class Meta:
        model = Slider
        fields = (
            "id",
            "car",
            "title",
            "description",
            "image",
            "get_image",
            "get_thumbnail",
            "get_created"
        )

        

class FeatureSerializer(serializers.ModelSerializer):
    '''
    Serializer class for car features
    '''

    class Meta:
        model = Feature
        fields = (
            "id",
            "car",
            "title",
            "description",
            "image",
            "get_image",
            "get_thumbnail",
            "get_created"
        )

