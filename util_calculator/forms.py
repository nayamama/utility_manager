from django import forms
from django.forms.widgets import SelectDateWidget
from django.utils.translation import gettext_lazy as _

from .models import Bill, Payment, Utility
from bootstrap_datepicker_plus import DatePickerInput


FREQUENCY = [
    ('day', 'Day'),
    ('week', 'Week'),
    ('month', 'Month')
]


class BillForm(forms.ModelForm):
    utility = forms.ModelChoiceField(queryset=Utility.objects.all())

    class Meta:
        model = Bill
        fields = ['bill_date', 'amount', 'utility']
        widgets = {
            'bill_date': SelectDateWidget(years=range(2020, 2040))
        }
        labels = {
            'bill_date': _('Bill Date'),
            'amount': _('Amount'),
            'utility': _('Utility')
        }


class PaymentForm(forms.ModelForm):
    utility = forms.ModelChoiceField(queryset=Utility.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'payment_date': SelectDateWidget(years=range(2021, 2040))
        }
        labels = {
            'payment_date': _('Bill Date'),
            'amount': _('Amount'),
            'utility': _('Utility')
        }


class CleanMixin(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end:
            if end <= start:
                self.add_error('end_date', 'End date should not occur before start date.')
        return cleaned_data


class CalculateCostForm(CleanMixin, forms.Form):
    utility = forms.ModelChoiceField(queryset=Utility.objects.all())
    all_dates = sorted(list(Bill.objects.values_list('bill_date', flat=True)))
    start_date = forms.ChoiceField(choices=[(x, x.strftime('%Y-%m-%d')) for x in all_dates])
    #utility1 = forms.ModelChoiceField(queryset=Utility.objects.all())
    end_date = forms.ChoiceField(choices=[(x, x.strftime('%Y-%m-%d')) for x in all_dates])


class GenericCostCalculatorForm(CleanMixin, forms.Form):
    start_date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y')
    )
    end_date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y')
    )
    amount = forms.DecimalField(decimal_places=2)
    frequency = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=FREQUENCY
    )


class JSCostCalculatorForm(CleanMixin, forms.Form):
    start_date = forms.DateField(
        required=True,
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    end_date = forms.DateField(
        required=True,
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
        })
    )
    amount = forms.DecimalField(decimal_places=2, required=True)
    frequency = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=FREQUENCY
    )


class CalculatePaymentDaysForm(forms.Form):
    date = forms.DateField(widget=SelectDateWidget(years=range(2021, 2040)))
    length = forms.IntegerField(min_value=1)
