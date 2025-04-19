from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class AuthSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ['signin', 'register', 'logout']

    def location(self, item):
        return reverse(item)
