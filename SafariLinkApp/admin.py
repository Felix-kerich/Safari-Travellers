from django.contrib import admin

from SafariLinkApp.models import Member, BusesAvailable, Notifications

admin.site.register(Member)
admin.site.register(BusesAvailable)
admin.site.register(Notifications)