document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("http://localhost:5000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password }),
    });

    let data;
    const contentType = res.headers.get("content-type") || "";

    if (contentType.includes("application/json")) {
      data = await res.json();
    } else {
      const text = await res.text();
      throw new Error(text || "Unexpected response format.");
    }

    if (!res.ok) throw new Error(data.message || "Login failed");

    localStorage.setItem("user", JSON.stringify(data.user));
    alert("✅ Login successful!");
    window.location.href = "dashboard.html";
  } catch (err) {
    alert("❌ Login error: " + err.message);
    console.error("Login failed:", err);
  }
});
