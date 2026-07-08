function sendEvent(type, win) {
    if (!win) return;

    callDBus(
        "org.zaimu.Desktop",
        "/desktop",
        "org.zaimu.Desktop",
        "WindowEvent",
        type,
        win.resourceClass || "unknown",
        win.caption || ""
    );
}

// ACTIVE WINDOW CHANGE (MOST IMPORTANT)
workspace.activeWindowChanged.connect(function(w) {
    sendEvent("windowActivated", w);
});

// WINDOW OPEN
workspace.windowAdded.connect(function(w) {
    sendEvent("windowAdded", w);
});

// WINDOW CLOSE
workspace.windowRemoved.connect(function(w) {
    sendEvent("windowRemoved", w);
});
