from django.contrib import admin
from .models import Gldetail, Glpost, Period, Entity, Status

# Register your models here.

class EntityAdmin(admin.ModelAdmin):
    pass
admin.site.register(Entity, EntityAdmin)

class PeriodAdmin(admin.ModelAdmin):
    pass
admin.site.register(Period, PeriodAdmin)

class GldetailAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        obj.username = request.user
        obj.save()
        
admin.site.register(Gldetail, GldetailAdmin)

class GlpostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Glpost, GlpostAdmin)

class StatusAdmin(admin.ModelAdmin):
    pass
admin.site.register(Status, StatusAdmin)