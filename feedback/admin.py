from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('star_rating', 'colored_table', 'menu_item_display', 'comment_preview', 'colored_anonymous', 'created_at')
    list_filter = ('rating', 'is_anonymous', 'created_at')
    search_fields = ('comment', 'menu_item_name', 'table__number')
    list_per_page = 20
    date_hierarchy = 'created_at'

    def star_rating(self, obj):
        return '*' * obj.rating + '.' * (5 - obj.rating)
    star_rating.short_description = 'Baho'

    def colored_table(self, obj):
        if obj.table:
            return f'Stol {obj.table.number}'
        return '-'
    colored_table.short_description = 'Stol'

    def menu_item_display(self, obj):
        if obj.menu_item_name:
            return obj.menu_item_name[:20] + '...' if len(obj.menu_item_name) > 20 else obj.menu_item_name
        return '-'
    menu_item_display.short_description = 'Taom'

    def comment_preview(self, obj):
        if obj.comment:
            return obj.comment[:30] + '...' if len(obj.comment) > 30 else obj.comment
        return '-'
    comment_preview.short_description = 'Fikr'

    def colored_anonymous(self, obj):
        return 'Ha' if obj.is_anonymous else "Yo'q"
    colored_anonymous.short_description = 'Anonim'
    colored_anonymous.boolean = True

    actions = ['mark_anonymous']

    @admin.action(description="Anonim qilish")
    def mark_anonymous(self, request, queryset):
        queryset.update(is_anonymous=True)
        self.message_user(request, 'Tanlanganlar anonim qilindi')
