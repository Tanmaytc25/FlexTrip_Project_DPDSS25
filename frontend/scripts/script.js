document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('microtripForm');
  const poiList = document.getElementById('poiList');
  const calendarEl = document.getElementById('calendar');

  // 📅 Initialize FullCalendar
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'timeGridDay',
    editable: true,
    droppable: true,
    height: 'auto',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'timeGridDay,timeGridWeek,dayGridMonth'
    },
    drop: function (info) {
      const draggedEl = info.draggedEl;
      const data = JSON.parse(draggedEl.dataset.event);

      calendar.addEvent({
        title: data.title,
        start: info.date,
        allDay: false,
        duration: data.duration
      });

      console.log(`✅ POI "${data.title}" added to calendar at ${info.date.toISOString()}`);
    }
  });

  calendar.render();

  // 🧠 Handle form submission
  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    poiList.innerHTML = ''; // Clear previous POIs
    calendar.getEvents().forEach(event => event.remove()); // Clear calendar

    const location = document.getElementById('location').value;
    const selectedInterests = Array.from(document.getElementById('interests').selectedOptions).map(opt => opt.value);
    const budget = document.getElementById('budget').value;

    const payload = {
      current_location: location,
      interests: selectedInterests,
      budget: budget ? parseFloat(budget) : null
    };

    try {
      const res = await fetch('http://localhost:5000/api/microtrip/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error(`Server responded with ${res.status}`);

      const data = await res.json();

      if (!data.recommended || data.recommended.length === 0) {
        poiList.innerHTML = '<p>No POIs found. Try other interests.</p>';
        return;
      }

      // 🎯 Render each POI as a draggable item
      data.recommended.forEach((poi) => {
        const poiDiv = document.createElement('div');
        poiDiv.className = 'draggable-poi';
        poiDiv.textContent = `${poi.name} – ${poi.duration_minutes} mins`;
        poiDiv.setAttribute('draggable', 'true');

        // Store POI data for drop
        poiDiv.dataset.event = JSON.stringify({
          title: poi.name,
          duration: `00:${poi.duration_minutes.toString().padStart(2, '0')}`
        });

        poiList.appendChild(poiDiv);
      });

      // 🧲 Make POIs draggable using FullCalendar plugin
      new FullCalendar.Draggable(poiList, {
        itemSelector: '.draggable-poi',
        eventData: function (el) {
          return JSON.parse(el.dataset.event);
        }
      });

    } catch (err) {
      console.error('❌ Error fetching POIs:', err);
      poiList.innerHTML = '<p>Server error. Try again later.</p>';
    }
  });
});
