from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from shop.sitemaps import ShopSitemap
from shop.productSitemap import ProductSitemap, BusinessSitemap
from authenticator.sitemaps import AuthSitemap
from user.sitemaps import UserSitemap
from seller.sitemaps import SellerSitemap

sitemaps_dict = {
    'business': BusinessSitemap,
    'products': ProductSitemap,
    'auth': AuthSitemap,
    'user': UserSitemap,
    'shop': ShopSitemap,
    'seller': SellerSitemap,
}

urlpatterns = [
    path('god_level/', admin.site.urls),
    
    # IMPORTANT: Put specific paths BEFORE the catch-all shop path!
    path('auth/', include('authenticator.urls')),
    path('account/', include('user.urls')),
    path('accounts/', include('allauth.urls')),
    path('seller/', include('seller.urls')),
    path('courier/', include('courier.urls')),
    path('moderator/', include('moderator.urls')),  # MOVED UP!
    path('administrator/', include('administrator.urls')),
    path('transactions/', include('transactions.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps_dict}, name='sitemap'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    
    # Shop URLs LAST - because it has catch-all patterns
    path('', include('shop.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)