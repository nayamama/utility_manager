from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render


class ManagerUserMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def handle_no_permission(self):
        context = {'msg': "Only Manager team have access to this function."}
        if self.request.is_ajax():
            return JsonResponse(context, status=403)
        return render(
            self.request,
            'status_page/403.html',
            context
        )


