from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import AddRecord
from django.db.models import Sum
from dashboard.utlis import filter_records_by_period
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
from budget.models import AddBudget

# Create your views here.

@login_required
def record_view(request):
    user= request.user

    # retrive all records belonging to logged in user
    record_list = AddRecord.objects.filter(user=user)

    if 'time_period' in request.POST:
        time_period = request.POST.get("time_period")
    else:
        time_period = "all_records"    
    
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    
    # filter records with selected time period
    filter_record = filter_records_by_period(record_list, time_period, start_date, end_date)
    filter_record = filter_record.order_by('-created_at')

    # Cards values
    total_income = filter_record.filter(type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = filter_record.filter(type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_balance = total_income - total_expenses

    if total_income or total_expenses > 0:
        income_percent = (total_income / (total_income + total_expenses)) * 100
        expense_percent = 100 - income_percent
    else:
        income_percent = 0
        expense_percent = 0 

    context ={
        'recent_records' : filter_record,
        'total_balance' : total_balance,
        'total_income' : total_income,
        'total_expenses' : total_expenses,
        'time_period' : time_period,
        'income_percent': round(income_percent, 2),
        'expense_percent': round(expense_percent, 2),
    }
    return render(request, 'record/record.html', context)


# add records
@login_required
def add_record(request):
    user = request.user


    if request.method == 'POST':
        date_ = request.POST.get('date')
        type_ = request.POST.get('type')
        category = request.POST.get('category')
        description = request.POST.get('description', '')
        amount = request.POST.get('amount')

    # Add record if record fields are present
        if date_ and type_ and category and amount:
            AddRecord.objects.create(
                user=user,
                date=date_,
                type=type_,
                category=category,
                description=description,
                amount=float(amount)
            )

            return redirect('record_list')
    return render(request, 'record/add_record.html')


# edit records
@login_required
def edit_record(request, record_id):
    record = get_object_or_404(AddRecord, id=record_id, user=request.user)

    if request.method == 'POST':
        record.date = request.POST.get('date')
        record.type = request.POST.get('type')
        record.category = request.POST.get('category')
        record.description = request.POST.get('description')
        record.amount = request.POST.get('amount')
        record.save()
        return redirect('record_list')
    return render(request, 'record/edit_record.html', {'record':record})


# delete records
@login_required
def delete_record(request, record_id):
    record = get_object_or_404(AddRecord, id=record_id, user=request.user)
    if request.method == 'POST':
        record.delete()  
        return redirect('record_list')
    return render(request, 'record/delete_record.html')




@login_required
def download_pdf(request):
    user = request.user

    if request.method == 'POST':
        records_list = AddRecord.objects.filter(user=user)
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')

        from_date = datetime.strptime(from_date_str, "%Y-%m-%d").date()
        to_date = datetime.strptime(to_date_str, "%Y-%m-%d").date()

        records = filter_records_by_period(
            record_list=records_list,
            time_period='custom',
            start_date=from_date,
            end_date=to_date
        )

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="FinTrack_{from_date}_to_{to_date}.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        p.setFont("Helvetica-Bold", 16)
        p.drawString(180, height - 50, "FinTrack - Records Report")

        p.setFont("Helvetica", 12)
        p.drawString(50, height - 80, f"Period: {from_date} to {to_date}")

        y = height - 120
        p.setFont("Helvetica-Bold", 11)
        headers = ["Date", "Type", "Category", "Description", "Amount"]
        x_positions = [50, 150, 250, 350, 480]

        for i, header in enumerate(headers):
            p.drawString(x_positions[i], y, header)

        p.line(45, y - 5, 550, y - 5)
        y -= 20
        p.setFont("Helvetica", 10)

        if not records.exists():
            p.drawString(50, y, "No records found in this date range.")
        else:
            for record in records:
                if y < 100:
                    p.showPage()
                    y = height - 120
                    p.setFont("Helvetica-Bold", 11)
                    for i, header in enumerate(headers):
                        p.drawString(x_positions[i], y, header)
                    p.line(45, y - 5, 550, y - 5)
                    y -= 20
                    p.setFont("Helvetica", 10)

                p.drawString(50, y, str(record.date))
                p.drawString(150, y, record.type)
                p.drawString(250, y, record.category)
                p.drawString(350, y, record.description[:30])
                p.drawString(480, y, str(record.amount))
                y -= 20

        p.showPage()
        p.save()
        return response
    
    return render(request, 'record/download_pdf.html')
