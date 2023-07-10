from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index, name="expenses"),
    path("add/",views.addExpense, name="add-expenses"),
    path("edit/<int:id>/", views.expense_edit, name="expense-edit"), 
    path("delete/<int:id>/", views.delete_expense, name="expense-delete"),
    path("search/", csrf_exempt(views.search_expenses), name="search-expenses"),
    path("category/summary/<int:opt>/", views.expense_category_summary, name="expense_category_summary"),
    path("stats/", views.stats_view, name="stats"),
]
