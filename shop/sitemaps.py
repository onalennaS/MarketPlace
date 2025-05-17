from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class ShopSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return ['home', 'shop_base','robots_txt']

    def location(self, item):
        return reverse(item)
