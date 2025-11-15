# TODO: Fix ValueError for Business Image in shop_base View

## Steps to Complete:
- [ ] Modify BusinessInformation model in seller/wrap_models/business_model.py: Change image field to allow null and blank, remove invalid default.
- [ ] Create and run Django migration for the model change.
- [ ] Update shop/templates/products/shop1.html template to check if business.image exists before rendering the img tag.
- [ ] Test the fix by running the server and accessing /home/.
