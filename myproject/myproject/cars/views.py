from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Car
import base64
from django.core.files.base import ContentFile
from io import BytesIO

# Cars view is vehicles page without any formatting which can be used for basic debugging
def cars_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT carid, carmaker, model, type, fuel, trans, seats, price, image_blob FROM cars")
        cars = cursor.fetchall()

    cars_list = []
    for car in cars:
        car = list(car)  # Convert the tuple to a list to allow modification
        if car[8]:  # Check if `image_blob` is not None
            try:
                car_image_base64 = base64.b64encode(car[8]).decode('utf-8')
                car.append(car_image_base64)
                # Uncomment line below for terminal debugging
                # print(f"Base64 Image Data for Car {car[0]}: {car_image_base64[:100]}...")
            except Exception as e:
                print(f"Error encoding image for Car {car[0]}: {e}")
                car.append(None)
        else:
            # Add None for cars without an image
            car.append(None)
        cars_list.append(car)

    paginator = Paginator(cars_list, 5)
    page = request.GET.get('page')
    try:
        cars_page = paginator.page(page)
    except PageNotAnInteger:
        cars_page = paginator.page(1)
    except EmptyPage:
        cars_page = paginator.page(paginator.num_pages)

    # Render the paginated cars list to the template
    return render(request, 'cars/cars_list.html', {'cars': cars_page})






def vehicles(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT carid, carmaker, model, type, fuel, trans, seats, price, image_blob FROM cars ORDER BY carmaker, model")
        cars = cursor.fetchall()

    cars_list = []
    for car in cars:
        car = list(car)  # Convert the tuple to a list to allow modification
        if car[8]:  # Check if `image_blob` is not None
            try:
                car_image_base64 = base64.b64encode(car[8]).decode('utf-8')
                car.append(car_image_base64)
                # Uncomment line below for terminal debugging
                # print(f"Base64 Image Data for Car {car[0]}: {car_image_base64[:100]}...")
            except Exception as e:
                print(f"Error encoding image for Car {car[0]}: {e}")
                car.append(None)
        else:
            # Add None for cars without an image
            car.append(None)
        cars_list.append(car)

    paginator = Paginator(cars_list, 5)
    page = request.GET.get('page')
    try:
        cars_page = paginator.page(page)
    except PageNotAnInteger:
        cars_page = paginator.page(1)
    except EmptyPage:
        cars_page = paginator.page(paginator.num_pages)

    return render(request, 'vehicles.html', {'cars': cars_page})


def index(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT carid, carmaker, model, type, fuel, trans, seats, price, image_blob FROM cars ORDER BY carmaker, model")
        cars = cursor.fetchall()

    cars_list = []
    for car in cars:
        car = list(car)  # Convert the tuple to a list to allow modification
        if car[8]:  # Check if `image_blob` is not None
            try:
                car_image_base64 = base64.b64encode(car[8]).decode('utf-8')
                car.append(car_image_base64)
                # Uncomment line below for terminal debugging
                # print(f"Base64 Image Data for Car {car[0]}: {car_image_base64[:100]}...")
            except Exception as e:
                print(f"Error encoding image for Car {car[0]}: {e}")
                car.append(None)
        else:
            # Add None for cars without an image
            car.append(None)
        cars_list.append(car)

    paginator = Paginator(cars_list, 3)
    page = request.GET.get('page')
    try:
        cars_page = paginator.page(page)
    except PageNotAnInteger:
        cars_page = paginator.page(1)
    except EmptyPage:
        cars_page = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'cars': cars_page})

def indexcars(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT carid, carmaker, model, type, fuel, trans, seats, price, image_blob FROM cars ORDER BY carmaker, model")
        cars = cursor.fetchall()

    cars_list = []
    for car in cars:
        car = list(car)  # Convert the tuple to a list to allow modification
        if car[8]:  # Check if `image_blob` is not None
            try:
                car_image_base64 = base64.b64encode(car[8]).decode('utf-8')
                car.append(car_image_base64)
                # Uncomment line below for terminal debugging
                # print(f"Base64 Image Data for Car {car[0]}: {car_image_base64[:100]}...")
            except Exception as e:
                print(f"Error encoding image for Car {car[0]}: {e}")
                car.append(None)
        else:
            # Add None for cars without an image
            car.append(None)
        cars_list.append(car)

    paginator = Paginator(cars_list, 3)
    page = request.GET.get('page')
    try:
        cars_page = paginator.page(page)
    except PageNotAnInteger:
        cars_page = paginator.page(1)
    except EmptyPage:
        cars_page = paginator.page(paginator.num_pages)

    return render(request, 'indexcars.html', {'cars': cars_page})

def support(request):
    return render(request, 'support.html')

def support_submit(request):
    return render(request, 'support_submit.html')


"""def serve_image(request, car_id):
    # Retrieve the car object by car_id
    car = get_object_or_404(Car, carid=car_id)
    car_photo = car.image_blob

    # Check file extension to determine MIME type
    content_type, encoding = mimetypes.guess_type(car_photo.name)
    if not content_type:
        content_type = 'application/octet-stream'  # Default to binary stream if MIME type is unknown

    # Open the image file and return it as an HTTP response
    with car_photo.open('rb') as img_file:
        response = HttpResponse(img_file.read(), content_type=content_type)

    return response
    """


def serve_image(request, car_id):
    # Fetch the car record from the database using raw SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT carid, carmaker, model, type, fuel, trans, seats, price, image_blob FROM cars WHERE carid = %s", [car_id])
        car_data = cursor.fetchone()  # This will return a tuple

    if car_data:
        image_data = car_data[7]  # Image data is assumed to be at index 7 (8th element in the tuple)
        
        # Return the image as an HttpResponse with the correct content type
        response = HttpResponse(image_data, content_type="image/webp")
        return response
    else:
        # Handle case where no car was found with the given car_id
        return HttpResponse(status=404)

    
def show_car_photo(request, car_id):
    # Retrieve the car object by car_id
    car = get_object_or_404(Car, carid=car_id)
    car_photo = car.image_blob
    response = HttpResponse(car_photo, content_type="image/webp")
    return response

    # Check if the car has an image stored in the database
    #if car.image_blob:
     #   # Serve the image stored as binary data in the image_url field
      #  response = HttpResponse(car.image_blob, content_type="image/webp")  # You can adjust this based on the image type
       # return response
    #else:
     #   return HttpResponse(car_id, status=404)