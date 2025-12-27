from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import date

class AddBudget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Main Budget")  # 👈 new field
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('completed', 'Completed'),
        ],
        default='active'
    )

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

    def is_expired(self):
        """True if the budget end date has passed."""
        return self.end_date < date.today()


    def auto_update_status(self):
        """Automatically set status to completed when expired."""
        if self.is_expired() and self.status != "completed":
            self.status = "completed"
            self.save(update_fields=["status"])



