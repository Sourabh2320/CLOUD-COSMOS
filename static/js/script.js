// Smooth scroll to insights panel
document.addEventListener('DOMContentLoaded', function () {
    const forecastElement = document.querySelector('.forecast');
    if (forecastElement) {
        forecastElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
});

// Confirm before deleting an expense
const deleteButtons = document.querySelectorAll('.delete-btn');
deleteButtons.forEach(btn => {
    btn.addEventListener('click', function (e) {
        const confirmDelete = confirm("Are you sure you want to delete this expense?");
        if (!confirmDelete) {
            e.preventDefault();
        }
    });
});
