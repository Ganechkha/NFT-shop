from django.shortcuts import render
from django.views.generic import ListView


class NftListView(ListView):
    template_name = "shop/nft/list.html"
