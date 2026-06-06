from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Table, Category, MenuItem, Advertisement
from orders.models import Order, OrderItem, Payment


def home(request):
    tables = Table.objects.filter(is_active=True)
    ads = Advertisement.objects.filter(is_active=True)
    
    # Statistika
    today = timezone.now().date()
    customers_today = Order.objects.filter(
        status='completed',
        completed_at__date=today
    ).count()

    # Taomlar statistikasi
    all_items = MenuItem.objects.filter(is_available=True).order_by('price')
    cheapest_item = all_items.first()
    expensive_item = all_items.last()
    popular_items = MenuItem.objects.filter(is_available=True, is_popular=True)[:3]

    free_tables = tables.filter(status='free').count()
    occupied_tables = tables.filter(status='occupied').count()

    return render(request, 'core/home.html', {
        'tables': tables,
        'ads': ads,
        'free_tables': free_tables,
        'occupied_tables': occupied_tables,
        'customers_today': customers_today,
        'cheapest_item': cheapest_item,
        'expensive_item': expensive_item,
        'popular_items': popular_items,
    })


def menu(request, table_id):
    table = get_object_or_404(Table, id=table_id, is_active=True)

    # Stolni band qilish
    if table.status == 'free':
        table.occupy()
        messages.success(request, f'Stol #{table.number} band qilindi. Xush kelibsiz!')
    elif table.status == 'cleaning':
        messages.warning(request, 'Stol tozalanmoqda, iltimos kuting...')
        return redirect('core:home')

    categories = Category.objects.filter(is_active=True).prefetch_related('items')
    cart_count = len(request.session.get(f'cart_{table_id}', []))

    return render(request, 'core/menu.html', {
        'table': table,
        'categories': categories,
        'table_id': table_id,
        'cart_count': cart_count,
    })


def item_detail(request, table_id, item_id):
    table = get_object_or_404(Table, id=table_id, is_active=True)
    item = get_object_or_404(MenuItem, id=item_id, is_available=True)

    serving_options = item.serving_options if item.serving_options else [1, 2, 3, 4, 5]

    return render(request, 'core/item_detail.html', {
        'table': table,
        'item': item,
        'table_id': table_id,
        'serving_options': serving_options,
    })


def add_to_cart(request, table_id, item_id):
    table = get_object_or_404(Table, id=table_id, is_active=True)
    item = get_object_or_404(MenuItem, id=item_id, is_available=True)

    if request.method == 'POST':
        cart = request.session.get(f'cart_{table_id}', [])
        servings = int(request.POST.get('servings', 1))
        quantity = int(request.POST.get('quantity', 1))
        notes = request.POST.get('notes', '')

        cart.append({
            'item_id': item.id,
            'name': item.name,
            'price': str(item.price),
            'servings': servings,
            'quantity': quantity,
            'notes': notes,
        })

        request.session[f'cart_{table_id}'] = cart
        request.session.modified = True
        messages.success(request, f'{item.name} savatga qo\'shildi!')

    return redirect('core:item_detail', table_id=table_id, item_id=item_id)


def remove_from_cart(request, table_id, cart_index):
    if request.method == 'POST':
        cart = request.session.get(f'cart_{table_id}', [])
        if 0 <= cart_index < len(cart):
            cart.pop(cart_index)
            request.session[f'cart_{table_id}'] = cart
            request.session.modified = True
            messages.success(request, 'Taom savatdan olib tashlandi')
    return redirect('core:cart', table_id=table_id)


def cart(request, table_id):
    table = get_object_or_404(Table, id=table_id, is_active=True)
    cart = request.session.get(f'cart_{table_id}', [])

    cart_items = []
    total = 0
    for idx, c in enumerate(cart):
        subtotal = float(c['price']) * c['quantity'] * c['servings']
        cart_items.append({
            'index': idx,
            'menu_item': type('obj', (object,), {
                'id': c['item_id'],
                'name': c['name'],
                'price': c['price'],
                'image': None,
                'prep_time_display': '',
                'servings': c['servings'],
                'quantity': c['quantity'],
                'subtotal': subtotal,
                'notes': c.get('notes', ''),
            })(),
        })
        total += subtotal

    return render(request, 'core/cart.html', {
        'table': table,
        'table_id': table_id,
        'cart_items': cart_items,
        'total_price': f"{total:,.0f}",
    })


def checkout(request, table_id):
    table = get_object_or_404(Table, id=table_id, is_active=True)
    cart = request.session.get(f'cart_{table_id}', [])

    if not cart:
        messages.error(request, 'Savat bo\'sh!')
        return redirect('core:cart', table_id=table_id)

    order = Order.objects.create(
        table=table,
        status='pending',
        notes=request.POST.get('notes', ''),
    )

    for c in cart:
        menu_item = MenuItem.objects.get(id=c['item_id'])
        OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=c['quantity'],
            servings=c['servings'],
            price_per_serving=menu_item.price,
            notes=c.get('notes', ''),
        )

    order.update_total()

    del request.session[f'cart_{table_id}']
    request.session.modified = True

    messages.success(request, 'Buyurtma qabul qilindi! Iltimos kuting...')
    return redirect('core:my_orders', table_id=table_id)


def my_orders(request, table_id):
    table = get_object_or_404(Table, id=table_id, is_active=True)
    orders = Order.objects.filter(table=table).order_by('-created_at')

    return render(request, 'core/my_orders.html', {
        'table': table,
        'table_id': table_id,
        'orders': orders,
    })


def complete_session(request, table_id):
    """Stol yakunlash - ofitsiant tomonidan"""
    table = get_object_or_404(Table, id=table_id)
    order_id = request.GET.get('order_id')

    if request.method == 'POST':
        if order_id:
            order = get_object_or_404(Order, id=order_id, table=table)
            order.complete_order()
        else:
            table.mark_free()

        messages.success(request, f'Stol #{table.number} bo\'shlashdi!')
        return redirect('core:home')

    return render(request, 'core/complete_session.html', {
        'table': table,
        'table_id': table_id,
        'orders': Order.objects.filter(table=table, status__in=['delivered', 'completed']),
    })
