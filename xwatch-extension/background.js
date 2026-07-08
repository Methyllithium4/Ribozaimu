function notifyAssistant(message) {
    fetch("http://127.0.0.1:8769/", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message })
    }).catch(err => console.error("Bridge error:", err));
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (!tab.url) return;

    if (changeInfo.status === "complete") {
        if (tab.url.includes("x.com")) {
            notifyAssistant("Baka baka baaaaka! Browsing twitter again instead of studying? How low can you sink lol");
        }
        if (tab.url.includes("youtube.com")) {
            notifyAssistant("Wasting time on Youtube??? For real?? Ahahaha! Get your ass out of there and go back to studying!");
        }
    }


});
