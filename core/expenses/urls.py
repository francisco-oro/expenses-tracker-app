from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(views.index), name="expenses"),
    path("add/",views.addExpense, name="add-expenses"),
    path("edit/<int:id>/", views.expense_edit, name="expense-edit"), 
    path("delete/<int:id>/", views.delete_expense, name="expense-delete"),
    path("search/", csrf_exempt(views.search_expenses), name="search-expenses"),
    path("category/summary/<int:opt>/", views.expense_category_summary, name="expense_category_summary"),
    path("stats/", views.stats_view, name="stats"),
    path("dashboard/",views.dashboard_view, name="dashboard"),
    path("expenses/export/csv/<int:opt>/", views.export_csv, name="expenses-export-csv"),
    path("expenses/export/xls/<int:opt>/", views.export_xlx, name="expenses-export-xls"),
    path("expenses/export/pdf/<int:opt>/", views.export_pdf, name="expenses-export-pdf"),
    path("expenses/tracker/<int:opt>/", views.timeline_expenses_tracker, name="expenses-tracker"),
]
