from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import (
    RedirectView
)
from store_app import views as store_app_views


urlpatterns = [
    url(r'^admin/logout/$', auth_views.logout, {'next_page': '/admin'}, name="logout"),
    url(r'^admin$', RedirectView.as_view(url='/admin/store_app/product/')),
    url(r'^admin/', admin.site.urls),
    url(r'^product_list/$', store_app_views.ProductList.as_view(), name="product_list"),
    url(r'^product_detail/(?P<pk>\d+)/$', store_app_views.ProductDetail.as_view(), name="product_detail"),
    url(r'', RedirectView.as_view(url='/product_list/')),
]