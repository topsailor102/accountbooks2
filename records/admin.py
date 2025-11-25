from django.contrib import admin

from records.models import Expense, Sector, Way

# Register your models here.

admin.site.register(Way)
admin.site.register(Sector)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("dateinfo", "sector", "place", "cost", "way", "summary")
    list_filter = ("sector", "way")


