from django.shortcuts import render
from . import models
from django.views.generic import (
    ListView,
    DetailView
)


class ProductDetail(DetailView):
    model = models.Product


class ProductList(ListView):
    model = models.Product
    queryset = models.Product.objects.all()


def test(request):
    return render(request, 'store_app/test.html')
