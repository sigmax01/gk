function umami() {
  if (window.location.hostname !== "localhost" && window.location.hostname !== "127.0.0.1") {
    var script = document.createElement("script");
    script.defer = true;
    script.src = "https://umami.ricolxwz.io/script.js";
    script.setAttribute(
      "data-website-id",
      "6e8f6608-3bbc-45fb-aaa0-3b8e47388d2d"
    );
    document.head.appendChild(script);
  }
}
umami();
