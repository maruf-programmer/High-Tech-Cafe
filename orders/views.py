from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.http import JsonResponse
from core.models import Table, Staff
from .models import WaiterCall, Order, Payment
import json


def call_waiter(request, table_id):
    table = get_object_or_404(Table, id=table_id, is_active=True)
    success = False
    reply_message = None

    if request.method == 'POST':
        reason = request.POST.get('reason', 'Mijoz chaqirdi')
        call = WaiterCall.objects.create(
            table=table,
            reason=reason,
        )
        # Barcha ofitsiantlarga SMS yuborish
        waiters = Staff.objects.filter(role='waiter', is_active=True)
        for waiter in waiters:
            waiter.send_sms(f"Stol {table.number} dan chaqiruv: {reason}")
            call.staff_phone += waiter.phone + ', '
        call.save()
        success = True

    # Agar javob kelgan bo'lsa
    latest_call = WaiterCall.objects.filter(table=table).order_by('-created_at').first()
    if latest_call and latest_call.reply_message:
        reply_message = latest_call.reply_message

    return render(request, 'orders/call_waiter.html', {
        'table': table,
        'table_id': table_id,
        'success': success,
        'reply_message': reply_message,
    })


@staff_member_required
def reply_to_call(request, call_id):
    """Ofitsiant tomonidan javob berish (AJAX)"""
    if request.method == 'POST':
        call = get_object_or_404(WaiterCall, id=call_id)
        message = request.POST.get('reply_message', '')
        call.reply_with_message(message)
        return JsonResponse({'status': 'success', 'message': 'Javob yuborildi'})
    return JsonResponse({'status': 'error'})


@staff_member_required
def mark_order_completed(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.status = 'completed'
        order.save()
        messages.success(request, 'Buyurtma yakunlandi')
    return redirect('core:my_orders', table_id=order.table.id)


def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if hasattr(order, 'payment'):
        payment = order.payment
    else:
        payment = None

    return render(request, 'orders/payment.html', {
        'order': order,
        'table_id': order.table.id,
        'payment': payment,
    })


def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        method = request.POST.get('method', 'cash')
        amount = order.total_price

        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={'amount': amount, 'method': method, 'status': 'pending'}
        )

        payment.method = method
        payment.transaction_id = f'TXN_{order.id}_{int(timezone.now().timestamp())}'

        # To'lovni simulyatsiya qilish
        if method == 'cash':
            payment.status = 'success'
            payment.completed_at = timezone.now()
        else:
            payment.status = 'success'
            payment.completed_at = timezone.now()

        payment.save()

        if payment.status == 'success':
            order.status = 'delivered'
            order.save()
            messages.success(request, 'To\'lov muvaffaqiyatli amalga oshirildi!')
        else:
            messages.error(request, 'To\'lovda xatolik yuz berdi')

        return redirect('orders:payment_page', order_id=order.id)

    return redirect('orders:payment_page', order_id=order.id)
