from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Order, OrderItem, WaiterCall, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)
    fields = ('menu_item', 'quantity', 'servings', 'price_per_serving', 'subtotal', 'notes')


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('transaction_id', 'status', 'completed_at')
    fields = ('method', 'amount', 'status', 'transaction_id', 'completed_at')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'colored_table', 'colored_status', 'total_price',
                    'item_count', 'wait_time', 'created_at')
    list_filter = ('status', 'table', 'created_at')
    search_fields = ('id', 'table__number', 'notes')
    readonly_fields = ('total_price', 'created_at', 'updated_at', 'completed_at',
                      'wait_time_display', 'session_duration')
    inlines = [OrderItemInline, PaymentInline]
    list_per_page = 20
    date_hierarchy = 'created_at'

    def order_number(self, obj):
        return f"#{obj.id}"
    order_number.short_description = 'Buyurtma'

    def colored_table(self, obj):
        return f'<span style="color: #00b894; font-weight: bold;">Stol {obj.table.number}</span>'
    colored_table.short_description = 'Stol'
    colored_table.allow_tags = True

    def colored_status(self, obj):
        colors = {
            'pending': '#f39c12',
            'confirmed': '#3498db',
            'preparing': '#e67e22',
            'ready': '#2ecc71',
            'delivered': '#1abc9c',
            'completed': '#27ae60',
            'cancelled': '#e74c3c',
        }
        color = colors.get(obj.status, '#fff')
        return f'<span style="color: {color}; font-weight: bold;">{obj.get_status_display()}</span>'
    colored_status.short_description = 'Holat'
    colored_status.allow_tags = True

    def item_count(self, obj):
        return f"{obj.items.count()} ta"
    item_count.short_description = 'Elementlar'

    def wait_time(self, obj):
        if obj.status in ['pending', 'confirmed', 'preparing']:
            delta = timezone.now() - obj.created_at
            minutes = delta.seconds // 60
            if minutes < 1:
                return f'<span style="color: #2ecc71;">Hozir</span>'
            elif minutes < 15:
                return f'<span style="color: #2ecc71;">{minutes}d</span>'
            elif minutes < 30:
                return f'<span style="color: #f39c12;">{minutes}d</span>'
            else:
                return f'<span style="color: #e74c3c;">{minutes}d</span>'
        return '-'
    wait_time.short_description = 'Kutish'
    wait_time.allow_tags = True

    def wait_time_display(self, obj):
        delta = timezone.now() - obj.created_at
        minutes = delta.seconds // 60
        return f"{minutes} daq"
    wait_time_display.short_description = 'Kutish vaqti'

    def session_duration(self, obj):
        if obj.completed_at:
            delta = obj.completed_at - obj.created_at
            minutes = delta.seconds // 60
            return f"{minutes} daq"
        return "Yakunlanmagan"
    session_duration.short_description = 'Sessiya'

    actions = ['mark_confirmed', 'mark_preparing', 'mark_ready', 'mark_delivered', 'mark_completed', 'mark_paid']

    @admin.action(description='Tasdiqlash')
    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, 'Buyurtmalar tasdiqlandi')

    @admin.action(description="Tayyorlanmoqda")
    def mark_preparing(self, request, queryset):
        queryset.update(status='preparing')
        self.message_user(request, "Tayyorlanmoqda deb belgilandi")

    @admin.action(description='Tayyor')
    def mark_ready(self, request, queryset):
        queryset.update(status='ready')
        self.message_user(request, 'Tayyor deb belgilandi')

    @admin.action(description='Yetkazildi')
    def mark_delivered(self, request, queryset):
        queryset.update(status='delivered')
        self.message_user(request, 'Yetkazildi deb belgilandi')

    @admin.action(description='Yakunlash')
    def mark_completed(self, request, queryset):
        for order in queryset:
            order.complete_order()
        self.message_user(request, 'Buyurtmalar yakunlandi')

    @admin.action(description="To'lov qilindi (simulyatsiya)")
    def mark_paid(self, request, queryset):
        for order in queryset:
            Payment.objects.get_or_create(
                order=order,
                defaults={
                    'amount': order.total_price,
                    'status': 'success',
                    'completed_at': timezone.now(),
                    'method': 'cash'
                }
            )
            order.status = 'delivered'
            order.save()
        self.message_user(request, "To'lovlar muvaffaqiyatli qilindi")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'order', 'quantity', 'servings', 'price_per_serving', 'subtotal')
    list_filter = ('order__status', 'menu_item__category')
    search_fields = ('menu_item__name', 'order__id')

    def order(self, obj):
        return f"#{obj.order.id}"
    order.short_description = 'Buyurtma'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'colored_amount', 'colored_method', 'colored_status', 'transaction_id', 'completed_at')
    list_filter = ('status', 'method', 'created_at')
    search_fields = ('transaction_id', 'order__id')
    readonly_fields = ('transaction_id', 'created_at', 'completed_at')

    def order(self, obj):
        return f"#{obj.order.id}"
    order.short_description = 'Buyurtma'

    def colored_amount(self, obj):
        return f'<span style="color: #00b894; font-weight: bold;">{obj.amount} som</span>'
    colored_amount.short_description = 'Summa'
    colored_amount.allow_tags = True

    def colored_method(self, obj):
        colors = {
            'cash': '#2ecc71',
            'card': '#3498db',
            'click': '#9b59b6',
            'payme': '#e74c3c',
            'uzum': '#f39c12',
        }
        color = colors.get(obj.method, '#fff')
        return f'<span style="color: {color};">{obj.get_method_display()}</span>'
    colored_method.short_description = 'Usul'
    colored_method.allow_tags = True

    def colored_status(self, obj):
        colors = {'pending': '#f39c12', 'success': '#2ecc71', 'failed': '#e74c3c', 'refunded': '#3498db'}
        color = colors.get(obj.status, '#fff')
        return f'<span style="color: {color}; font-weight: bold;">{obj.get_status_display()}</span>'
    colored_status.short_description = 'Holat'
    colored_status.allow_tags = True


