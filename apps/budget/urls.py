from django.urls import path
from .views import budget_list, budget_completed_view, set_budget, edit_budget, delete_budget, add_expense_with_budget, view_expense_with_budget, view_completed_budget_expenses

urlpatterns = [
    # main list page (shows all budgets)
    path('', budget_list, name="budget_list"),
    path('budget_completed/', budget_completed_view, name="budget_completed"),


    # create a new budget
    path('add/', set_budget, name="set_budget"),
    

    # edit or delete specific budget
    path('<int:budget_id>/edit/', edit_budget, name="edit_budget"),
    path('<int:budget_id>/delete/', delete_budget, name="delete_budget"),

    # add expense with budget
    path('<int:budget_id>/add-expense-with-budget', add_expense_with_budget, name="add_expense_with_budget"),
    path('<int:budget_id>/view-expense-with-budget', view_expense_with_budget, name="view_expense_with_budget"),
    path('budget/<int:budget_id>/completed-expenses/', view_completed_budget_expenses, name='view_completed_budget_expenses'),


]
