// ✅ dashboard.js — Handles displaying user trips and logout

import { getToken, logout } from "./api.js";

console.log("✅ dashboard.js loaded!");

function isTokenExpired(token) {
  if (!token) return true;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return Date.now() >= payload.exp * 1000;
  } catch {
    return true;
  }
}

const token = getToken();
if (isTokenExpired(token)) {
  alert("⚠️ Your session has expired. Please log in again.");
  logout();
  window.location.href = "login.html";
}

document.addEventListener("DOMContentLoaded", async () => {
  const tripList = document.getElementById("tripList");
  const logoutBtn = document.getElementById("logoutBtn");

  logoutBtn.addEventListener("click", () => {
    logout();
    window.location.href = "login.html";
  });

  try {
    const res = await fetch("http://localhost:5000/api/trips", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      throw new Error("Failed to fetch trips.");
    }

    const trips = await res.json();

    if (!trips.length) {
      tripList.innerHTML = "<p>No trips found.</p>";
      return;
    }

    tripList.innerHTML = trips
      .map(
        (trip) => `
      <div class="trip">
        <h3>${trip.name}</h3>
        <p><strong>Destination:</strong> ${trip.destination}</p>
        <p><strong>Dates:</strong> ${trip.start_date} to ${trip.end_date}</p>
        <p><strong>Budget:</strong> €${trip.budget}</p>
        <p><strong>Travel Pace:</strong> ${trip.travel_pace}</p>
        <p><strong>Interests:</strong> ${trip.interests?.join(", ") || "N/A"}</p>
        <a href="trip_detail.html?trip_id=${trip.id}">View Details</a>
      </div>
    `
      )
      .join("");
  } catch (err) {
    console.error("❌ Failed to load trips:", err);
    tripList.innerHTML = `<p>Error loading trips: ${err.message}</p>`;
  }
});
