import pytest
from .models import Car, Category, Color


@pytest.fixture
def category_instance():
   return Category.objects.create(name='auto')

@pytest.fixture
def category_instance_2():
   return Category.objects.create(name='pick up')

@pytest.fixture
def color_instance():
   return Color.objects.create(name='rojo')


@pytest.mark.django_db
class TestCarsAPIView:
    def create_car_objects(self, category, color, quantity, name):
        for i in range(quantity):
            Car.objects.create(
                category=category, 
                title=f"{name} {i+1}", 
                secondary_title=f"title secondary {i+1}", 
                description_title=f"description {i+1}", 
                price=1000 * i, 
                color=color, 
                year=2000+i, 
                doors=5
            )
    
    def test_get_paginated_response_with_valid_params(self, client, category_instance, color_instance):
        
        # Create 24 cars for pagination testing
        self.create_car_objects(category_instance, color_instance, 24, 'Car')
            
        response = client.get('/api/v1/cars/?p=1&created=descending')
        assert response.status_code == 200

        # Assert pagination details (replace with expected values from CustomPagination)
        assert response.data['count'] == 24
        assert len(response.data['results']) == 12  # 12 cars per page (from CustomPagination)

        # Assert first car in the first page is sorted by descending created date
        assert response.data['results'][0]['title'] == "Car 24"  # Assuming title reflects creation order

    def test_get_paginated_response_with_invalid_page(self, client, category_instance, color_instance):
        # Create some cars
        self.create_car_objects(category_instance, color_instance, 5, 'Car')

        response = client.get('/api/v1/cars/?p=99')  # Invalid page number
        assert response.status_code == 404
    
    def test_get_paginated_response_with_category_filter(self, client, category_instance, color_instance, category_instance_2):
        category = "auto"
        self.create_car_objects(category_instance, color_instance, 10, 'Car')
        self.create_car_objects(category_instance_2, color_instance, 5, 'Car2')

        response = client.get(f'/api/v1/cars/?category={category}') # To order, add for example: &created=descending
        assert response.status_code == 200
        assert len(response.data['results']) == 10  # Only cars with the specified category
    
    def test_get_paginated_response_with_created_sorting(self, client, category_instance, color_instance):
        # Create cars with varying creation dates
        self.create_car_objects(category_instance, color_instance, 5, 'Car')

        response = client.get('/api/v1/cars/?created=ascending')
        assert response.status_code == 200
        assert response.data['results'][0]['title'] == "Car 1"  # Sorted by ascending created date

    def test_get_paginated_response_with_price_sorting(self, client, category_instance, color_instance):
        # Create cars with varying prices (assuming a 'price' field)
        self.create_car_objects(category_instance, color_instance, 5, 'Car')

        response = client.get('/api/v1/cars/?price=lowest')
        assert response.status_code == 200
        assert response.data['results'][0]['title'] == "Car 1"  # Sorted by lowest price

    def test_get_paginated_response_with_year_sorting(self, client, category_instance, color_instance):
        # Create cars with varying 'year' fields (assuming a 'year' field)
        self.create_car_objects(category_instance, color_instance, 5, 'Car')

        response = client.get('/api/v1/cars/?year=new')
        assert response.status_code == 200
        assert response.data['results'][0]['title'] == "Car 5"  # Sorted by newest year