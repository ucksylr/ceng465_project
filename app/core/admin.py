from django.contrib import admin

from core.models import Event, User

admin.site.register(User)
admin.site.register(Event)
