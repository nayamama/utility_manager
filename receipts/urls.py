from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'receipts'

urlpatterns = [
    path('', views.ReceiptListView.as_view(), name='receipts-list'),
    path('store-creation/', views.StoreCreateView.as_view(), name='store-creation'),
    path('receipt-creation/', views.ReceiptCreateView.as_view(), name="receipt-creation"),
    path('update/<int:pk>/', views.ReceiptUpdateView.as_view(), name='receipt-update'),
    path('delete/<int:pk>/', views.ReceiptDeleteView.as_view(), name='receipt-delete'),
    path('images/<int:pk>/', views.ImageView.as_view(), name='image'),
]