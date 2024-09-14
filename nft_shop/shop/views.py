from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

from .models import NftProduct


@method_decorator(login_required, name="dispatch")
class NftListView(ListView):
    model = NftProduct
    template_name = "shop/nft/list.html"
    context_object_name = "nfts"
    queryset = NftProduct.sold_objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "shop"
        return context


@method_decorator(login_required, name="get")
class NftDetail(DetailView):
    model = NftProduct

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "shop"
        return context
