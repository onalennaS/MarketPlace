document.addEventListener('DOMContentLoaded', function() {
    const filterItems = document.querySelectorAll('.dropdown-item[data-filter]');
    const orderCards = document.querySelectorAll('.border-bottom.p-3');
    const dropdownButton = document.getElementById('dropdownMenuButton');

    filterItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const filterType = this.getAttribute('data-filter');
            const filterText = this.textContent;

            // Update button text
            dropdownButton.textContent = filterText;

            // Get current date
            const now = new Date();
            let startDate, endDate;

            switch(filterType) {
                case 'today':
                    startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
                    endDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59);
                    break;
                case 'yesterday':
                    startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1);
                    endDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1, 23, 59, 59);
                    break;
                case 'this_week':
                    const weekStart = new Date(now);
                    weekStart.setDate(now.getDate() - now.getDay());
                    startDate = new Date(weekStart.getFullYear(), weekStart.getMonth(), weekStart.getDate());
                    endDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59);
                    break;
                case 'last_week':
                    const lastWeekStart = new Date(now);
                    lastWeekStart.setDate(now.getDate() - now.getDay() - 7);
                    const lastWeekEnd = new Date(now);
                    lastWeekEnd.setDate(now.getDate() - now.getDay() - 1);
                    startDate = new Date(lastWeekStart.getFullYear(), lastWeekStart.getMonth(), lastWeekStart.getDate());
                    endDate = new Date(lastWeekEnd.getFullYear(), lastWeekEnd.getMonth(), lastWeekEnd.getDate(), 23, 59, 59);
                    break;
                case 'last_2_weeks':
                    const twoWeeksAgo = new Date(now);
                    twoWeeksAgo.setDate(now.getDate() - 14);
                    startDate = new Date(twoWeeksAgo.getFullYear(), twoWeeksAgo.getMonth(), twoWeeksAgo.getDate());
                    endDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59);
                    break;
                case 'last_month':
                    const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
                    const lastMonthEnd = new Date(now.getFullYear(), now.getMonth(), 0);
                    startDate = new Date(lastMonth.getFullYear(), lastMonth.getMonth(), lastMonth.getDate());
                    endDate = new Date(lastMonthEnd.getFullYear(), lastMonthEnd.getMonth(), lastMonthEnd.getDate(), 23, 59, 59);
                    break;
                case 'last_3_months':
                    const threeMonthsAgo = new Date(now);
                    threeMonthsAgo.setMonth(now.getMonth() - 3);
                    startDate = new Date(threeMonthsAgo.getFullYear(), threeMonthsAgo.getMonth(), threeMonthsAgo.getDate());
                    endDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59);
                    break;
                default:
                    // Show all orders
                    orderCards.forEach(card => card.style.display = 'block');
                    return;
            }

            // Filter orders
            orderCards.forEach(card => {
                const dateElement = card.querySelector('.date-to-filter');
                if (dateElement) {
                    const orderDateText = dateElement.textContent.trim();
                    const orderDate = parseDate(orderDateText);

                    if (orderDate >= startDate && orderDate <= endDate) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                }
            });
        });
    });

    // Function to parse date in format "Oct. 27, 2025, 2:05 a.m."
    function parseDate(dateString) {
        // Remove the period at the end if present
        dateString = dateString.replace(/\.$/, '');

        // Split date and time
        const parts = dateString.split(', ');
        if (parts.length !== 3) return new Date(0);

        const datePart = parts[0] + ', ' + parts[1]; // "Oct. 27, 2025"
        const timePart = parts[2]; // "2:05 a.m."

        // Parse time
        const timeMatch = timePart.match(/(\d+):(\d+)\s*(a\.m\.|p\.m\.)/);
        if (!timeMatch) return new Date(0);

        let hours = parseInt(timeMatch[1]);
        const minutes = parseInt(timeMatch[2]);
        const ampm = timeMatch[3];

        if (ampm === 'p.m.' && hours !== 12) {
            hours += 12;
        } else if (ampm === 'a.m.' && hours === 12) {
            hours = 0;
        }

        // Create date object
        const date = new Date(datePart);
        date.setHours(hours, minutes, 0, 0);

        return date;
    }
});
