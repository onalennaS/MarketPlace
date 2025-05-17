from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from seller.wrap_models.product_model import Product
from seller.wrap_models.business_model import BusinessInformation

class ProductSitemap(Sitemap):
	changefreq = "weekly"
	priority = 1.0
	def items(self):
        # You should return a list of tuples (product, business)
		return [
            (product, product.business)  # assuming there's a ForeignKey: product.business -> BusinessInformation
            for product in Product.objects.select_related('business').filter(business__status="approved")
        ]

	def location(self, item):
		product, business = item
		return reverse('view_product', args=[business.slug, product.slug])

class BusinessSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return BusinessInformation.objects.all()  # instead of static strings

    def location(self, item):
        return reverse('view_business_products', args=[item.slug])