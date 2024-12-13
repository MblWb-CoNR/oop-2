from django.contrib import admin
from .models import AdvUser
from .models import Categories
from .models import Application


admin.site.register(AdvUser)
admin.site.register(Categories)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    model = Application
    list_display = ('date', 'name', 'description', 'photo', 'price')

