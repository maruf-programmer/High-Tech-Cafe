from django.contrib import admin
from django.utils import timezone
from .models import Table, Category, MenuItem, Advertisement, Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'phone', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('name', 'phone')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'colored_status', 'is_active', 'session_time')
    list_filter = ('status', 'is_active')
    search_fields = ('number',)
    readonly_fields = ('session_time', 'current_session_start')

    def colored_status(self, obj):
        status_colors = {
            'free': '#00b894',
            'occupied': '#e74c3c',
            'reserved': '#3498db',
            'cleaning': '#f39c12',
        }
        color = status_colors.get(obj.status, '#fff')
        return f'<span style="color: {color}; font-weight: bold;">{obj.get_status_display()}</span>'
    colored_status.short_description = 'Holat'
    colored_status.allow_tags = True

    def session_time(self, obj):
        if obj.current_session_start:
            delta = timezone.now() - obj.current_session_start
            minutes = delta.seconds // 60
            return f"{minutes} daq"
        return '-'
    session_time.short_description = 'Sessiya vaqti'

    actions = ['make_free', 'make_occupied', 'make_cleaning']

    @admin.action(description='Band qilish')
    def make_occupied(self, request, queryset):
        queryset.update(status='occupied', current_session_start=timezone.now())
        self.message_user(request, 'Stollar band qilindi')

    @admin.action(description="Bo'shlash")
    def make_free(self, request, queryset):
        queryset.update(status='free', current_session_start=None)
        self.message_user(request, "Stollar bo'shlandi")

    @admin.action(description='Tozalash')
    def make_cleaning(self, request, queryset):
        queryset.update(status='cleaning')
        self.message_user(request, "Stollar tozalanmoqda")


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'prep_time_minutes', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('order', 'is_active')
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'prep_time_minutes', 'is_available', 'is_popular', 'calories')
    list_filter = ('category', 'is_available', 'is_popular')
    search_fields = ('name', 'description', 'ingredients', 'vitamins')
    list_editable = ('is_available',)
    list_per_page = 20


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'display_order', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'display_order')
