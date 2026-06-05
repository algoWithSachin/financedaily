from langchain.tools import tool
from apps.record.models import AddRecord


@tool
def get_last_records(user_id: int = 1, limit: int = 5):
    "return last records for user"

    records = AddRecord.objects.filter(
        user = user_id,
    ).order_by("-created_at")[:limit]

    result = []

    for r in records:
        result.append(
            {
                "date": str(r.date),
                "type": str(r.type),
                "category": str(r.category),
                "amount": int(r.amount),
            }
        )
    return str(result)