function umami() {
  if (window.location.hostname !== "localhost" && window.location.hostname !== "127.0.0.1") {
    var script = document.createElement("script");
    script.defer = true;
    script.src = "https://umami.ricolxwz.io/script.js";
    script.setAttribute(
      "data-website-id",
      "d50e6f6b-02f0-414c-aceb-b1cf92e9c37f"
    );
    document.head.appendChild(script);
  }
}
umami();
