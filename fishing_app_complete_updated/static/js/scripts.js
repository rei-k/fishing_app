// 改良されたスクリプト
document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded.');

    const searchInput = document.querySelector('input[type="search"]');
    searchInput.addEventListener('input', function(event) {
        const query = event.target.value.trim().toLowerCase(); // trim()で前後の空白を削除する
        document.querySelectorAll('.card').forEach(card => {
            const title = card.querySelector('.card-title').textContent.trim().toLowerCase(); // trim()で前後の空白を削除する
            card.style.display = title.includes(query) ? '' : 'none';
        });
    });
});
