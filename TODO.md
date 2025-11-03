# Moderator Dashboard Functionalization Tasks

## Overview
Make the moderator dashboard functional by replacing hard-coded values with dynamic data fetched from the database. Update the view to query relevant models and pass data to the template.

## Tasks
- [ ] Update `moderator/views/render_views.py` dashboard view to fetch real data:
  - Business moderations (approved, rejected, pending counts)
  - Product moderations (approved, rejected, pending counts)
  - User count
  - Courier count
  - Comments count (if model exists, else set to 0)
  - Dynamic notifications based on pending moderations
  - Chart data: Aggregate user/business growth over time (e.g., by month)
- [ ] Update `moderator/templates/moderator/dashboard.html` to use context variables instead of hard-coded values
- [ ] Test the dashboard to ensure data loads correctly
- [ ] Handle edge cases (e.g., no data available)

## Dependencies
- Models: Moderation, ProductModeration, User, Courier
- If comments model exists, integrate it

## Next Steps
- After updating view, render template with dynamic data
- Verify charts display correctly with aggregated data
