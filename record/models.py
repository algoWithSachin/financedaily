from django.db import models
from django.contrib.auth.models import User
from budget.models import AddBudget

# Create your models here.
class AddRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(AddBudget, on_delete=models.SET_NULL, null=True, blank=True, related_name='records')
    date = models.DateField()
    type = models.CharField(max_length=10)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return   f"{self.user.username} - {self.type} - {self.category}"
