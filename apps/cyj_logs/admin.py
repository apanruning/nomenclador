from models import SearchLog
from django.contrib import admin

class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('type_search','tuvo_exito','level','url','message','created',)
    list_filter = ('type_search','tuvo_exito','created',)
    ordering = ('created',)
    search_fields = ('type_search','tuvo_exito','created','message',)
    
admin.site.register(SearchLog, SearchLogAdmin)


