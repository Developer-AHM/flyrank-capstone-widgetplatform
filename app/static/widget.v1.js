(function () {
  var script = document.currentScript;
  var url = new URL(script.src);
  var widgetId = url.searchParams.get("id");
  var apiBase = url.origin;

  function el(tag, text) {
    var node = document.createElement(tag);
    if (text) node.textContent = text;
    return node;
  }

  fetch(apiBase + "/widgets/" + encodeURIComponent(widgetId) + "/config")
    .then(function (res) {
      if (!res.ok) throw new Error("config request failed: " + res.status);
      return res.json();
    })
    .then(function (cfg) {
      var box = el("div");
      box.className = "lw-widget";
      box.appendChild(el("h3", cfg.title));
      if (cfg.description) box.appendChild(el("p", cfg.description));

      var form = el("form");
      cfg.fields.forEach(function (f) {
        var label = el("label", f.label);
        var input = f.type === "textarea" ? el("textarea") : el("input");
        if (f.type !== "textarea") input.type = f.type;
        input.name = f.name;
        input.required = !!f.required;
        label.appendChild(el("br"));
        label.appendChild(input);
        form.appendChild(label);
        form.appendChild(el("br"));
      });

      var button = el("button", cfg.button_text);
      button.type = "submit";
      form.appendChild(button);
      box.appendChild(form);

      script.parentNode.insertBefore(box, script);
    })
    .catch(function (err) {
      console.error("widget failed to load:", err);
    });
})();