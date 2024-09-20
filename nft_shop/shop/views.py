from django.shortcuts import render
from django.views.generic import DetailView
from django.core.paginator import Paginator, \
    PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import NftProduct


def nft_list(request: HttpRequest):
    nfts = NftProduct.sold_objects.all()
    paginator = Paginator(nfts, 12)
    page = request.GET.get("page")
    ajax_nfts = request.GET.get("ajax_nfts")

    try:
        paginator.page(page)
    except PageNotAnInteger:
        nfts = paginator.page(1)
    except EmptyPage:
        if ajax_nfts:
            return HttpResponse("")

        nfts = paginator.page(paginator.num_pages)

    if ajax_nfts:
        return render(request,
                      "shop/nft/list_part.html",
                      {"section": "shop",
                       "nfts": nfts})
    return render(request,
                  "shop/nft/list.html",
                  {"section": "shop",
                   "nfts": nfts})


@method_decorator(login_required, name="get")
class NftDetail(DetailView):
    model = NftProduct
    template_name = "shop/nft/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "shop"
        return context
