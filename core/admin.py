import base64
import io
import qrcode

from django.contrib import admin
from django.utils.html import format_html

from .models import Provider, Customer, FikaID, Transaction


class FikaIDAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'count', 'show_limit', 'show_qr')
    readonly_fields = ['fika_code', 'qr_string']

    def show_limit(self, obj):
        if obj.customer:
            return obj.customer.limit

    def show_qr(self, obj):
        b64_string = ''
        with io.BytesIO() as out:
            qrcode.make(obj.qr_string).save(out, format='png')
            b64_string = base64.b64encode(out.getvalue()).decode()
        return format_html(f'<img src="data:image/png;base64,{b64_string}" width="100" height="100">')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'fika_id', 'customer', 'provider', 'created')
    readonly_fields = ['created']


admin.site.register(Provider)
admin.site.register(Customer)
admin.site.register(FikaID, FikaIDAdmin)
admin.site.register(Transaction, TransactionAdmin)
