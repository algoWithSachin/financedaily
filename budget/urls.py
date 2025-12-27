from django.urls import path
from . import views

urlpatterns = [
    # main list page (shows all budgets)
    path('', views.budget_list, name="budget_list"),
    path('budget_completed/', views.budget_completed_view, name="budget_completed"),


    # create a new budget
    path('add/', views.set_budget, name="set_budget"),
    

    # edit or delete specific budget
    path('<int:budget_id>/edit/', views.edit_budget, name="edit_budget"),
    path('<int:budget_id>/delete/', views.delete_budget, name="delete_budget"),

    # add expense with budget
    path('<int:budget_id>/add-expense-with-budget', views.add_expense_with_budget, name="add_expense_with_budget"),
    path('<int:budget_id>/view-expense-with-budget', views.view_expense_with_budget, name="view_expense_with_budget"),
    path('budget/<int:budget_id>/completed-expenses/', views.view_completed_budget_expenses, name='view_completed_budget_expenses'),



]
