from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
import json
from .models import UserPreferences


# Create your views here
@login_required(login_url='/auth/login/')
def index(request):
    exists = UserPreferences.objects.filter(user=request.user).exists()
    user_preferences = None 

    if exists:
        user_preferences = UserPreferences.objects.get(user=request.user)

    
    if request.method == "GET":
        currency_data = []

        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        
        with open(file_path, 'r') as json_file:
            
            data = json.load(json_file)

            for key, value in data.items():
                currency_data.append({'name':key,'value':value})
            
            # Debugging
            # import pdb
            # pdb.set_trace()

        return render(request, 'preferences/index.html', context={'currencies':currency_data, "user_preferences": user_preferences})
    
    else:
        currency = request.POST['currency']

        if exists: 
            currency = request.POST['currency']
            user_preferences.currency = currency
            user_preferences.save()
        else: 
            UserPreferences.objects.create(user=request.user, currency=currency)
        
        messages.success(request, 'Changes saved')
        return redirect('preferences')