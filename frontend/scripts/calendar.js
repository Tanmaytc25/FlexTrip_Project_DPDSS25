document.addEventListener('DOMContentLoaded', function () {
  const calendarEl = document.getElementById('calendar');
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
      // You could implement a save-to-DB here if needed
      console.log(`🗓️ Dropped: ${info.draggedEl.innerText}`);
    }
  });

  calendar.render();

  // Microtrip form logic
  const form = document.getElementById('microtripForm');
  const output = document.getElementById('output');

  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const location = form.location.value;
    const selectedInterests = Array.from(form.interests.selectedOptions).map(opt => opt.value);
    const budget = form.budget.value ? parseFloat(form.budget.value) : null;

    const data = {
      current_location: location,
      interests: selectedInterests,
      budget: budget
    };

    const response = await fetch('http://localhost:5000/api/microtrip/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    output.textContent = JSON.stringify(result, null, 2);

    const suggestionsEl = document.getElementById('poi-suggestions');
    suggestionsEl.innerHTML = ''; // Clear previous

    if (result.recommended && result.recommended.length > 0) {
      result.recommended.forEach((poi, index) => {
        const item = document.createElement('div');
        item.className = 'poi-item';
        item.textContent = poi.name;
        item.setAttribute('data-duration', poi.duration_minutes || 60);

        // Make draggable
        new FullCalendar.Draggable(item, {
          eventData: {
            title: poi.name,
            duration: `${poi.duration_minutes || 60}m`
          }
        });

        suggestionsEl.appendChild(item);
      });
    } else {
      suggestionsEl.innerHTML = '<p>No suggestions found.</p>';
    }
  });
});
