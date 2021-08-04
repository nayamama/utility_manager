from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Receipt, Store, Images
from .forms import ReceiptForm, ImagesFormSet, UpdateImagesFormSet, ImageForm
from util_calculator.views import AjaxableResponseMixin
from accounts_admin.utils import ManagerUserMixin


class ReceiptListView(LoginRequiredMixin, ListView):
    model = Receipt
    paginate_by = 5
    ordering = ['-date']


class StoreCreateView(ManagerUserMixin, AjaxableResponseMixin, SuccessMessageMixin, CreateView):
    model = Store
    fields = ['name']
    template_name = "receipts/create_store.html"
    success_url = reverse_lazy('receipts:receipts-list')

    def get_success_message(self, cleaned_data):
        return '{} was created successfully!'.format(self.object.name)


class ReceiptCreateView(ManagerUserMixin, CreateView):
    model = Receipt
    form_class = ReceiptForm
    success_url = reverse_lazy('receipts:receipts-list')
    template_name = 'receipts/create_receipt.html'

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateView, self).get_context_data(**kwargs)
        formset = ImagesFormSet(queryset=Images.objects.none())
        context['formset'] = formset
        context['form'] = ReceiptForm()
        return context

    def post(self, request, *args, **kwargs):
        formset = ImagesFormSet(request.POST, request.FILES)
        form = ReceiptForm(request.POST)
        if formset.is_valid() and form.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        receipt = form.save()
        formset.instance = receipt
        print(formset)
        formset.save()
        messages.success(self.request, "Yeeew, you upload a new receipt successfully!")

        if self.request.is_ajax():
            data = {
                'form': form,
                'formset': formset
            }
            return JsonResponse(data)
        else:
            return HttpResponseRedirect(reverse('receipts:receipts-list'))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ReceiptUpdateView(ManagerUserMixin, UpdateView):
    template_name = 'receipts/update_receipt.html'
    model = Receipt
    form_class = ReceiptForm
    success_url = reverse_lazy('receipts:receipts-list')

    def get_object(self, queryset=None):
        try:
            obj = super(ReceiptUpdateView, self).get_object()
        except Receipt.DoesNotExist:
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        context = super(ReceiptUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = ReceiptForm(self.request.POST, instance=self.object)
            context['formset'] = UpdateImagesFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['form'] = ReceiptForm(instance=self.object)
            context['formset'] = UpdateImagesFormSet(instance=self.object)
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = UpdateImagesFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if formset.is_valid() and form.is_valid():
            return self.form_valid(form, formset)
        else:
            print(formset.errors)
            print(formset.non_form_errors)
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        self.object.save()
        messages.success(self.request, "Yeeew, you update a new receipt successfully!")

        if self.request.is_ajax():
            data = {
                'form': form,
                'formset': formset
            }
            return JsonResponse(data)
        else:
            return HttpResponseRedirect(reverse('receipts:receipts-list'))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ReceiptDeleteView(ManagerUserMixin, AjaxableResponseMixin, DeleteView):
    model = Receipt
    success_url = reverse_lazy('receipts:receipts-list')
    template_name = 'receipts/receipt_confirm_delete.html'

    def get_object(self, queryset=None):
        try:
            obj = super(ReceiptDeleteView, self).get_object()
        except Receipt.DoesNotExist:
            raise Http404()
        return obj

    def get_success_message(self, cleaned_data):
        return 'Receipt #{} was deleted successfully!'.format(self.object.pk)


class ImageView(LoginRequiredMixin, DetailView):
    model = Images

    def get_object(self, queryset=None):
        try:
            obj = super(ImageView, self).get_object()
        except Images.DoesNotExist:
            raise Http404()
        return obj

    def dispatch(self, request, *args, **kwargs):
        picture = get_object_or_404(Images, pk=self.kwargs['pk'])
        pic_url = picture.image.url
        self.pic_name = pic_url[22:]
        return super(ImageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data(**kwargs)
        context['title'] = self.pic_name
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.request.is_ajax():
            data = render_to_string(
                'receipts/image.html',
                context,
                request=self.request,
            )
            return JsonResponse(data, status=200, safe=False)
        else:
            return self.render_to_response(context)
