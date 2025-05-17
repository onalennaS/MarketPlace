"""
URL configuration for Market project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from authenticator import views
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from shop.sitemaps import ShopSitemap


from authenticator.sitemaps import AuthSitemap
from user.sitemaps import UserSitemap
from seller.sitemaps import SellerSitemap



sitemaps_dict = {
    'products': ShopSitemap,
    'auth': AuthSitemap,
    'user': UserSitemap,
     'shop': ShopSitemap,
      'seller': SellerSitemap,

}
from django.views.generic import TemplateView

urlpatterns = [
    path('god_level/', admin.site.urls),
    path('',include('shop.urls')),
    path('seller/',include('seller.urls')),
    path('courier/',include('courier.urls')),
    path('auth/', include('authenticator.urls')),
    path('account/', include('user.urls')),
    path('accounts/', include('allauth.urls')),
    path('shop/',include('shop.urls')),
     path('moderator/',include('moderator.urls')),
    path('administrator/',include('administrator.urls')),
    path('transactions/', include('transactions.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps_dict}, name='sitemap'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
