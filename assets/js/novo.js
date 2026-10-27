// Mostra os vídeos mais recentes do canal (gerados em videos.json pelo GitHub Action).
(async () => {
    const box = document.querySelector('[data-videos]');
    if (!box) return;
    try {
        const res = await fetch('videos.json', { cache: 'no-cache' });
        if (!res.ok) return;
        const videos = (await res.json())
            .sort((a, b) => b.published.localeCompare(a.published))
            .slice(0, Number(box.dataset.videos) || 3);
        if (!videos.length) return;

        const fmt = new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' });
        const tpl = box.querySelector('.episode');

        box.replaceChildren(...videos.map(({ id, title, published }) => {
            const el = tpl.cloneNode(true);
            el.href = `https://www.youtube.com/watch?v=${id}`;
            const img = el.querySelector('img');
            img.src = `https://i.ytimg.com/vi/${id}/hqdefault.jpg`;
            img.alt = title;
            el.querySelector('.ep-tag').textContent = fmt.format(new Date(published));
            el.querySelector('.ep-title').textContent = title;
            return el;
        }));
    } catch {
        /* mantém os cards estáticos do HTML */
    }
})();
