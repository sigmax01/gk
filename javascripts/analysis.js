function umami() {
  if (window.location.hostname !== "localhost" && window.location.hostname !== "127.0.0.1") {
    var script = document.createElement("script");
    script.defer = true;
    script.src = "https://cloud.umami.is/script.js";
    script.setAttribute(
      "data-website-id",
      "4ff41d98-fbf4-4444-b816-16546dd5a9ea"
    );
    document.head.appendChild(script);
  }
}
umami();
