from django.contrib import admin
from .models import UserIncome, Source
# Register your models here.
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'description', 'owner', 'source')
    search_field = ('amount', 'date', 'description', 'owner', 'source')

    list_per_page = 5    


admin.site.register(Source)
admin.site.register(UserIncome, IncomeAdmin)