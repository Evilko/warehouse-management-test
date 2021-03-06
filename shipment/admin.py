import qrcode
import io
import uuid
import os
import requests

from django.urls import reverse
from django.contrib import admin, messages
from django.core.mail import EmailMessage
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from django.utils.translation import gettext as _

from .forms import ShipmentForm


from common.models import ShipmentStock
from warehouse.forms import StockFormM2M

from .models import get_shipment_total
from .models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    """
    Отображение списка и формы заказов
    """
    class StockInline(admin.StackedInline):
        model = ShipmentStock
        form = StockFormM2M
        max_num = 0
        min_num = 0
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')
        can_delete = False

    form = ShipmentForm
    # поля для отображения в списке погрузок
    shipment_total = get_shipment_total
    shipment_total.short_description = _('Сумма покупки')
    list_display = ('customer', 'date', 'status', shipment_total, 'qr', )
    # поля для фильтрации
    list_filter = ('date', 'customer', 'status', )
    # поля для текстового поиска
    search_fields = ('status', 'customer__full_name', )
    fieldsets = ((_('ИНФОРМАЦИЯ О ПОКУПКЕ'),
                  {'fields': ('shipment_id', 'customer_name',
                              'number_of_items', 'total',
                              'shipment_status', 'shipment_date',
                              'shipment_qr', )}), )
    inlines = (StockInline, )

    def is_shipment_available(self, obj):
        return all(s.stock.number > s.number
                   for s in ShipmentStock.objects.filter(shipment=obj))

    # убираем кнопку "Добавить погрузку" при отображении списка погрузок
    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        shipment_available = self.is_shipment_available(obj)
        # нажата кнопка Cancel
        if '_cancel' in request.POST:
            if obj.status == Shipment.SENT:
                # обновляем при отмене заказа,
                # если товары были зарезервированы
                for shipment_stock in obj.shipmentstock_set.all():
                    shipment_stock.stock.number += shipment_stock.number
                    shipment_stock.stock.save()
            obj.status = Shipment.CANCELLED
        elif obj.status == Shipment.CREATED:
            # проверка данных клиента на сервере
            if shipment_available:
                obj.status = Shipment.SENT
                # обновляем склад
                for shipment_stock in obj.shipmentstock_set.all():
                    shipment_stock.stock.number -= shipment_stock.number
                    shipment_stock.stock.save()
                obj.qr = str(obj.id) + str(uuid.uuid4())
                email = obj.customer.email
                link = self.get_confirmation_link(request.get_host(), obj.qr)
                body = _('Здравствуйте, подтвердите '
                         + 'получение покупки: перейдите по ссылке ')
                body += _('из QR-кода во вложении (') + link + ').'
                self.send_email_to_customer(email, body, obj, link)
        elif obj.status == Shipment.SENT:
            obj.status = Shipment.DONE
        super().save_model(request, obj, form, change)
        # печатаем сообщение об ошибке
        if not shipment_available:
            messages.set_level(request, messages.ERROR)
            messages.error(request, _('На складе недостаточно '
                                      + 'товара для данной покупки'))

    # добавляем значения в extra_context для дальнейшего использования
    # на странице формы информации о погрузке
    def change_view(self, request, object_id,
                    form_url='', extra_context=None):
        extra = extra_context or {}
        obj = Shipment.objects.get(pk=object_id)
        extra['STATUS_VALUE'] = Shipment.objects.get(pk=object_id).status
        extra['STATUS_DONE'] = Shipment.DONE
        extra['STATUS_CANCELLED'] = Shipment.CANCELLED
        extra['STATUS_CREATED'] = Shipment.CREATED
        extra['STATUS_SENT'] = Shipment.SENT
        extra['SHIPMENT_AVAILABLE'] = self.is_shipment_available(obj)
        return super().change_view(request, object_id,
                                   form_url, extra_context=extra)

    def get_qr(self, link):
        qr = qrcode.make(link)
        img = qr.get_image()
        byte_stream = io.BytesIO()
        img.save(byte_stream, 'PNG')
        return byte_stream.getvalue()

    def get_confirmation_link(self, host, qr):
        return str(host) + reverse('shipment:shipment_confirmation',
                                   args=(qr, ))

    def send_email_to_customer(self, receiver, body, customer, link):
        qr = self.get_qr(link)
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(qr)
        encode_base64(attachment)
        attachment.add_header('Content-Disposition',
                              'attachment; filename=qr.png')
        message = EmailMessage(subject=_('Подтверждение получения товара'),
                               body=body, to=[receiver, ],
                               attachments=[attachment, ])
        message.send()
