const CACHE_TTL = 1000 * 60 * 5; // 5 минут

async function loadUser(userId) {
    const cacheKey = `user_cache_${userId}`;
    const timeKey = `user_cache_${userId}_time`;

    const cached = localStorage.getItem(cacheKey);
    const cachedTime = localStorage.getItem(timeKey);

    const isValid = cached && cachedTime && (Date.now() - parseInt(cachedTime)) < CACHE_TTL;

    if (isValid) {
        return JSON.parse(cached);
    }

    // если кэш просрочен или отсутствует — запрашиваем заново
    try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
            document.getElementsByClassName("profile-main__wrapper")[0].innerHTML = `<h2>Пользователь не найден</h2>`
            throw new Error("Пользователь не найден");
        };

        const data = await response.json();

        localStorage.setItem(cacheKey, JSON.stringify(data));
        localStorage.setItem(timeKey, Date.now().toString());

        return data;
    } catch (error) {
        console.error("Ошибка при загрузке пользователя:", error);

        // на случай сбоя — отдаём старые данные, если есть
        if (cached) {
            return JSON.parse(cached);
        } else {
            throw error;
        }
    }
}