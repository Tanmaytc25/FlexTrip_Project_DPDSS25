// ✅ main.js — Trip suggestion and submission logic

import { getToken, logout, createTrip } from "./api.js";

console.log("✅ main.js loaded!");

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

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("tripForm");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;
    const destination = document.getElementById("destination").value;
    const interests = Array.from(document.getElementById("interests").selectedOptions).map(opt => opt.value);
    const budget = parseFloat(document.getElementById("budget").value);
    const pace = document.getElementById("pace").value;

    const payload = {
      name: "User Trip",
      description: "A user-created trip",
      destination,
      start_date: startDate,
      end_date: endDate,
      budget,
      travel_pace: pace,
      interests,
      destinations: [] // Can be filled later
    };

    try {
      const result = await createTrip(payload);
      alert("✅ Trip created successfully!");
      console.log("📝 Trip creation result:", result);
      // Optionally reset form
      form.reset();
    } catch (err) {
      console.error("❌ Trip creation failed:", err);
      alert(`❌ Failed to create trip: ${err.message}`);
    }
  });
});
