from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class SellerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return [ 'business', 'register_business_form']

    def location(self, item):
        return reverse(item)