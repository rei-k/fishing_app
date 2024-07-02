// Improved scripts
document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded.');

    const searchInput = document.querySelector('input[type="search"]');
    searchInput.addEventListener('input', function(event) {
        const query = event.target.value.toLowerCase();
        document.querySelectorAll('.card').forEach(card => {
            const name = card.querySelector('.card-title').textContent.toLowerCase();
            card.style.display = name.includes(query) ? '' : 'none';
        });
    });
});
