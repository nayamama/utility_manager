from django.urls import path

from . import views

# add namespaces to the URLconf
app_name = 'util_calculator'

urlpatterns = [
    path('', views.BillListView.as_view(), name='bill-list'),
    path('bills/<int:pk>/', views.BillDetailView.as_view(), name="bill-detail"),
    path('fill/', views.BillFormView.as_view(), name='bill-creation'),
    path('payment-creation/', views.PaymentFormView.as_view(), name='payment-creation'),
    path('utility-creation/', views.UtilityCreateView.as_view(), name='utility-creation'),
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('mama-calculator/', views.calculate_average_utility_cost, name='ma-utility-result'),
    path('date-calculator/', views.calculate_payment_dates, name='payment-date'),
    path('generic-calculator/', views.generic_cost_calculator, name='generic-calculator'),
    path('js-calculator/', views.js_cost_calculator, name='js-calculator'),
    path('pure-js-calculator/', views.pure_js_calculator, name='pure-js'),
    path('calculator/', views.CalculatorFormView.as_view(), name='calculate'),
    path('get-data/', views.DatesView.as_view(), name='get-dates'),

]