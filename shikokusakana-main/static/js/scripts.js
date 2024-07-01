document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchFish');
    searchInput.addEventListener('input', function() {
        const filter = searchInput.value.toLowerCase();
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            const title = card.querySelector('.card-title').textContent.toLowerCase();
            if (title.includes(filter)) {
                card.parentElement.style.display = '';
            } else {
                card.parentElement.style.display = 'none';
            }
        });
    });
});
