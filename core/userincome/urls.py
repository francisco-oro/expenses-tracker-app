from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index, name="income"),
    path("add/",views.add_income, name="add-income"),
    path("edit/<int:id>/", views.income_edit, name="income-edit"), 
    path("delete/<int:id>/", views.delete_income, name="income-delete"),
    path("search/", csrf_exempt(views.search_income), name="search-income")
]
