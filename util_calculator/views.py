import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import View
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from accounts_admin.utils import ManagerUserMixin
from .models import Bill, Payment, Utility
from .forms import BillForm, CalculateCostForm, GenericCostCalculatorForm, JSCostCalculatorForm, PaymentForm, \
    CalculatePaymentDaysForm


class AjaxableResponseMixin:
    def form_invalid(self, form):
        response = super.form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'form': form,
            }
            return JsonResponse(data)
        else:
            return response


class UtilityCreateView(ManagerUserMixin, AjaxableResponseMixin, SuccessMessageMixin, CreateView):
    model = Utility
    fields = ['name']
    template_name = "util_calculator/create_utility.html"
    success_url = reverse_lazy('util_calculator:bill-list')

    def get_success_message(self, cleaned_data):
        return '{} was created successfully!'.format(self.object.name)


class BillListView(LoginRequiredMixin, ListView):
    model = Bill
    paginate_by = 8
    ordering = ['-bill_date']


class BillFormView(ManagerUserMixin, AjaxableResponseMixin, CreateView):
    template_name = 'util_calculator/create_bill.html'
    form_class = BillForm
    success_url = reverse_lazy('util_calculator:bill-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.pub_date = timezone.now()
        if self.request.is_ajax():
            data = {
                'form': form,
            }
            return JsonResponse(data)
        else:
            return response


class BillDetailView(LoginRequiredMixin, AjaxableResponseMixin, DetailView):
    model = Bill
    template_name = "util_calculator/bill_detail.html"

    def get_object(self, queryset=None):
        try:
            obj = super(BillDetailView, self).get_object()
        except Bill.DoesNotExist:
            raise Http404()
        return obj


class PaymentFormView(ManagerUserMixin, AjaxableResponseMixin, CreateView):
    template_name = 'util_calculator/create_payment.html'
    form_class = PaymentForm
    success_url = reverse_lazy('util_calculator:payment-list')


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    paginate_by = 10
    ordering = ['-payment_date']


def payments_calculation(start, end):
    pays = Payment.objects.filter(payment_date__range=[start, end])
    result = sum([p.amount for p in pays])
    return result


class CalculatorFormView(LoginRequiredMixin, FormView):
    form_class = CalculateCostForm
    template_name = 'util_calculator/new_calculator.html'


def date_converter(tag):
    raw_data = sorted(list(Bill.objects.filter(utility__name=tag).values_list('bill_date', flat=True)))
    strf_data = [d.strftime('%Y-%m-%d') for d in raw_data]
    return strf_data


class DatesView(LoginRequiredMixin, View):
    def get(self, request):
        data = dict()
        data['hydro_dates'] = date_converter('Hydro')
        data['water_dates'] = date_converter('Water')
        json_data = json.dumps(data)
        return JsonResponse(json_data, safe=False)


@login_required()
def calculate_average_utility_cost(request):
    data = dict()
    if request.method == 'POST':
        form = CalculateCostForm(request.POST)
        if form.is_valid():
            utility = form.cleaned_data['utility']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            start_bill = get_object_or_404(Bill, bill_date=start_date)
            end_bill = get_object_or_404(Bill, bill_date=end_date)
            # get the payments between start and end
            pays = payments_calculation(start_date, end_date)
            average_cost = round(
                (start_bill.amount + pays - end_bill.amount) / (end_bill.bill_date - start_bill.bill_date).days, 2)

            msg = 'The average {} cost between {} and {} is {}.'.format(utility, start_date, end_date, average_cost)
            data = {
                'msg': msg
            }
        else:
            print(form.errors.as_data())
            return JsonResponse(form.errors.as_json(), safe=False)
    return JsonResponse(data)


def get_average_cost(form):
    average_cost = None
    start_date = form.cleaned_data['start_date']
    end_date = form.cleaned_data['end_date']
    amount = form.cleaned_data['amount']
    tdelta = (end_date - start_date).days
    frequency = form.cleaned_data['frequency']
    if frequency == "day":
        average_cost = amount / tdelta
    elif frequency == "week":
        average_cost = amount / tdelta * 7
    else:
        average_cost = amount / tdelta * 30

    return start_date, end_date, frequency, average_cost


def generic_cost_calculator(request):
    average_cost = None
    start_date = None
    end_date = None
    frequency = None
    if request.method == 'POST':
        form = GenericCostCalculatorForm(request.POST)
        if form.is_valid():
            start_date, end_date, frequency, average_cost = get_average_cost(form)

        return render(
            request,
            'util_calculator/general_cost_calculator.html',
            {
                 'form': GenericCostCalculatorForm(),
                 'average_cost': round(average_cost, 3),
                 'start_date': start_date,
                 'end_date': end_date,
                 'frequency': frequency
            }
        )
    else:
        form = GenericCostCalculatorForm()
    return render(request, 'util_calculator/general_cost_calculator.html', {'form': form})


def pure_js_calculator(request):
    form = JSCostCalculatorForm()
    return render(request, 'util_calculator/pure_js_calculator.html', {'form': form})


def js_cost_calculator(request):
    data = dict()
    if request.method == 'POST':
        form = JSCostCalculatorForm(request.POST)
        if form.is_valid():
            start_date, end_date, frequency, average_cost = get_average_cost(form)
            msg = 'The average cost between {} and {} is {} per {}.'\
                .format(start_date, end_date, round(average_cost, 2), frequency)
            data['html_form'] = render_to_string(
                'util_calculator/result.html',
                {'msg': msg},
                request=request
            )
        return JsonResponse(data)
    else:
        form = JSCostCalculatorForm()
    return render(request, 'util_calculator/js_general_calculator.html', {'form': form})


def calculate_payment_dates(request):
    from datetime import timedelta
    data = dict()
    if request.method == 'POST':
        print('post')
        form = CalculatePaymentDaysForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            delta = form.cleaned_data['length']
            end_date = date + timedelta(days=delta)
            msg = 'The next payment should be {} {}, {}'.format(end_date.strftime('%B'), end_date.day, end_date.year)
            data['html_form'] = render_to_string(
                'util_calculator/payment_date.html',
                {'msg': msg},
                request=request
            )
        return JsonResponse(data)
    else:
        form = CalculatePaymentDaysForm()
    return render(request, 'util_calculator/days_calculator.html', {'form': form})


