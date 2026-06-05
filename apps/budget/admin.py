from django.contrib import admin
from .models import AddBudget

# Register your models here.
class AddBudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'start_date', 'end_date', 'amount', 'status')

admin.site.register(AddBudget, AddBudgetAdmin)