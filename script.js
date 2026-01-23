document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const marqueeView = document.getElementById('marquee-view');
    const searchView = document.getElementById('search-view');
    let allBadges = [];

    // Fetch Badges Data
    fetch('badges.json')
        .then(response => response.json())
        .then(data => {
            renderMarquees(data);
            collectAllBadges(data);
        })
        .catch(error => console.error('Error loading badges:', error));

    function renderMarquees(data) {
        let index = 0;
        for (const [category, items] of Object.entries(data)) {
            if (items.length === 0) continue;

            const direction = index % 2 === 0 ? 'marquee-left' : 'marquee-right';
            const section = document.createElement('div');
            section.className = 'category-section';

            // Create enough items to fill screen for smooth scroll
            // We repeat list 6 times if small, 3 times if large
            const repeatCount = items.length < 10 ? 6 : 3;
            let extendedItems = [];
            for (let i = 0; i < repeatCount; i++) {
                extendedItems = extendedItems.concat(items);
            }

            const badgesHTML = extendedItems.map(item => `
                <div class="badge-item" onclick="copyToClipboard('${item.url}')" title="${item.name}">
                    <img src="${item.path}" alt="${item.name}" loading="lazy">
                </div>
            `).join('');

            section.innerHTML = `
                <span class="row-label">${category}</span>
                <div class="marquee-container">
                    <div class="marquee-content ${direction}">
                        ${badgesHTML}
                    </div>
                </div>
            `;

            marqueeView.appendChild(section);
            index++;
        }
    }

    function collectAllBadges(data) {
        for (const [category, items] of Object.entries(data)) {
            items.forEach(item => {
                // Avoid duplicates based on unique path or name
                // Some badges might share names across categories? (unlikely but possible)
                if (!allBadges.find(b => b.path === item.path)) {
                    allBadges.push(item);
                }
            });
        }
    }

    // Search Functionality
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();

        if (query.trim() === '') {
            marqueeView.style.display = 'flex';
            searchView.style.display = 'none';
        } else {
            marqueeView.style.display = 'none';
            searchView.style.display = 'grid';

            const results = allBadges.filter(b => b.name.toLowerCase().includes(query));

            if (results.length > 0) {
                searchView.innerHTML = results.map(b => `
                    <div class="search-result-item" onclick="copyToClipboard('${b.url}')">
                        <img src="${b.path}" alt="${b.name}">
                        <span>${b.name}</span>
                    </div>
                `).join('');
            } else {
                searchView.innerHTML = '<p style="text-align:center; grid-column: 1/-1;">No results found.</p>';
            }
        }
    });

    // Make copy function global so inline onclicks might work (though we didn't use inline in JS generation)
    // Actually we used onclick="copyToClipboard..." in the template above.
    // So we need to expose it to window or attach via delegation.
    // Attaching to window is easiest for the dynamic string templates.
    window.copyToClipboard = function (text) {
        navigator.clipboard.writeText(text).then(() => {
            const toast = document.getElementById("toast");
            toast.className = "show";
            setTimeout(function () { toast.className = toast.className.replace("show", ""); }, 3000);
        });
    };
});
