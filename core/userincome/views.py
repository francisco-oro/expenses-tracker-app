from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import *
import json
from userpreferences.models import UserPreferences
# Create your views here.
import datetime

def search_income(request):
     if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner = request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner= request.user)
        
        data = income.values()
        
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/auth/login/')
def index(request):
    source = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)

    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    
    # User customized settings 

    try:
        currency = UserPreferences.objects.get(user=request.user).currency
    except ObjectDoesNotExist:
         messages.info(request, "Please take a moment to set your preferences at the account section")
         return redirect('preferences')


    context = {
          'income': income,
          "page_obj": page_obj,
          "currency": currency,
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='/auth/login/')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == "GET": 
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']

        try: 
            source = request.POST['source']
        except:
             messages.error(request, "Please add a valid Source")
             return render(request, 'income/add_income.html')
        

        if not amount: 
            messages.error(request, "Amount is required")
            return render(request, 'income/add_income.html', context)
        
        if not description: 
            messages.error(request, "Description is required")
            return render(request, 'income/add_income.html', context)
        
        try:
            UserIncome.objects.create(owner=request.user,amount=amount, date=date, source=source , description=description)
        
        except Exception as e:
                        messages.error(request, "Please enter a valid date")
                        return render(request, 'income/add_income.html', context)
        
        messages.success(request, "Record inserted successfully")
        return redirect('income')
    
@login_required(login_url='/auth/login/')
def income_edit(request, id):
     income = UserIncome.objects.get(pk=id)
     sources = Source.objects.all()
     context = {
          'income': income,
          'values': income,
          "sources": sources,
     }

     if request.method == 'GET':
          return render(request, 'income/edit-income.html', context)
     
     if request.method == 'POST': 
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']

        try: 
            source = request.POST['source']
        except:
             messages.error(request, "Please add a valid Source")
             return render(request, 'income/edit-income.html', context)
        

        if not amount: 
            messages.error(request, "Amount is required")
            return render(request, 'income/edit-income.html', context)
        
        if not description: 
            messages.error(request, "Description is required")
            return render(request, 'income/edit-income.html', context)
        
        
        if income.owner != request.user:
             messages.error(request, 'This record belongs to another account')
             return render(request, 'income/edit-income.html', context)

        income.amount = amount
        income.date = date
        income.source = source
        income.description = description

        try: 
            income.save()
        except: 
            messages.error(request, "Please enter a valid date")
            return render(request, 'income/edit-income.html', context)
         
        messages.success(request, "Record updated successfully")
        return redirect('income')
     
@login_required(login_url='/auth/login/')
def delete_income(request, id):
     income = UserIncome.objects.get(pk=id)
     if request.user == income.owner: 
        if income:
            income.delete()
            messages.success(request, "Record succesfully removed")
            return redirect('income')
        
     messages.error(request, "Cannot delete that record")
     return redirect('income')

def income_source_summary(request, opt):

     today = datetime.date.today()

     if opt == 1:
        one_week_ago = today - datetime.timedelta(days=7)
        start_from = one_week_ago

     elif opt == 2:
        one_month_ago = today - datetime.timedelta(days=30)
        start_from = one_month_ago

     elif opt == 3:
        four_months_ago = today - datetime.timedelta(days=30*4)
        start_from = four_months_ago
     
     elif opt == 4:
        six_months_ago = today - datetime.timedelta(days=30*6)
        start_from = six_months_ago
     
     elif opt == 5:
        one_year_ago = today - datetime.timedelta(days=365)
        start_from = one_year_ago
     else:
         return JsonResponse({"error", "Invalid option key"}, safe=False)


     income = UserIncome.objects.filter(date__gte = start_from, date__lte = today, owner=request.user)
     
     income_summary = {}

     def get_source(income):
          return income.source
    
     def get_income_source_amount(income):
          amount = 0
          
          filtered_by_source = UserIncome.objects.filter(source=source)
          for item in filtered_by_source:
               amount += item.amount
          return amount


     source_list = list(set(map(get_source, income)))

     for item in income:
        for source in source_list:
             income_summary[source] = get_income_source_amount(source)

     return JsonResponse(income_summary, safe=False)

def stats_view(request):
     return render(request, 'income/stats.html')