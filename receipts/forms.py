from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.widgets import SelectDateWidget

from .models import Receipt, Images, Store


class ReceiptForm(forms.ModelForm):
    #store = forms.ModelChoiceField(queryset=Store.objects.none())

    class Meta:
        model = Receipt
        fields = ['date', 'amount', 'store']

        widgets = {
            'date': SelectDateWidget(years=range(2020, 2040))
        }
        labels = {
            'date': 'Date',
            'amount': "Amount",
            'store': 'Store'
        }

    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)
        self.fields['store'].queryset = Store.objects.all()


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ['image']


ImagesFormSet = inlineformset_factory(
    parent_model=Receipt,
    model=Images,
    form=ImageForm,
    can_delete=False,
    extra=1)

UpdateImagesFormSet = inlineformset_factory(
    parent_model=Receipt,
    model=Images,
    form=ImageForm,
    extra=1)



