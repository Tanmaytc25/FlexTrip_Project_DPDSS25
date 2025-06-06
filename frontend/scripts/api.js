// ✅ api.js — Central API functions and auth utilities

const API_BASE = "http://localhost:5000/api";

// ✅ Token Management
export function getToken() {
  return localStorage.getItem("token");
}

export function setToken(token) {
  localStorage.setItem("token", token);
}

export function logout() {
  localStorage.removeItem("token");
}

// ✅ Helper for making authenticated API requests
async function authFetch(url, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(url, { ...options, headers });

  if (!res.ok) {
    let error;
    try {
      error = await res.json();
    } catch {
      error = { error: "Unknown error" };
    }
    throw new Error(error.error || "API request failed");
  }

  return res.json();
}

// ✅ Create Micro Trip
export async function createMicroTrip(data) {
  return await authFetch(`${API_BASE}/microtrip/generate`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

// ✅ Create a Trip from Micro Trip suggestion
export async function createTrip(data) {
  return await authFetch(`${API_BASE}/trips/create`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

// ✅ User Login
export async function login(email, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: "Login failed" }));
    throw new Error(error.error || "Login failed");
  }

  const data = await res.json();
  setToken(data.access_token);
  return data;
}

// ✅ Register New User
export async function register(userData) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: "Registration failed" }));
    throw new Error(error.error || "Registration failed");
  }

  const data = await res.json();
  setToken(data.access_token);
  return data;
}

// ✅ Fetch current user's trips
export async function fetchTrips() {
  return await authFetch(`${API_BASE}/trips`);
}
