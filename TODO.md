# TODO: Update shop_base2.html to hide "My Account" link for sellers

## Tasks
- [x] Add condition to hide "My Account" link in desktop navigation for sellers (group "business")
- [x] Add condition to hide "My Account" link in mobile bottom navigation for sellers (group "business")
- [x] Verify changes in the file

## Notes
- Sellers are identified by being in the "business" group.
- Use {% if not user.groups.filter(name="business").exists %} to check if user is not a seller.
- Changes verified: "My Account" link is properly hidden for sellers in both desktop and mobile navigation using the is_business_user context variable.
