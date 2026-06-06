from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from core.models import Table, Staff, Category, MenuItem
from orders.models import Order, OrderItem, WaiterCall
from feedback.models import Feedback


@staff_member_required
def dashboard(request):
    # Basic stats
    total_tables = Table.objects.count()
    free_tables = Table.objects.filter(status='free').count()
    occupied_tables = Table.objects.filter(status='occupied').count()
    total_staff = Staff.objects.filter(is_active=True).count()

    # Orders
    pending_orders = Order.objects.exclude(status__in=['completed', 'cancelled']).count()
    today_completed = Order.objects.filter(
        status='completed',
        completed_at__date=timezone.now().date()
    ).count()

    # Waiter calls
    waiter_calls_count = WaiterCall.objects.filter(is_answered=False).count()

    # Lists for dashboard
    pending_orders_list = Order.objects.exclude(
        status__in=['completed', 'cancelled']
    ).select_related('table').order_by('-created_at')[:5]

    waiter_calls_list = WaiterCall.objects.filter(is_answered=False).select_related('table').order_by('-created_at')[:5]

    active_tables = Table.objects.filter(status='occupied').order_by('-current_session_start')[:5]

    recent_feedback = Feedback.objects.all().select_related('table').order_by('-created_at')[:5]

    context = {
        'total_tables': total_tables,
        'free_tables': free_tables,
        'occupied_tables': occupied_tables,
        'total_staff': total_staff,
        'pending_orders': pending_orders,
        'today_completed': today_completed,
        'waiter_calls_count': waiter_calls_count,
        'pending_orders_list': pending_orders_list,
        'waiter_calls_list': waiter_calls_list,
        'active_tables': active_tables,
        'recent_feedback': recent_feedback,
    }

    return render(request, 'staff/dashboard.html', context)


@staff_member_required
def order_list(request):
    status_filter = request.GET.get('status')
    orders = Order.objects.all().select_related('table').prefetch_related('items__menu_item')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    else:
        # By default show active orders
        orders = orders.exclude(status__in=['completed', 'cancelled'])

    return render(request, 'staff/orders.html', {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status_filter
    })


@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            if new_status == 'completed':
                order.complete_order()
            order.save()
            messages.success(request, f"Buyurtma #{order.id} holati '{order.get_status_display()}'ga o'zgartirildi.")
    
    return redirect(request.META.get('HTTP_REFERER', 'core:staff_orders'))


@staff_member_required
def waiter_calls(request):
    calls = WaiterCall.objects.all().select_related('table').order_by('-is_answered', '-created_at')
    return render(request, 'staff/calls.html', {'calls': calls})


@staff_member_required
def resolve_call(request, call_id):
    call = get_object_or_404(WaiterCall, id=call_id)
    if request.method == 'POST':
        message = request.POST.get('reply_message', 'Xodim yo\'lda')
        call.reply_with_message(message)
        messages.success(request, f"Stol #{call.table.number} chaqiruviga javob berildi.")
    return redirect('core:staff_calls')


@staff_member_required
def menu_management(request):
    categories = Category.objects.all().prefetch_related('items')
    return render(request, 'staff/menu.html', {'categories': categories})


@staff_member_required
def menu_item_add(request):
    if request.method == 'POST':
        # Simple implementation for brevity, normally you'd use a Form
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description', '')
        
        category = get_object_or_404(Category, id=category_id)
        MenuItem.objects.create(
            name=name,
            category=category,
            price=price,
            description=description,
            is_available=True
        )
        messages.success(request, f"'{name}' menyuga qo'shildi.")
        return redirect('core:staff_menu')
    
    categories = Category.objects.all()
    return render(request, 'staff/menu_item_form.html', {'categories': categories})


@staff_member_required
def menu_item_edit(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.category_id = request.POST.get('category')
        item.price = request.POST.get('price')
        item.description = request.POST.get('description', '')
        item.is_available = 'is_available' in request.POST
        item.save()
        messages.success(request, f"'{item.name}' tahrirlandi.")
        return redirect('core:staff_menu')
    
    categories = Category.objects.all()
    return render(request, 'staff/menu_item_form.html', {'item': item, 'categories': categories})


@staff_member_required
def table_management(request):
    tables = Table.objects.all().order_by('number')
    return render(request, 'staff/tables.html', {'tables': tables})


@staff_member_required
def update_table_status(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Table.STATUS_CHOICES):
            table.status = new_status
            if new_status == 'free':
                table.current_session_start = None
            elif new_status == 'occupied' and not table.current_session_start:
                table.current_session_start = timezone.now()
            table.save()
            messages.success(request, f"Stol #{table.number} holati yangilandi.")
    
    return redirect('core:staff_tables')


@staff_member_required
def add_table(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        if number:
            if Table.objects.filter(number=number).exists():
                messages.error(request, f"Stol #{number} allaqachon mavjud.")
            else:
                Table.objects.create(number=number)
                messages.success(request, f"Stol #{number} muvaffaqiyatli qo'shildi.")
        else:
            messages.error(request, "Stol raqamini kiriting.")
    
    return redirect('core:staff_tables')
