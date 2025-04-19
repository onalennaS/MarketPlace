
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class UserSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [ 'seller_landing_page']

    def location(self, item):
        return reverse(item)