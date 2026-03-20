function toggleLike(articleId) {
    // 1. Достаем защитный токен со страницы
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // 2. Отправляем запрос
    fetch(`/like/${articleId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken, // Передаем найденный токен
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Пожалуйста, войдите в аккаунт, чтобы ставить лайки!");
            return;
        }

        // 3. Ищем счетчик ИМЕННО для этой статьи и обновляем цифру
        document.getElementById(`like-count-${articleId}`).innerText = data.total_likes;

        // 4. Ищем кнопку ИМЕННО для этой статьи и закрашиваем её
        const btn = document.getElementById(`like-btn-${articleId}`);
        if (data.liked) {
            btn.classList.add("liked");
        } else {
            btn.classList.remove("liked");
        }
    })
    .catch(error => console.error("Ошибка при отправке лайка:", error));
}

