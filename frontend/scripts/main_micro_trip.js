import { createMicroTrip, createTrip, getToken, logout } from "./api.js";

console.log("✅ main_micro_trip.js loaded!");

// ✅ Token expiration checker
function isTokenExpired(token) {
  if (!token) return true;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return Date.now() >= payload.exp * 1000;
  } catch {
    return true;
  }
}

// ✅ Auto-logout if token is expired
const token = getToken();
if (isTokenExpired(token)) {
  alert("⚠️ Your session has expired. Please log in again.");
  logout();
  window.location.href = "login.html";
}

let lastMicroTripResponse = null;
let calendarConnected = false;

document.addEventListener("DOMContentLoaded", async () => {
  const form = document.getElementById("microTripForm");
  const resultEl = document.getElementById("microTripResult");
  const saveBtn = document.getElementById("saveTripBtn");
  const syncBtn = document.getElementById("syncCalendarBtn");

  // ✅ Check if calendar is connected
  try {
    const res = await fetch("http://localhost:5000/api/oauth/calendar/status", {
      headers: { Authorization: `Bearer ${getToken()}` }
    });
    const data = await res.json();
    calendarConnected = data.connected;
    console.log(`📆 Calendar connected: ${calendarConnected}`);

    if (calendarConnected) {
      document.getElementById("calendar").insertAdjacentHTML("afterbegin", `<p style="color: green;">✅ Google Calendar connected</p>`);
    }
  } catch (err) {
    console.error("❌ Failed to check calendar connection:", err);
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("🚀 Micro-trip form submitted!");

    const today = new Date().toISOString().split("T")[0];

    const payload = {
      current_location: document.getElementById("location").value,
      start_time: `${today}T${document.getElementById("startTime").value}:00`,
      end_time: `${today}T${document.getElementById("endTime").value}:00`,
      interests: Array.from(document.getElementById("interests").selectedOptions).map(opt => opt.value),
      budget: parseFloat(document.getElementById("budget").value),
      events: [{
        name: "Placeholder Event",
        start_time: `${today}T12:00:00`,
        end_time: `${today}T13:00:00`
      }]
    };

    console.log("📦 Sending micro-trip payload:", payload);

    try {
      const response = await createMicroTrip(payload);
      console.log("✅ Micro-trip result:", response);
      lastMicroTripResponse = response;

      if (response.recommended?.length) {
        resultEl.innerHTML = `
          <h3>Recommended Micro Trip:</h3>
          <div class="poi-cards">
            ${response.recommended.map(item => `
              <div class="poi-card" draggable="true" data-id="${item.name}">
                <h4>${item.name}</h4>
                <p><strong>Location:</strong> ${item.location}</p>
                <p><strong>Interest:</strong> ${item.interest}</p>
                <p><strong>Duration:</strong> ${item.duration_minutes} min</p>
                <p><strong>Cost:</strong> €${item.estimated_cost} (${item.price_range})</p>
                <p>${item.description}</p>
              </div>
            `).join("")}
          </div>
        `;

        // 🟢 Prepare drag handlers
        document.querySelectorAll(".poi-card").forEach(card => {
          card.addEventListener("dragstart", (e) => {
            e.dataTransfer.setData("text/plain", e.target.dataset.id);
          });
        });

        saveBtn.style.display = "inline-block";
        syncBtn.style.display = "none";
      } else {
        resultEl.innerHTML = `<p>❗ No suggestions found. Try adjusting your inputs.</p>`;
        saveBtn.style.display = "none";
        syncBtn.style.display = "none";
      }
    } catch (err) {
      console.error("❌ Micro-trip generation failed:", err);
      resultEl.innerHTML = `<p>Error: ${err.message}</p>`;
      saveBtn.style.display = "none";
      syncBtn.style.display = "none";
    }
  });

  saveBtn.addEventListener("click", async () => {
    if (!lastMicroTripResponse?.recommended?.length) return;

    const today = new Date().toISOString().split("T")[0];

    const tripData = {
      name: "Saved Micro Trip",
      description: "Trip auto-generated from micro-trip suggestion.",
      destination: lastMicroTripResponse.recommended[0]?.location || "Unknown",
      start_date: today,
      end_date: today,
      budget: parseFloat(document.getElementById("budget").value),
      travel_pace: "moderate",
      interests: Array.from(document.getElementById("interests").selectedOptions).map(opt => opt.value),
      destinations: lastMicroTripResponse.recommended.map(poi => ({
        name: poi.name,
        location: poi.location,
        description: poi.description,
        interest: poi.interest,
        estimated_cost: poi.estimated_cost,
        duration_minutes: poi.duration_minutes,
        price_range: poi.price_range
      }))
    };

    try {
      const result = await createTrip(tripData);
      alert("✅ Trip saved successfully!");
      console.log("📝 Trip save response:", result);

      syncBtn.setAttribute("data-trip-id", result.trip_id);
      syncBtn.style.display = "inline-block";

      if (calendarConnected) {
        await triggerCalendarSync(result.trip_id);
      }
    } catch (err) {
      console.error("❌ Failed to save trip:", err);
      alert("Failed to save trip.");
      syncBtn.style.display = "none";
    }
  });

  syncBtn.addEventListener("click", async () => {
    const tripId = syncBtn.getAttribute("data-trip-id");
    if (!tripId) {
      alert("⚠️ No trip ID found. Please save the trip first.");
      return;
    }
    await triggerCalendarSync(tripId);
  });

  async function triggerCalendarSync(tripId) {
    try {
      const res = await fetch(`http://localhost:5000/api/oauth/calendar/sync/${tripId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${getToken()}`
        }
      });

      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.error || "Unknown error during calendar sync.");
      }

      alert("📆 Trip successfully synced to your Google Calendar!");
    } catch (err) {
      console.error("❌ Calendar sync error:", err);
      alert(`❌ Calendar sync failed: ${err.message}`);
    }
  }
});
