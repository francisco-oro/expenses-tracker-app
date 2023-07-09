from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import *
from .serializers import *
import json
from userpreferences.models import UserPreferences
# Create your views here.

def search_expenses(request):
     if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner = request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner= request.user)
        
        data = expenses.values()
        
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/auth/login/')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)

    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    
    # User customized settings 

    try:
        currency = UserPreferences.objects.get(user=request.user).currency
    except ObjectDoesNotExist:
         messages.info(request, "Please take a moment to set your preferences at the account section")
         return redirect('preferences')


    context = {
          'expenses': expenses,
          "page_obj": page_obj,
          "currency": currency,
    }

    return render(request, 'expenses/index.html', context)

def addExpense(request):

    categories = Category.objects.all()

    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == "GET": 
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        try: 
            category = request.POST['category']
        except:
             messages.error(request, "Please add a valid category")
             return render(request, 'expenses/add_expense.html')
        

        if not amount: 
            messages.error(request, "Amount is required")
            return render(request, 'expenses/add_expense.html', context)
        
        if not description: 
            messages.error(request, "Description is required")
            return render(request, 'expenses/add_expense.html', context)
        
        try:
            Expense.objects.create(owner=request.user,amount=amount, date=date, category=category, description=description)
        
        except Exception as e:
                        messages.error(request, "Please enter a valid date")
                        return render(request, 'expenses/add_expense.html', context)
        
        messages.success(request, "Record inserted successfully")
        return redirect('expenses')
    

def expense_edit(request, id):
     expense = Expense.objects.get(pk=id)
     categories = Category.objects.all()
     context = {
          'expense': expense,
          'values': expense,
          "categories": categories,
     }

     if request.method == 'GET':
          return render(request, 'expenses/edit-instance.html', context)
     
     if request.method == 'POST': 
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']

        try: 
            category = request.POST['category']
        except:
             messages.error(request, "Please add a valid category")
             return render(request, 'expenses/edit-instance.html')
        

        if not amount: 
            messages.error(request, "Amount is required")
            return render(request, 'expenses/edit-instance.html', context)
        
        if not description: 
            messages.error(request, "Description is required")
            return render(request, 'expenses/edit-instance.html', context)
        
        
        if expense.owner != request.user:
             messages.error(request, 'This record belongs to another account')
             return render(request, 'expenses/edit-instance.html', context)

        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        try: 
            expense.save()
        except: 
            messages.error(request, "Please enter a valid date")
            return render(request, 'expenses/edit-instance.html', context)
         
        messages.success(request, "Record updated successfully")
        return redirect('expenses')
     

def delete_expense(request, id):
     expense = Expense.objects.get(pk=id)
     if request.user == expense.owner: 
        if expense:
            expense.delete()
            messages.success(request, "Record succesfully removed")
            return redirect('expenses')
        
     messages.error(request, "Cannot delete that record")
     return redirect('expenses')