from dataclasses import dataclass


@dataclass
class DesktopEvent:
    type: str
    app: str = ""
    title: str = ""