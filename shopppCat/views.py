import logging
from timeit import default_timer

from django.contrib.syndication.views import Feed
from rest_framework.decorators import action
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views import View
from django.contrib.auth.models import Group, User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.cache import cache
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import ProductSerializer, OrderSerializer
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from drf_spectacular.utils import extend_schema

from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order

log = logging.getLogger(__name__)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    fiterset_fields = [
        'name', 'discription', 'price', 'discount'
    ]
    search_fields = [
        'name', 'discription'
    ]
    ordering = 'pk','name'


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    fiterset_fields = [
        'createt_at, '
        'user',
    ]
    search_fields = [
        'createt_at, '
        'user',
    ]
    ordering = 'pk','createt_at'

class ShopIndexView(View):
    def get(self, request:HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 199),
            ('Smatphone', 500),
            ('Desktop', 350),
        ]
        context = {
            'time_run': default_timer(),
            'products': products
        }
        return render(request, 'shopppCat/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.all(),
        }
        return render(request, 'shopppCat/group-list.html', context=context)

    def post(self, request:HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = "shopppCat/product-details.html"
    model = Product
    context_object_name = "products"


class ProductListView(ListView):
    template_name = 'shopppCat/products_list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.all


class ProductCreateView(PermissionRequiredMixin,CreateView):
    permission_required = 'shopppCat.add_product'
    model = Product
    fields = 'name', 'price', 'discount', 'discription'
    success_url = reverse_lazy('shopppCat:product_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        return super().form_valid(form)

class ProductUdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.reqest.user
        return self.request.user.is_superoser or user.has_perm('shopppCat.add_product') or Product.created_by == user

    model = Product
    fields = 'name', 'price', 'discount', 'discription'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopppCat:product_det',
            kwargs={'pk': self.object.pk}
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopppCat:product_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.arhivate = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class LatestProductsFeed(Feed):
    title = 'Latest Products'
    description = 'Latest Products'
    link = reverse_lazy('shopppCat:product_list')

    def items(self):
        return Product.objects.all()[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.discription

    def item_link(self, item):
        return reverse('shopppCat:product_det', kwargs={'pk': item.pk})

class OrderListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related('products')
    )


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopppCat.view_order'
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related('products')
    )


class OrderCreateView(CreateView):
    model = Order
    fields = 'delivery_address', 'promo_code', 'user', 'products'
    success_url = reverse_lazy('shopppCat:order')


class OrderUdateView(UpdateView):
    model = Order
    fields = 'delivery_address', 'promo_code', 'user', 'products'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopppCat:order-detail',
            kwargs={'pk': self.object.pk}
        )

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopppCat:order')


def index_upload (request:HttpRequest)->HttpResponse:
    if request.method =='POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        file_size = fs.size(myfile)
        if file_size >= 1048576:
            return render(request, 'shopppCat/error.html')
        else:
            filename = fs.save(myfile.name, myfile)
            print('save!', filename)
    return render(request, 'shopppCat/upload.html')


class OrderExportView(View):
    def get(self, request:HttpRequest) -> JsonResponse:
        order = Order.objects.order_by("pk").all()
        order_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promo_code': order.promo_code,
                'user': order.user,
                'products': order.products
            }
            for order in order
        ]
        return JsonResponse({'order': order_data})


# Классы для Практической работы 19.6
class UserOrdersListView(ListView):
    template_name = 'shopppCat/user_orders.html'
    context_object_ = 'user_orders'

    def get_queryset(self, **kwargs):
        ower = get_object_or_404(User, pk=self.kwargs['user_id'])
        orders = Order.objects.filter(user=ower).all()
        context = {
            'USER': ower,
            'orders': orders,
        }
        return context

    def get_context_data(self, **kwargs):
        context = super(UserOrdersListView, self).get_context_data(**kwargs)
        return context
class User_OrderExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        order_data = cache.get(
            f'order_{self.kwargs["user_id"]}'
        )
        if order_data is None:
            ower = get_object_or_404(User, pk=self.kwargs['user_id'])
            order = Order.objects.filter(user=ower).all()
            order_data = [
                {
                    'pk': order.pk,
                    'delivery_address': order.delivery_address,
                    'promo_code': order.promo_code,
                    'user': order.user,
                    'products': order.products
                }
                for order in order
            ]
            cache.set(
                f'order_{ower.pk}',
                order_data,
                timeout=60
            )
        return JsonResponse({'order': order_data})