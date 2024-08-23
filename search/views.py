import requests
from django.http import JsonResponse
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm

def custom_404_view(request, exception):
    return redirect(f'{settings.LOGIN_URL}')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            loginuser = authenticate(request, username=username, password=password)
            
            if loginuser is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to a home page or dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'search/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'search/dashboard.html')

def register_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.usable_password = True
            messages.success(request, 'Account was created.')
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'search/register.html', {'form': form})

def search_foods(request):
    query = request.GET.get('query', '')
    if query:
        api_key = settings.API_KEY
        base_url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
        params = {
            'api_key': api_key,
            'query': query,
            'pageSize': 25  # Limit the number of results for dropdown
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            foods = data.get('foods', [])
            return JsonResponse([{'description': food['description'], 'id': food['fdcId']} for food in foods], safe=False)
    return JsonResponse([], safe=False)

def search_nutrition(request):
    query = request.GET.get('query', '')
    if query:
        api_key = settings.API_KEY
        base_url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
        params = {
            'api_key': api_key,
            'query': query,
            'pageSize': 1  # Limit the number of results for dropdown
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            foods = data.get('foods', [])
            food = data['foods'][0]

            calories = "N/A"
            sugar = "N/A"
            fibre = "N/A"
            protein = "N/A"
            fat = "N/A"
            carbohydrates = "N/A"

            myData = {}
            nutrientsList = (food['foodNutrients'])

            myData['name'] = food['description']
            myData['nutrients'] = []
            for nutrient in nutrientsList:
                name = nutrient['nutrientName']
                if (
                    (
                        name == "Total Sugars"
                        or name == "Energy"
                        or name == "Protein"
                        or "Sodium" in name
                        or "Carbohydrate" in name
                        or "fat" in name
                        or "Fibre" in name

                    )
                ):
                
                    newNutrientDict = {}
                    newNutrientDict['name'] = nutrient['nutrientName']
                    newNutrientDict['amount'] = str(nutrient['value'])
                    newNutrientDict['units'] = nutrient['unitName'].lower()
                    myData['nutrients'].append(newNutrientDict)
            return JsonResponse(myData, safe=False)


