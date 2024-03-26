from django.contrib import admin
from io import TextIOWrapper
from csv import DictReader
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .admin_export import ExportAsCSW
from .models import Product,Order
from django.utils.translation import gettext as _
from .forms import CSVImportForm
# Register your models here.

class OrderInLine(admin.TabularInline):
    model = Product.orders.through

@admin.action(description = 'Archive prod')
def mark_archived(modeladmin:admin.ModelAdmin,request:HttpRequest,queryset:QuerySet):
    queryset.update(arhivate=True)


@admin.action(description='Unarchive prod')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(arhivate=False)

class ProductAdmin(admin.ModelAdmin,ExportAsCSW):
    change_list_template = 'shopppCat/product_changelist.html'
    actions = [
        mark_archived,
        'export_csv',
        mark_unarchived,
    ]
    list_display = "pk","name","discription","price", "discount",'arhivate'
    inlines = [
        OrderInLine
    ]
    list_display_links = 'pk', 'name'
    ordering = 'pk','name'
    search_fields = 'name', 'discription'
    fieldsets = [
        (None, {
            'fields': ('name', 'discription')
        }),
        (_('Price options'), {
            'fields': ('price', 'discount'),
            'classes': ('collapse', 'wide'),
        }),
        (_('Extra options'), {
            'fields': ('arhivate',),
            'classes': ('collapse', 'wide'),
        }),
    ]

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        form = CSVImportForm()
        context = {
            'form': form,
        }
        return render(request, 'admin/csv_form.html', context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import_product_csv/',
                self.import_csv,
                name='import_product_csv',
            ),
        ]
        return custom_urls + urls

admin.site.register(Product, ProductAdmin)

class ProductInline(admin.TabularInline):
    model = Order.products.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = 'shopppCat/order_changelist.html'
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_address", "promo_code", "createt_at", 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related("user")

    def user_verbose(self,obj:Order)->str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)

        csv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding=request.encoding
        )
        reader = DictReader(csv_file)

        product = [
            Product(**row)
            for row in reader
        ]
        Product.objects.bulk_create(product)
        self.message_user(request, 'Data was import')
        return redirect('..')
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import_order_csv/',
                self.import_csv,
                name='import_order_csv',
            ),
        ]
        return custom_urls + urls