from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index, name="income"),
    path("add/",views.add_income, name="add-income"),
    path("edit/<int:id>/", views.income_edit, name="income-edit"), 
    path("delete/<int:id>/", views.delete_income, name="income-delete"),
    path("search/", csrf_exempt(views.search_income), name="search-income"),
    path("source/summary/<int:opt>/", views.income_source_summary, name="income_source_summary"),
    path("stats/", views.stats_view, name="income-stats"),
    path("export/csv/<int:opt>/", views.export_csv, name="income-export-csv"),
    path("export/xls/<int:opt>/", views.export_xlx, name="income-export-xls"),
    path("export/pdf/<int:opt>/", views.export_pdf, name="income-export-pdf"),
    path("tracker/<int:opt>/", views.timeline_income_tracker, name="income-tracker")
]   
