from django.db.models import Q
from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Color, Car, Slider, Feature
from .serializers import CategorySerializer, ColorSerializer, CarSerializer, CarDetailSerializer, SliderSerializer, FeatureSerializer
from .paginations import CustomPagination
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework import permissions
from knox.auth import TokenAuthentication
import json, os


@authentication_classes([])
@permission_classes([permissions.AllowAny])
class Categories(APIView):
    '''
    Return all the car categories
    '''

    def get_object(self):
        try:
            # Retrieve all objects from the Category model and order them by name
            return Category.objects.order_by('name').all()
        except Category.DoesNotExist:
            # Raise an HTTP 404 error if the object does not exist
            raise Http404

    #@api_view(['GET'])
    def get(self, request, format=None):
        # Get the object from the database
        categories = self.get_object()
        # Create a serializer object
        serializer = CategorySerializer(categories, many=True)

        # Return the serialized data
        return Response(serializer.data)
    

@authentication_classes([])
@permission_classes([permissions.AllowAny])
class Colors(APIView):
    '''
    Return all the car colors
    '''

    def get_object(self):
        try:
            # Get all objects from the Color model and order them by name
            return Color.objects.order_by('name').all()
        except Category.DoesNotExist:
            # Raise an HTTP 404 error if the object does not exist
            raise Http404
        
    #@api_view(['GET'])
    def get(self, request, format=None):
        # Get the color object from the database
        colors = self.get_object()
        # Create a serializer object to serialize the color object
        serializer = ColorSerializer(colors, many=True)

        # Return the serialized data
        return Response(serializer.data)


@authentication_classes([])
@permission_classes([permissions.AllowAny])
class Cars(generics.ListAPIView):
    '''
    Return 12 cars by page. Set in paginations.py.\n
    Can be filtered by query parameters,\n
    (page) ?p= ,
    ?category =,
    ?created =,
    ?price =,
    ?year =,\n
    'cars/?p=1&category=auto&created=descending&price=highiest&year=new'\n
    'cars/?p=1&category=auto'\n
    'cars/?p=2'
    '''

    queryset = Car.objects.all()
    pagination_class = CustomPagination

    def get_object(self, category, created, price, year):
        # Set the created_str variable to None if the created parameter is not set
        created_str = None
        # If the created parameter is set to 'descending', set the created_str variable to 'created'
        if created == 'descending': created_str = '-created'
        # If the created parameter is set to 'ascending', set the created_str variable to '-created'
        elif created == 'ascending': created_str = 'created'

        # Set the price_str variable to None if the price parameter is not set
        price_str = None
        # If the price parameter is set to 'lowest', set the price_str variable to 'price'
        if price == 'lowest': price_str = 'price'
        # If the price parameter is set to 'highest', set the price_str variable to '-price'
        elif price == 'highest': price_str = '-price'

        # Set the year_str variable to None if the year parameter is not set
        year_str = None
        # If the year parameter is set to 'new', set the year_str variable to '-year'
        if year == 'new': year_str = '-year'
        # If the year parameter is set to 'old', set the year_str variable to 'year'
        elif year == 'old': year_str = 'year'
        

        # Try to get the Car object from the Car model
        try:
            # If the category and created parameters are set, return the Car object sorted by the created_str variable
            if category and created:
                return Car.objects.filter(category__slug=category).order_by(created_str).all()
            # If the category and price parameters are set, return the Car object sorted by the price_str variable
            elif category and price:
                return Car.objects.filter(category__slug=category).order_by(price_str).all()
            # If the category and year parameters are set, return the Car object sorted by the year_str variable
            elif category and year:
                return Car.objects.filter(category__slug=category).order_by(year_str).all()
            # If the category, created, price and year parameters are not set, return the Car object sorted by the 'title' field
            else: 
                if category:
                    return Car.objects.filter(category__slug=category).all()
                # If the price parameter is set, return the Car object sorted by the price
                elif price:
                    return Car.objects.order_by(price_str).all()
                # If the created parameter is set, return the Car object sorted by the created_str variable
                elif created:
                    return Car.objects.order_by(created_str).all()
                # If the year parameter is set, return the Car object sorted by the year_str variable
                elif year:
                    return Car.objects.order_by(year_str).all()
                # If parameters not present, return the Car object sorted by title
                else:
                    return Car.objects.order_by('title').all()
        # If the Car object does not exist, raise an Http404 error
        except Car.DoesNotExist:
            raise Http404

    #@api_view(['GET'])
    def get(self, request, *args, **kwargs):
        # Get the query parameters from the request
        category = self.request.query_params.get('category')
        created = self.request.query_params.get('created')
        price = self.request.query_params.get('price')
        year = self.request.query_params.get('year')
        # Get the cars from the database based on the query parameters
        cars = self.get_object(category, created, price, year)
        # Paginate the results
        results = self.paginate_queryset(cars)
        # Create a serializer to serialize the results
        serializer = CarSerializer(results, many=True)

        # Return the paginated response
        return self.get_paginated_response(serializer.data)


