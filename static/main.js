// static/main.js
document.addEventListener("DOMContentLoaded", () => {
  const sendBtn = document.getElementById("send-btn");
  const textarea = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const form = document.getElementById("chat-form");

  if (!sendBtn || !textarea || !chatBox || !form) return;

  sendBtn.addEventListener("click", sendMessage);
  textarea.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      sendMessage();
    }
  });

  async function sendMessage() {
    const text = textarea.value.trim();
    if (!text) return;
    appendMessage("user", text);
    textarea.value = "";
    const endpoint = form.dataset.endpoint;
    const loadingId = appendMessage("bot", "Thinking...");

    try {
      const resp = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });
      const data = await resp.json();
      replaceMessage(loadingId, data.reply || "No response.");
    } catch (err) {
      console.error(err);
      replaceMessage(loadingId, "Error: could not reach server. Check server logs.");
    }
  }

  function appendMessage(who, text) {
    const id = "m" + Date.now() + Math.floor(Math.random()*1000);
    const div = document.createElement("div");
    div.className = "msg " + (who === "user" ? "user" : "bot");
    div.id = id;
    div.innerHTML = <div class="bubble">${escapeHtml(text)}</div>;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return id;
  }

  function replaceMessage(id, newText) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = <div class="bubble">${escapeHtml(newText)}</div>;
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function escapeHtml(s){
    return s
      .replaceAll("&","&amp;")
      .replaceAll("<","&lt;")
      .replaceAll(">","&gt;")
      .replaceAll("\n","<br>");
  }
});
