from django.contrib import admin
from api.models import SalesforceData,EmailTrack,EmailLinkTrack,EventData

admin.site.register(SalesforceData)
admin.site.register(EmailTrack)
admin.site.register(EmailLinkTrack)
admin.site.register(EventData)
# Register your models here.