class CarDetail(APIView):
    '''
    Return all the car information\n
    by category slug and car title slug.\n
    'cars/<slug:category_slug>/<slug:car_title_slug>/'
    'cars/auto/corolla
    '''

    def get_object(self, category_slug, car_title_slug):
        #try to get the car object from the database
        try:
            #return the car object from the database that matches the category slug and car title slug
            return Car.objects.filter(category__slug=category_slug).filter(slug=car_title_slug).first()
        #if the car object does not exist
        except Car.DoesNotExist:
            #raise an HTTP 404 error
            raise Http404
    
    #@api_view(['GET'])
    def get(self, request, category_slug, car_title_slug, format=None):
        # Get the car object from the given category slug and car title slug
        car = self.get_object(category_slug, car_title_slug)
        # Create a serializer object for the car object
        serializer = CarDetailSerializer(car)
       
        # Return the serialized data of the car object
        return Response(serializer.data)


class Search(APIView, CustomPagination):
    '''
    Search by query parameter ?q=\n
    over car title, secondary title,\n
    title description and description\n
    'cars/search/?q=hilux'
    '''

    def get_object(self, search):
        #try to get the car object from the database
        try:
            #return the car object that matches the search query
            return Car.objects.filter(
                #search for the car title that contains the search query
                Q(title__icontains=search) | 
                #search for the car description that contains the search query
                Q(description__icontains=search) |
                #search for the car description title that contains the search query
                Q(description_title__icontains=search) |
                #search for the car secondary title that contains the search query
                Q(secondary_title__icontains=search)
                #order the results by the created date
                ).order_by('created')
        #if the car object does not exist, raise an HTTP 404 error
        except Car.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        # Get the query parameter from the request
        search = self.request.query_params.get('q')

        # If the query parameter is not present, return an empty list
        if search == None:
            return Response([])
            
        # Get the cars from the database
        cars = self.get_object(search)
        # Paginate the cars
        results = self.paginate_queryset(cars, request, view=self)
        # Serialize the results
        serializer = CarSerializer(results, many=True)

        # Return the serialized results
        return self.get_paginated_response(serializer.data)
    
    
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class CarCRUD(APIView):
    '''
    Get especific car, update car, create car,
    delete car and delete slider or feature items
    '''
    

    #Define a function to save slider and features
    def save_slider_features(self, items, info):
        #Loop through each item in the list of items
        for item in items:
            #Get the id of the item
            id = item['id']

            #Check if the info is slider
            if info == 'slider':
                #Check if the slider exists
                exist = Slider.objects.filter(id=id).exists()
                #If the slider exists
                if exist == True:
                    #Get the slider query
                    slider_query = Slider.objects.get(id=id)
                    #Create a serializer for the slider
                    serializer_slider = SliderSerializer(slider_query, item, partial=True)
                    #Check if the serializer is valid
                    if serializer_slider.is_valid():
                        #Save the serializer
                        serializer_slider.save()
                #If the slider does not exist
                else:
                    #Delete the id from the item
                    del item['id']
                    #Create a serializer for the slider
                    serializer_slider = SliderSerializer(data=item)

                    #Check if the serializer is valid
                    if serializer_slider.is_valid():
                        #Update the car from the item 
                        item['car'] = Car.objects.get(id=int(item['car']))
                        #Create the serializer
                        serializer_slider.create(item)
            #Check if the info is feature
            else:
                #Check if the feature exists
                exist = Feature.objects.filter(id=id).exists()
                #If the feature exists
                if exist == True:
                    #Get the feature query
                    feature_query = Feature.objects.get(id=id)
                    #Create a serializer for the feature
                    serializer_feature = FeatureSerializer(feature_query, item, partial=True)
                    #Check if the serializer is valid
                    if serializer_feature.is_valid():
                        #Save the serializer
                        serializer_feature.save()
                #If the feature does not exist
                else:
                    #Delete the id from the item
                    del item['id']
                    #Create a serializer for the feature
                    serializer_feature = FeatureSerializer(data=item)
                    #Check if the serializer is valid
                    if serializer_feature.is_valid():
                        #Update the car from the item
                        item['car'] = Car.objects.get(id=int(item['car']))
                        #Create the serializer
                        serializer_feature.create(item)
        
    #Define a function called create_data that takes myDict as parameter
    def create_data(self, myDict):
        #Create an empty dictionary called car
        car = {}
        #Create an empty list called slider
        slider = []
        #Create an empty list called features
        features = []

        #Loop through each key and value in myDict
        for k, v in myDict.items():
            #Check if the key is not equal to slider, features, slider-images, features-images, or info
            if k != 'slider' and k != 'features' and k != 'slider-images' and k != 'features-images' and k != 'info':
                #Check if the key is available
                if k == 'available':
                    #Check if the value is true
                    if v[0] == 'true':
                        #Set the key in car to True
                        car[k] = True
                    else:
                        #Set the key in car to False
                        car[k] = False
                #Check if the key is not equal to image
                elif k != 'image':
                    #Check if the value is not empty
                    if v[0] != '':
                        #Set the key in car to the value
                        car[k] = v[0]
                #Check if the key is equal to image
                else:
                    #Set the key in car to the value
                    car[k] = v
            #Check if the key is equal to slider or features
            if k == 'slider' or k == 'features':
                #Create an empty dictionary called dic
                dic = {}
                #Loop through each item in the value of the key
                for index, item in enumerate(v):
                    #Loop through each key and value in the json of the item
                    for key, value in json.loads(item).items():                  
                        #Check if the key is equal to image and the value is true
                        if key == 'image' and value == True:
                            #Loop through each image in the value of the key
                            for indx, img in enumerate(myDict[str(k) + '-images']):                            
                                #Check if the name of the image is equal to the key and the index
                                if img.name == k + '-' + str(index):
                                    #Set the image in dic to the image in myDict
                                    dic['image'] = myDict[str(k) + '-images'][indx]
                        #Check if the key is equal to image and the value is empty
                        elif key == 'image' and value == '':
                            #Do nothing
                            pass
                        #Check if the key is not equal to image
                        else:
                            #Check if the value is not empty
                            if value != '':
                                #Set the key in dic to the value
                                dic[key] = value
                    #Check if the key is equal to slider
                    if k == 'slider':
                        #Append the dic to the slider list
                        slider.append(dic)
                    #Check if the key is not equal to slider
                    else:
                        #Append the dic to the features list
                        features.append(dic)
                    #Reset the dic
                    dic = {}

        #Return the car, slider, and features lists
        return car, slider, features
    
    #Define a function to delete a slider or feature item from the database
    def delete_slider_features_item(self, id, info):
        #Check if the info is equal to 'slider'
        if info == 'slider':
            #Get the slider object from the database
            slider = Slider.objects.get(id=id)
            #Remove the image associated with the slider
            os.remove(slider.image.path)
            #Delete the slider from the database
            slider.delete()
        else:
            #Get the feature object from the database
            feature = Feature.objects.get(id=id)
            #Remove the image associated with the feature
            os.remove(feature.image.path)
            #Delete the feature from the database
            feature.delete()
        
        #Return a response with the info deleted
        return Response( str(info) +' deleted')
    
    #@api_view(['PUT'])
    def put(self, request, format=None):   
        try:  
            # Create a dictionary from the request data
            myDict = dict(request.data)
            # Create data for the car, slider, and features
            car, slider, features = self.create_data(myDict)
            # Set the response to 'created'
            response = 'created'

            # If the info is set to 'update', get the car instance from the database and update it
            if request.data['info'] == 'update':
                # Set the response to 'update'
                response = 'updated'
                car_instance = Car.objects.get(id=int(request.data['id']))
                serializer_car = CarSerializer(car_instance, car, partial=True)

                # Validate the serializer and save the car data
                if serializer_car.is_valid():
                    car['category'] = Category.objects.get(name=car['category'])
                    car['color'] = Color.objects.get(name=car['color'])
                    serializer_car.save(**car)
                # Print any errors in the serializer
                #print(serializer_car.errors)
            # Otherwise, create a new car
            else:
                serializer_car = CarSerializer(data=car)
                if serializer_car.is_valid():
                    car['category'] = Category.objects.get(name=car['category'])
                    car['color'] = Color.objects.get(name=car['color'])
                    id = serializer_car.create(car)
                    # Iterate through the slider and features and set the car id
                    for item in slider:
                        item['car'] = id
                    for item in features:
                        item['car'] = id

            # Save the slider and features
            self.save_slider_features(slider, 'slider')
            self.save_slider_features(features, 'features')
            
            # Return the response
            return Response(response)
        except Exception as e:
            print('exception', e)
            return Response(str(e))
    
    #@api_view(['POST'])
    def post(self, request, format=None):
        try:
            # Get the id and info from the request data
            id = request.data['id']
            info = request.data['info']

            # Check if the info is car-data
            if request.data['info'] == 'car-data':
                # Get the car object from the id
                car = Car.objects.get(id=id)
                # Create a serializer for the car object
                serializer = CarDetailSerializer(car)
                # Return the serialized data
                return Response(serializer.data)
            # Check if the info is delete-car
            elif request.data['info'] == 'delete-car':
                # Delete the car object with the given id
                Car.objects.filter(id=id).first().delete()
                # Create a response string
                response = 'car deleted'
            # If the info is not car-data or delete-car
            else:
                try:
                # Call the delete_slider_features_item function
                    response = self.delete_slider_features_item(id, info)
                except:
                    response = 'query does not exist'
            
            # Return the response string
            return Response(str(response))
        except Exception as e:
            print('exception', e)
            return Response(str(e))


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def create_category(request):
    try:
        name = request.data['name']

        category = Category.objects.create(name=name)
        category.save()

        return Response('created')
    except:
        return Response('not created')
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def create_color(request):
    try:
        name = request.data['name']

        color = Color.objects.create(name=name)
        color.save()

        return Response('created')
    except:
        return Response('not created')