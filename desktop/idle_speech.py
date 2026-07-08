import random
import time
import csv
from PyQt6.QtCore import QObject


class IdleSpeechManager(QObject):

    def __init__(self, assistant):
        super().__init__()

        self.assistant = assistant

        self.last_trigger = time.time()
        self.next_delay = self.random_delay()

        self.lines = self.load_lines("assets/speech/lines.tsv")

    # -------------------------
    # LOAD TSV
    # -------------------------

    def load_lines(self, path):
        items = []

        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter="\t")
                for row in reader:
                    if len(row) >= 2:
                        items.append((row[0], row[1]))
        except FileNotFoundError:
            print("[IdleSpeech] TSV not found")

        return items

    # -------------------------
    # TIMER LOGIC
    # -------------------------

    def random_delay(self):
        return random.randint(10, 15)  # 1–5 minutes

    def update(self):
        now = time.time()

        if now - self.last_trigger < self.next_delay:
            return

        self.trigger_idle_speech()

        self.last_trigger = now
        self.next_delay = self.random_delay()

    # -------------------------
    # CORE ACTION
    # -------------------------

    def trigger_idle_speech(self):
        if not self.lines:
            return

        text, audio_file = random.choice(self.lines)

        # trigger UI speech
        QTimer.singleShot(0, lambda: self.assistant.set_speech(text))

        # play audio
        self.play_sound(f"assets/speech/{audio_file}")

    # -------------------------
    # AUDIO
    # -------------------------

    def play_sound(self, file):
        subprocess.Popen([
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel",
            "quiet",
            file
        ])