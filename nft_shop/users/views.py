from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from account.models import Profile


User = get_user_model()


@method_decorator(login_required, name="dispatch")
class UserListView(ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"
    paginate_by = 12

    def get_queryset(self) -> QuerySet:
        return User.objects.filter(is_active=True) \
                           .exclude(id=self.request.user.id) \
                           .select_related("profile") \
                           .order_by("-id") \


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "users"
        return context


@method_decorator(login_required, name="dispatch")
class UserProfileDetail(DetailView):
    model = Profile
    context_object_name = "profile"
    template_name = "users/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "users"
        return context
