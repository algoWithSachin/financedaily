from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class AddBudget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Main Budget")  # 👈 new field
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s {self.name} ({self.start_date} - {self.end_date})"

    # helper functions
    def spent_amount(self):
        """Total expenses linked to this budget within its date range."""
        from record.models import AddRecord
        total = (
            AddRecord.objects.filter(
                user=self.user,
                budget=self,                       # ✅ Correct link
                type__iexact='Expense',             # ✅ Safer match
                date__range=(self.start_date, self.end_date)
            ).aggregate(total=Sum('amount'))['total'] or 0
        )
        return float(total)

    def remaining(self):
        return float(self.amount) - float(self.spent_amount())

    def used_percent(self):
        if self.amount == 0:
            return 0
        return (float(self.spent_amount()) / float(self.amount)) * 100




