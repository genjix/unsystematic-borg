from django.contrib import admin
from unsystem.models import UserProfile, Talk, Ticket

class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ("user",)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Talk)
admin.site.register(Ticket)

