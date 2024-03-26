from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ShopIndexView,
                    GroupsListView,
                    ProductDetailsView,
                    ProductListView,
                    OrderDetailsView,
                    ProductUdateView,
                    ProductCreateView,
                    OrderUdateView,
                    ProductDeleteView,
                    LatestProductsFeed,
                    UserOrdersListView,
                    OrderDeleteView,
                    OrderExportView,
                    OrderListView, index_upload,
                    OrderCreateView, ProductViewSet, OrderViewSet)

app_name = 'shopppCat'

routers = DefaultRouter()
routers.register(r'products', ProductViewSet)
routers.register(r'orders', OrderViewSet)


urlpatterns = [
    path('', ShopIndexView.as_view(), name='index_shop'),
    path('api/', include(routers.urls)),
    path('groups/', GroupsListView.as_view(), name='group-list'),

    # пути для Практической работы 19.6
    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user_order_list'),
    path('users/<int:user_id>/orders/export', UserOrdersListView.as_view(), name='user_order_list'),

    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product-details'),
    path('products/<int:pk>/update', ProductUdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete', ProductDeleteView.as_view(), name='delete'),
    path('products/create', ProductCreateView.as_view(), name='create_prod'),
    path('products/latest/feed',LatestProductsFeed(), name='product-feed'),
    path('orders/', OrderListView.as_view(), name='order'),
    path('orders/export', OrderExportView.as_view(), name='order-export'),
    path('orders/create', OrderCreateView.as_view(), name='create_order'),
    path('orders/<int:pk>/', OrderDetailsView.as_view(), name='order-detail'),
    path('orders/<int:pk>/update', OrderUdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete', OrderDeleteView.as_view(), name='order_delete'),
    path('upload/', index_upload, name='upload'),

]