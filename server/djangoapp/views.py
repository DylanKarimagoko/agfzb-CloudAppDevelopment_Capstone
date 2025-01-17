from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .models import CarModel
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request,"djangoapp/contact.html")

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')
# ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")
# ...

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request,"djangoapp/registration.html",context)
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        user_exist = False
        print("here")
        try:
            
            User.objects.get(username=username)
            user_exist = True
        except:
           
            logger.debug("{} is new user".format(username))
        if not user_exist:
        
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://dylankarimag-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context = {}
        context["dealerships_list"] = dealerships
        # Return a list of dealer short name
        return render(request,'djangoapp/index.html',context )

def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://dylankarimag-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        reviews = get_dealer_reviews_from_cf(url,dealer_id)
        print(reviews)
        context = {}
        context['reviews_list'] = reviews
        context['id'] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):

def add_review(request, dealer_id):
    print("hello")
    if request.method == 'GET':
        cars = CarModel.objects.all()
        context = {}
        context['cars'] = cars
        context['id'] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        username = request.user.username
        purchase = request.POST.get('purchased')
        print(purchase)
        review = {}
        car_id = request.POST.get("car")
        car = CarModel.objects.get(pk=car_id)
        review["name"] = username
        review['id'] = dealer_id
        review['dealership'] = dealer_id
        review['review'] = request.POST.get('review')
        review['purchase'] = False
        if purchase == 'on':
            review['purchase'] = True
            review['purchase_date'] = request.POST.get('date')
            review['car_make'] = car.car_make.name
            review['car_model'] = "Car"
            review['car_year'] = int(car.year.strftime("%Y"))
        #print(payload)
        url = "https://dylankarimag-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
        post_request(url, review, id=dealer_id)
        return redirect('djangoapp:dealer', dealer_id=dealer_id)
# ...

