from django.urls import path
from .views import ProductListView, OrderListView

app_name = 'shopppCat'

urlpatterns = [
    path('prod/', ProductListView.as_view(), name='api_test_prod'),
    path('order/', OrderListView.as_view(), name='api_test_order'),
]