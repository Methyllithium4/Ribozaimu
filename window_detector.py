import subprocess


def get_active_window_name():
    try:
        win_id = subprocess.check_output(
            ["xdotool", "getactivewindow"],
            text=True
        ).strip()

        name = subprocess.check_output(
            ["xdotool", "getwindowname", win_id],
            text=True
        ).strip()

        return name
    except Exception:
        return None
    
def classify_window(name: str) -> str:
    if not name:
        return None

    name = name.lower()

    # Browser detection
    if any(x in name for x in ["vivaldi", "firefox", "chrome", "edge"]):
        return "browser"

    # PDF detection
    if any(x in name for x in ["pdf", "okular", "evince", "zathura"]):
        return "pdf"

    return "unknown"    