@admin.register(WaiterCall)
class WaiterCallAdmin(admin.ModelAdmin):
    list_display = ('colored_table', 'reason_short', 'wait_time', 'colored_answered', 'reply_preview', 'created_at')
    list_filter = ('is_answered', 'created_at', 'table')
    search_fields = ('table__number', 'reason', 'reply_message')
    readonly_fields = ('created_at', 'answered_at', 'reply_message', 'staff_phone')
    list_per_page = 20

    def colored_table(self, obj):
        return f'<span style="color: #00b894; font-weight: bold;">Stol {obj.table.number}</span>'
    colored_table.short_description = 'Stol'
    colored_table.allow_tags = True

    def reason_short(self, obj):
        return obj.reason[:30] + '...' if len(obj.reason) > 30 else obj.reason
    reason_short.short_description = 'Sabab'

    def wait_time(self, obj):
        delta = timezone.now() - obj.created_at
        minutes = delta.seconds // 60
        if minutes < 5:
            return f'<span style="color: #2ecc71;">{minutes}d</span>'
        elif minutes < 15:
            return f'<span style="color: #f39c12;">{minutes}d</span>'
        else:
            return f'<span style="color: #e74c3c;">{minutes}d</span>'
    wait_time.short_description = 'Kutish'
    wait_time.allow_tags = True

    def colored_answered(self, obj):
        if obj.is_answered:
            return format_html('<span style="color: #2ecc71;"><i>Ha</i></span>')
        return format_html('<span style="color: #e74c3c;"><i>Yo\'q</i></span>')
    colored_answered.short_description = 'Javob'

    def reply_preview(self, obj):
        if obj.reply_message:
            return obj.reply_message[:20] + '...' if len(obj.reply_message) > 20 else obj.reply_message
        return '-'
    reply_preview.short_description = 'Javob'

    actions = ['mark_answered', 'reply_to_selected']

    @admin.action(description="Javob berildi")
    def mark_answered(self, request, queryset):
        queryset.update(is_answered=True, answered_at=timezone.now())
        self.message_user(request, 'Javob berildi deb belgilandi')

    @admin.action(description="Tanlanganlarga javob yuborish")
    def reply_to_selected(self, request, queryset):
        for call in queryset.filter(is_answered=False):
            call.reply_with_message("Tez orada xizmatni ko'rsatamiz!")
        self.message_user(request, 'Javoblar yuborildi')
