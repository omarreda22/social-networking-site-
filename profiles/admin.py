from django.contrib import admin

from .models import Profile, Relationship


admin.site.register(Profile)



class RelationshipAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status']
    list_editable = ['status']

admin.site.register(Relationship, RelationshipAdmin)
