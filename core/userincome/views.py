from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from rest_framework import status
from .models import *
import json
from userpreferences.models import UserPreferences
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table, TableStyle, colors
import datetime
import pdb
import xlwt
import csv

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
     start_from = today - datetime.timedelta(days=opt)

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

def timeline_income_tracker(request, opt):
    try:
        calendar = []
        today = datetime.datetime.today()
        start_from = today - datetime.timedelta(days=opt)
         
        expenses = UserIncome.objects.filter(date__gte=start_from, date__lte=today, owner=request.user)
        
        if opt >= 60:
            count = [0] * (opt // 30)

            for i in range(opt // 30):
                 
                 start_month = today - datetime.timedelta(days=(opt - (i * 30)))
                 end_month = today - datetime.timedelta(days=(opt - ((i + 1) * 30 - 1)))

                 monthly_expenses = expenses.filter(date__gte=start_month, date__lte=end_month)
                 total_expenses = monthly_expenses.aggregate(total_amount=Sum('amount'))['total_amount']

                 count[i] = total_expenses or 0
                 formatted_month = start_month.strftime("%B")
                 
                 calendar.append(formatted_month)
        
        else:
            count = [0] * opt
             
            for i in range(opt):    

                current_day_expenses = expenses.filter(date=start_from)
                count[i] = sum(expense.amount for expense in current_day_expenses)
                
                if opt >= 30:
                    formatted_date = start_from.strftime("%d/%m/%Y")
                else:
                    formatted_date = start_from.strftime("%A")
                calendar.append(formatted_date)
                start_from += datetime.timedelta(days=1)
         
        content = {
            'count': count,
            'tags': calendar
        }

        return JsonResponse(content)
    except Exception:
        return HttpResponse('You must provide a valid days count', status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/auth/login/')
def stats_view(request):
     return render(request, 'income/stats.html')


# Exporting views
def export_csv(request, opt):
    today = datetime.datetime.today()
    start_from = today - datetime.timedelta(days=opt)

    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_from_{start_from}_to_{datetime.datetime.today()}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Source', 'Date'])

    income = UserIncome.objects.filter(owner=request.user, date__gte = start_from, date__lte = today)

    for instance in income:
        writer.writerow([instance.amount, instance.description, instance.source, instance.date])


def export_xlx(request, opt):
    today = datetime.datetime.today()
    start_from = today - datetime.timedelta(days=opt)

    response = HttpResponse(content_type = 'application/mx-excel')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_from_{start_from}_to_{datetime.datetime.today()}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Source', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()

    rows = UserIncome.objects.filter(owner = request.user, date__gte = start_from, date__lte = today).values_list('amount', 'description', 'source', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    
    return response

def export_pdf(request, opt):
    today = datetime.datetime.today()
    start_from = today - datetime.timedelta(days=opt)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_from_{start_from}_to_{datetime.datetime.today()}.pdf"'

    # Create the PDF object
    p = SimpleDocTemplate(response, pagesize=letter)
    # Set the column names
    columns = ['Amount', 'Description', 'Source', 'Date']
    table_data = [columns,]
    # Every element in rows is a tuple
    rows = UserIncome.objects.filter(owner=request.user, date__gte = start_from, date__lte = today).values_list('amount', 'description', 'source', 'date')
    for row in rows:
        table_data.append(row)
    
    c_width = [1*inch, 3.5*inch, 1.3*inch, 1*inch]
    t = Table(table_data, rowHeights=40, repeatRows=1, colWidths=c_width)
    # Note (0,0) references the top-left corner. Similarly, (-1, -1) references the bottom-right corner
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1, 0), colors.limegreen),]))

    elements = []
    elements.append(t)
    p.build(elements)


    return response