from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
from django.views.decorators.csrf import csrf_exempt
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def test(request):
    if request.method == "GET":
        return render(request, 'djangoapp/test.html')

# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            request.session['is_authenticated'] = True
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    if 'is_authenticated' in request.session:
        del request.session['is_authenticated']
    # Redirect user back to course list view
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://kulshrestha4-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ','.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context = {
            "dealer_names": dealer_names,
            }
        return  HttpResponse(dealer_names)
    return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://kulshrestha4-5000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        # Get dealers from the URL
        dealerships = get_dealer_reviews_from_cf(url, id=dealer_id)
        # Concat all dealer's short name
        reviews = ',\n'.join([f"{dealer.review}\n Sentiment: {dealer.sentiment}" for dealer in dealerships])
        # Return a list of dealer short named
        context = {
            "reviews": reviews,
            }
        return HttpResponse(reviews)
    return render(request, 'djangoapp/index.html', context)

@csrf_exempt 
def add_review(request, dealer_id):
    if request.method == 'POST':

        url = "https://kulshrestha4-5000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
        
        name = request.POST.get('name')
        dealership = request.POST.get('dealership')
        review = request.POST.get('review')
        purchase = request.POST.get('purchase')
        purchase_date = request.POST.get('purchase_date')
        car_make = request.POST.get('car_make')
        car_model = request.POST.get('car_model')
        car_year = request.POST.get('car_year')
    
        json_payload = {
            'id': dealer_id, 
            'name': name, 
            'dealership': dealership, 
            'review': review, 
            'purchase': purchase, 
            'purchase_date': purchase_date, 
            'car_make': car_make, 
            'car_model': car_model, 
            'car_year': car_year
        }

        try:
            # Set the Content-Type header to 'application/json'
            headers = {'Content-Type': 'application/json'}

            # Send a POST request with JSON data
            response = requests.post(url, json_payload=json_payload, headers=headers)

            if response.status_code == 200:
                # Assuming the external API returns a JSON response
                response_data = response.json()
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Failed to post review to the external API'})
        except Exception as e:
            # Handle any exceptions that may occur during the request
            return JsonResponse({'error': f'An error occurred: {str(e)}'})

    return JsonResponse({'error': 'Only POST requests are allowed'})

