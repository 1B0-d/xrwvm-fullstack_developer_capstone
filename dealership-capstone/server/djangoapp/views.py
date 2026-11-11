# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.views.decorators.http import require_GET, require_POST
import logging
import json
from urllib.parse import quote
import requests
from .restapis import get_request, analyze_review_sentiments, post_review
from .models import CarMake, CarModel
from .populate import initiate
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)

def get_cars(request):
    if not CarMake.objects.exists():
        initiate()
    cars = [{'CarModel': car.name, 'CarMake': car.car_make.name}
            for car in CarModel.objects.select_related('car_make')]
    return JsonResponse({'CarModels': cars})


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
@require_POST
def login_user(request):
    # Get username and password from request.POST dictionary
    try:
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
    except (ValueError, KeyError, TypeError):
        return JsonResponse({'error': 'Invalid request'}, status=400)
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

@require_GET
def logout_request(request):
    logout(request)
    return JsonResponse({'userName': ''})

# Create a `registration` view to handle sign up request
@csrf_exempt
@require_POST
def registration(request):
    try:
        data = json.loads(request.body)
        username = data['userName'].strip()
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']
        if not username or not password:
            raise ValueError('Empty username or password')
    except (ValueError, KeyError, TypeError, AttributeError):
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        with transaction.atomic():
            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name, email=email)
    except IntegrityError:
        return JsonResponse({'userName': username, 'error': 'Already Registered'})
    login(request, user)
    return JsonResponse({'userName': username, 'status': 'Authenticated'})


@require_GET
def get_dealerships(request, state='All'):
    endpoint = '/fetchDealers' if state == 'All' else '/fetchDealers/' + quote(state, safe='')
    try:
        return JsonResponse({'status': 200, 'dealers': get_request(endpoint)})
    except (requests.RequestException, ValueError):
        return JsonResponse({'status': 502, 'message': 'Backend unavailable'}, status=502)


@require_GET
def get_dealer_details(request, dealer_id):
    try:
        return JsonResponse({'status': 200, 'dealer': get_request('/fetchDealer/' + str(dealer_id))})
    except (requests.RequestException, ValueError):
        return JsonResponse({'status': 502, 'message': 'Backend unavailable'}, status=502)


@require_GET
def get_dealer_reviews(request, dealer_id):
    try:
        reviews = get_request('/fetchReviews/dealer/' + str(dealer_id))
        for review in reviews:
            review['sentiment'] = analyze_review_sentiments(review['review'])['sentiment']
        return JsonResponse({'status': 200, 'reviews': reviews})
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return JsonResponse({'status': 502, 'message': 'Backend unavailable or invalid response'}, status=502)


@csrf_exempt
@require_POST
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 403, 'message': 'Unauthorized'}, status=403)
    try:
        data = json.loads(request.body)
        if not isinstance(data, dict):
            raise ValueError('Expected object')
    except (ValueError, TypeError):
        return JsonResponse({'status': 400, 'message': 'Invalid request'}, status=400)
    try:
        post_review(data)
        return JsonResponse({'status': 200})
    except (requests.RequestException, ValueError):
        return JsonResponse({'status': 502, 'message': 'Error in posting review'}, status=502)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
