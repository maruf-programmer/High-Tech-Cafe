from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Table
from .models import Feedback


def submit_feedback(request, table_id, order_id=0):
    table = get_object_or_404(Table, id=table_id, is_active=True)
    success = False

    if request.method == 'POST':
        rating = request.POST.get('rating')
        if rating:
            Feedback.objects.create(
                table=table,
                rating=int(rating),
                comment=request.POST.get('comment', ''),
                menu_item_name=request.POST.get('menu_item_name', ''),
                is_anonymous=request.POST.get('is_anonymous') == 'true',
            )
            success = True

    return render(request, 'feedback/submit.html', {
        'table': table,
        'table_id': table_id,
        'order_id': order_id,
        'success': success,
    })
