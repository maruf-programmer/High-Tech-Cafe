from django.db import models
from core.models import Table


class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1 - Juda yomon'),
        (2, '2 - Yomon'),
        (3, "3 - O'rtacha"),
        (4, '4 - Yaxshi'),
        (5, "5 - A'lo"),
    ]

    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, related_name='feedbacks', verbose_name='Stol')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Baho')
    comment = models.TextField(blank=True, verbose_name='Fikr')
    menu_item_name = models.CharField(max_length=200, blank=True, verbose_name='Taom nomi')
    is_anonymous = models.BooleanField(default=False, verbose_name='Anonim')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')

    class Meta:
        verbose_name = 'Fikr'
        verbose_name_plural = 'Fikrlar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{'Anonim' if self.is_anonymous else 'Foydalanuvchi'} - {self.rating} yulduz"
