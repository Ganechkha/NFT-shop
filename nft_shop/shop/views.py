import redis
from django.db.models import F, Value
from django.conf import settings
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.views.generic import DetailView
from django.core.paginator import Paginator, \
    PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import NftProduct, Category
from . utils import set_views_for_products


r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def nft_list(request: HttpRequest, category_slug: str = None):
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        nfts = NftProduct.sold_objects.filter(category=category)
        nfts = set_views_for_products(nfts)
    else:
        category = None
        nfts = NftProduct.sold_objects.all()
        nfts = set_views_for_products(nfts)

    categories = Category.objects.all()
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

    template_name = "shop/nft/list_part.html" if ajax_nfts else "shop/nft/list.html"
    return render(request,
                  template_name,
                  {"section": "shop",
                   "categories": categories,
                   "category": category,
                   "nfts": nfts})


@method_decorator(login_required, name="get")
class NftDetail(DetailView):
    model = NftProduct
    template_name = "shop/nft/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_views = r.incr(f"nft:{self.object.id}:views")
        context["views"] = total_views
        context["section"] = "shop"
        return context
