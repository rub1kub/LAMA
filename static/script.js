document.addEventListener('DOMContentLoaded', () => {
  let selectedCoordinates = null;
  let myMap, myPlacemark;

  const mainContent = document.getElementById('mainContent');
  const inputPanel = document.getElementById('inputPanel');
  const mapContainer = document.getElementById('mapContainer');
  const llamaBubble = document.getElementById('parallax-bubble');
  const button = document.getElementById('getRecommendations');
  const confirmBtn = document.getElementById('confirmPoint');
  const closeBtn = document.getElementById('closeMap');

  const loader = document.getElementById('loader');
  const resultsContainer = document.getElementById('resultsContainer');
  const recommendationBlock = document.getElementById('recommendationContent');
  const competitorsBlock = document.getElementById('competitorCards');

  document.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 30;
    const y = (e.clientY / window.innerHeight - 0.5) * 30;

    const targets = [
      { id: "parallax-lama", depth: 0.4 },
      { id: "parallax-bubble", depth: 0.6 },
      { id: "parallax-leaves", depth: 0.2 },
      { id: "parallax-leaves2", depth: 0.3 }
    ];

    targets.forEach(({ id, depth }) => {
      const el = document.getElementById(id);
      if (!el) return;
      const rotate = el.dataset.rotate ? `rotate(${el.dataset.rotate})` : '';
      el.style.transform = `${rotate} translate(${x * depth}px, ${y * depth}px)`;
    });
  });

  button.addEventListener('click', () => {
    mainContent.classList.add('expanded');
    inputPanel.classList.add('hidden');
    mapContainer.classList.remove('map-hidden');
    mapContainer.classList.add('map-visible');
    initMap();
  });

  closeBtn.addEventListener('click', () => {
    mainContent.classList.remove('expanded');
    inputPanel.classList.remove('hidden');
    mapContainer.classList.remove('map-visible');
    mapContainer.classList.add('map-hidden');
    if (myMap) {
      myMap.destroy();
      myMap = null;
    }
    selectedCoordinates = null;
  });

  confirmBtn.addEventListener('click', async () => {
    if (!selectedCoordinates) {
      alert("Пожалуйста, выберите точку на карте");
      return;
    }

    console.log("Координаты выбраны:", selectedCoordinates);

    mainContent.classList.remove('expanded');
    mapContainer.classList.remove('map-visible');
    llamaBubble.style.display = "none";
    mainContent.style.display = "none";
    loader.style.display = "block";

    await Promise.all([
      fetchRecommendations(),
      fetchCompetitors()
    ]);

    loader.style.display = "none";
    resultsContainer.classList.remove("results-hidden");
  });

  function initMap() {
    ymaps.ready(() => {
      myMap = new ymaps.Map("map", {
        center: [55.751244, 37.618423],
        zoom: 12,
        controls: ['zoomControl', 'geolocationControl']
      });

      myMap.events.add('click', function (e) {
        const coords = e.get('coords');
        selectedCoordinates = coords;
        console.log("Выбраны координаты:", coords);
        if (myPlacemark) {
          myPlacemark.geometry.setCoordinates(coords);
        } else {
          myPlacemark = new ymaps.Placemark(coords, {
            hintContent: 'Вы выбрали эту точку',
            balloonContent: 'Местоположение выбрано'
          }, {
            preset: 'islands#violetDotIconWithCaption',
            draggable: true
          });
          myMap.geoObjects.add(myPlacemark);
        }
      });
    });
  }

  async function fetchRecommendations() {
    const [lat, lon] = selectedCoordinates;
    console.log("Запрос рекомендаций...");

    try {
      const response = await fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lat, lon, type: "кофейня", business: {} })
      });
      const data = await response.json();
      console.log("Ответ рекомендаций:", data);

      if (data.analysis) {
        const analysis = document.createElement('p');
        analysis.innerText = data.analysis;
        recommendationBlock.appendChild(analysis);
      }

      if (Array.isArray(data.recommendations)) {
        const list = document.createElement('ul');
        data.recommendations.forEach(rec => {
          const li = document.createElement('li');
          li.innerText = rec;
          list.appendChild(li);
        });
        recommendationBlock.appendChild(list);
      }
    } catch (err) {
      console.error("Ошибка при получении рекомендаций:", err);
      recommendationBlock.innerHTML = "<p>Ошибка загрузки рекомендаций.</p>";
    }
  }

  async function fetchCompetitors() {
    const [lat, lon] = selectedCoordinates;
    console.log("Запрос конкурентов...");

    try {
      const response = await fetch('/competitors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lat, lon, type: "кофейня" })
      });

      const data = await response.json();
      console.log("Ответ конкурентов:", data);

      const competitors = data.competitors || [];

      if (competitors.length === 0) {
        competitorsBlock.innerHTML = "<p>Конкуренты не найдены.</p>";
        return;
      }

      competitors.forEach(biz => {
        const card = document.createElement('div');
        card.className = 'competitor-card';

        const name = document.createElement('h3');
        name.innerText = biz.name || 'Без названия';
        card.appendChild(name);

        if (biz.address) {
          const address = document.createElement('p');
          address.innerText = `📍 ${biz.address}`;
          card.appendChild(address);
        }

        if (biz.url) {
          const site = document.createElement('p');
          site.innerHTML = `<a href="${biz.url}" target="_blank">🌐 Сайт</a>`;
          card.appendChild(site);
        }

        if (biz.vk) {
          const vk = document.createElement('p');
          vk.innerHTML = `<a href="${biz.vk}" target="_blank">VK</a>`;
          card.appendChild(vk);
        }
        if (biz.telegram) {
          const tg = document.createElement('p');
          tg.innerHTML = `<a href="${biz.telegram}" target="_blank">Telegram</a>`;
          card.appendChild(tg);
        }
        competitorsBlock.appendChild(card);
      });
    } catch (err) {
      console.error("Ошибка при получении конкурентов:", err);
      competitorsBlock.innerHTML = "<p>Ошибка загрузки данных о конкурентах.</p>";
    }
  }
});