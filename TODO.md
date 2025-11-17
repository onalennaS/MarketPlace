# TODO: Update User Dashboard Sidebar Design

## Overview
Update the sidebar navigation in all user dashboard templates to match the design consistency with the navbar in shop_base2.html. Change from nav flex-column structure to list-group structure used in the mobile menu.

## Files to Update
- user/templates/home/account_settings.html
- user/templates/home/address.html
- user/templates/home/buyer_reviews.html
- user/templates/home/buyer_support.html
- user/templates/home/credit.html
- user/templates/home/gift_card.html
- user/templates/home/order_history.html
- user/templates/home/payment_history.html
- user/templates/home/profile.html
- user/templates/home/referrals_earnings.html
- user/templates/home/subscription_plan.html
- user/templates/home/track_orders.html
- user/templates/home/view_order_details.html
- user/templates/home/wish_lists.html

## Changes Required
1. Replace `<ul class="nav flex-column px-3 mt-3">` with `<div class="list-group list-group-flush">`
2. Replace `<li class="nav-item">` with appropriate structure
3. Replace `<a class="nav-link d-flex align-items-center">` with `<a class="list-group-item list-group-item-action">`
4. Add `<i>` icons and `<span>` text inside links
5. Add `<div class="section-header">` for section headers like "Profile", "Orders", "Payment", "More"
6. Fix "Subscription Plan" link to point to `{% url 'subscription_plan' %}` instead of `{% url 'buyer_support' %}`
7. Ensure active class is applied correctly (e.g., `active` for current page)

## Steps
1. [x] Update account_settings.html
2. [x] Update address.html
3. [x] Update buyer_reviews.html
4. [x] Update buyer_support.html
5. [x] Update credit.html
6. [x] Update gift_card.html
7. [x] Update order_history.html
8. [x] Update payment_history.html
9. [x] Update profile.html
10. [x] Update referrals_earnings.html
11. [x] Update subscription_plan.html
12. [x] Update track_orders.html
13. [x] Update view_order_details.html
14. [x] Update wish_lists.html

## Verification
- Check that sidebar matches mobile menu design
- Ensure all links work correctly
- Verify active states are applied
- Test responsiveness
