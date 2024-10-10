import redis
from decimal import Decimal
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.core.paginator import Paginator, \
    PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import NftProduct, Category
from .utils import set_views_for_products
from .forms import NftProductSellForm, \
    UpdatePriceWithPercentsForm
from account.models import Profile


r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)
User = get_user_model()


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

        context["similar_nfts"] = NftProduct.sold_objects \
                                       .filter(Q(owner=self.object.owner)
                                               | Q(category=self.object.category)) \
                                       .exclude(id=self.object.id)[:6]

        profile_id = self.request.user.profile.id
        profile = Profile.objects.get(id=profile_id)
        context["favorites"] = profile.favorites.all()
        context["section"] = "shop"
        return context


def put_nft_on_sale(request: HttpRequest, nft_id: int) -> HttpResponse:
    nft = NftProduct.objects.get(id=nft_id)
    if request.method == "POST":
        form = NftProductSellForm(data=request.POST, instance=nft)
        nft_on_sale = form.save(commit=False)
        nft_on_sale.is_sale = True
        nft_on_sale.save()

        return redirect("shop:nft_list")
    else:
        form = NftProductSellForm(instance=nft)
        percent_form = UpdatePriceWithPercentsForm()

    return render(request, "shop/nft/put_nft_on_sale.html",
                  context={"section": "shop",
                           "form": form,
                           "percent_form": percent_form,
                           "nft": nft})


@require_POST
def nft_price_update(request, nft_id: int) -> HttpResponse:
    nft = NftProduct.objects.get(id=nft_id)
    percent_form = UpdatePriceWithPercentsForm(data=request.POST)

    if percent_form.is_valid():
        nft.price += (nft.price
                      * Decimal(percent_form.cleaned_data["price_increase"])
                      / Decimal(100))
        nft.save()

    return redirect("shop:put_nft_on_sale", nft_id=nft_id)
