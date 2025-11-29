# Courier Dashboard Modification Plan

## Information Gathered
- Current dashboard uses `courier/templates/courier/orders.html` extending `courier/templates/courier/base.html`.
- Base.html has an offcanvas sidebar for mobile and collapsed sidebar for desktop.
- Orders.html displays tabbed views for Available, Waiting, In Progress, Completed orders with cards.
- Uses Bootstrap 5, Bootstrap Icons, dark theme.

## Plan
1. Modify `base.html` to implement fixed sidebar with:
   - Top section: Logo and company name
   - Navigation: Dashboard, Available Orders, My Deliveries, Messages, Earnings/Stats, Profile
   - Bottom: Settings, Logout
   - Make sidebar collapsible on mobile

2. Update `orders.html` to:
   - Add header bar with page title, search bar, notification bell, profile avatar
   - Move tab navigation below header
   - Add stats dashboard as default view (Today's deliveries, Total earnings, Pending orders, Completed deliveries)
   - Enhance order cards with better layout and status badges
   - Add visual enhancements: shadows, hover states, icons

3. Ensure responsive design: sidebar collapses on mobile, content stacks vertically

## Dependent Files to Edit
- `courier/templates/courier/base.html`
- `courier/templates/courier/orders.html`

## Followup Steps
- Test layout on different screen sizes
- Verify navigation links work correctly
- Check for any missing URLs or views for new sections (e.g., Messages, Profile)
- Run the app to ensure no template errors
