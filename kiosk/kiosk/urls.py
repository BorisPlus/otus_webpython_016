from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import (
    HttpResponseRedirect,
)
try:
    from kiosk.store_app import views as store_app_views
except:
    from store_app import views as store_app_views


def admin_default(request):
    if request:
        pass
    return HttpResponseRedirect('/admin/store_app/product/')


def default(request):
    if request:
        pass
    return HttpResponseRedirect('/product_list/')


urlpatterns = [
    url(r'^admin/logout/$', auth_views.logout, {'next_page': '/admin'}, name="logout"),
    url(r'^admin$', admin_default),
    url(r'^admin/', admin.site.urls),
    url(r'^product_list/$', store_app_views.ProductList.as_view()),
    url(r'^product_detail/(?P<pk>\d+)/$', store_app_views.ProductDetail.as_view()),
    url(r'^test/$', store_app_views.test),
    url(r'', default),
]