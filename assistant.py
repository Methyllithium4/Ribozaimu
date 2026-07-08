import sys
import subprocess
import random
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPainter, QPixmap, QTransform
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPen, QColor
from PyQt6.QtCore import QRect
from window_detector import get_active_window_name
from window_detector import classify_window  # or keep in same file

from desktop_bridge import DesktopBridge
from desktop.reactions import Reaction
from desktop.idle_speech import IdleSpeechManager

from behaviour import BehaviourController
from bridge_server import BridgeServer

class AssistantWindow(QWidget):
    def __init__(self):
        super().__init__()

        # -----------------------------
        # WINDOW
        # -----------------------------
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.resize(350, 350)

        # -----------------------------
        # SPRITES
        # -----------------------------
        self.sprites = {
            "idle_1": QPixmap("assets/idle_bored.png"),
            "idle_2": QPixmap("assets/idle_bored2.png"),
            "blink_1": QPixmap("assets/idle_bored_blink.png"),
            "blink_2": QPixmap("assets/idle_bored_blink2.png"),
        }

        self.speech_bubble = QPixmap("assets/speech_bubble.png")

        self.is_blinking = False

        # -----------------------------
        # SPEECH SYSTEM
        # -----------------------------
        self.full_text = "Finally going to study, eh? I wanna see you try, zaaako~"
        self.visible_text = ""
        self.text_index = 0

        self.speech_active = True

        # timers
        self.type_timer = QTimer(self)
        self.type_timer.timeout.connect(self.type_next_char)
        self.type_timer.start(40)

        self.speech_timer = QTimer(self)
        self.speech_timer.setSingleShot(True)
        self.speech_timer.timeout.connect(self.hide_speech)
        self.speech_timer.start(5000)
        
        self.random_event_timer = QTimer(self)
        self.random_event_timer.timeout.connect(self.random_event)
        self.reset_random_timer()

        # -----------------------------
        # STATE
        # -----------------------------
        self.drag_offset = QPoint()

        # -----------------------------
        # BEHAVIOUR
        # -----------------------------
        self.behaviour = BehaviourController(self)
        
        self.faces = {
            "idle": QPixmap("assets/idle_face.png"),
            "blink": QPixmap("assets/blink_face.png"),
            "talk": QPixmap("assets/talking_face.png"),
        }
        
        self.idle_speech = IdleSpeechManager(self)
        
        
        # -----------------------------
        # Window recognition
        # -----------------------------
        
        self.last_window = None
        self.window_timer = QTimer(self)
        self.window_timer.timeout.connect(self.check_window)
        self.window_timer.start(5000)
        
        self.bridge = BridgeServer(self)
        self.bridge.start()
        
        # -----------------------------
        # MAIN LOOP
        # -----------------------------
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)

        self.show()

    # -----------------------------
    # SPEECH LOGIC
    # -----------------------------

    def type_next_char(self):
        if not self.speech_active:
            return
    
        if self.text_index < len(self.full_text):
            self.visible_text += self.full_text[self.text_index]
            self.text_index += 1
        else:
            self.type_timer.stop()
    
        self.update()

    def hide_speech(self):
        self.speech_active = False
        self.update()

    def reset_speech(self, text):
        self.full_text = text
        self.visible_text = ""
        self.text_index = 0
        self.speech_active = True

        self.type_timer.start(40)
        self.speech_timer.start(5000)
        
    def get_face_key(self):
        # speech overrides everything
        if self.speech_active:
            return "talk"
    
        if self.is_blinking:
            return "blink"
    
        return "idle"

    # -----------------------------
    # ANIMATION
    # -----------------------------

    def get_frame_key(self):
        phase = self.behaviour.get_anim_phase()
        frame = 1 if phase < 0.5 else 2

        return f"blink_{frame}" if self.is_blinking else f"idle_{frame}"

    # -----------------------------
    # LOOP
    # -----------------------------

    def tick(self):
        self.idle_speech.update()
        self.update()
        
    def reset_random_timer(self):
        # 1–5 minutes in milliseconds
        delay_ms = random.randint(190_000, 1_000_0000)
        self.random_event_timer.start(delay_ms)
        
    def random_event(self):
        # 🔊 choose what to say
        messages = [
            ("Hey there, stinky~", "baka-mitsuba.mp3"),
            ("Baaka ♡", "baka-mitsuba2.mp3"),
            ("I bet you can't even explain to me the last lecture you studied", "100-baka.mp3"),
            ("Heard some rumors saying you were smart, too bad they seem to be false", "baka-mitsuba.mp3"),
        ]
    
        text, sound = random.choice(messages)
    
        # 🗣 trigger speech bubble
        self.set_speech(text)
    
        # 🔊 play sound
        self.play_sound(sound)
    
        # 🔁 reschedule next event
        self.reset_random_timer()
        
    # -----------------------------
    # INPUT
    # -----------------------------

    def mousePressEvent(self, event):
        # click anywhere dismisses speech
        if self.speech_active:
            self.hide_speech()

        self.drag_offset = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        self.move(event.globalPosition().toPoint() - self.drag_offset)

    def mouseDoubleClickEvent(self, event):
        sys.exit(0)

    # -----------------------------
    # RENDER
    # -----------------------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # -----------------------------
        # SPRITE
        # -----------------------------
        frame_key = self.get_frame_key()
        sprite = self.sprites[frame_key]

        if self.behaviour.is_facing_right():
            sprite = sprite.transformed(
                QTransform().scale(-1, 1),
                Qt.TransformationMode.SmoothTransformation
            )

        bob = self.behaviour.get_bob_offset()

        scaled = sprite.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2 + int(bob)

        painter.drawPixmap(x, y, scaled)
        # -----------------------------
        # FACE OVERLAY
        # -----------------------------
        face_key = self.get_face_key()
        face = self.faces[face_key]
        
        # face follows same flip direction as body
        if self.behaviour.is_facing_right():
            face = face.transformed(
                QTransform().scale(-1, 1),
                Qt.TransformationMode.SmoothTransformation
            )
        
        # scale face to match body scaling
        face_scaled = face.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        # IMPORTANT: same position + bob so it sticks perfectly
        painter.drawPixmap(x, y, face_scaled)
        # -----------------------------
        # SPEECH BUBBLE
        # -----------------------------
        if self.speech_active:
            bubble = self.speech_bubble.scaled(
                int(self.width() * 0.95),
                int(self.height() * 0.45),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        
            # center horizontally
            bx = (self.width() - bubble.width()) // 2
        
            # move DOWN a bit more (important change)
            by = int(self.height() * 0.30) + int(bob * 0.2)
        
            painter.drawPixmap(bx, by, bubble)
        
            # -----------------------------
            # TEXT INSIDE BUBBLE
            # -----------------------------
        
            # white text with subtle shadow-like outline for readability
            painter.setPen(QPen(QColor(255, 255, 255)))
        
            text_rect = QRect(
                bx + int(bubble.width() * 0.1),
                by + int(bubble.height() * 0.25),  # move text DOWN inside bubble
                int(bubble.width() * 0.8),
                int(bubble.height() * 0.6)
            )
        
            painter.drawText(
                text_rect,
                Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                self.visible_text
            )
        painter.end()
    

    
    def check_window(self):
        name = get_active_window_name()
    
        if name == self.last_window:
            return
    
        self.last_window = name
    
        category = classify_window(name)
    
        if category == "browser":
            self.set_speech("Vivaldi browser opened")
    
        elif category == "pdf":
            self.set_speech("PDF file opened with Okular")
            
        elif category =="krita":
            self.set_speech("Drawing? Nice nice, I hope you're drawing me!")
    
        ##elif category == "unknown":
        ##    self.play_sound("baka-mitsuba.mp3")
        ##    self.set_speech("Procrastinating again? What a loser!")
            
    def set_speech(self, text: str):
        self.full_text = text
        self.visible_text = ""
        self.text_index = 0
        self.speech_active = True
    
        # restart typing cleanly
        self.type_timer.stop()
        self.type_timer.start(40)
    
        self.speech_timer.start(9000)
        
    def start_typing(self, text):
        self.full_text = text
        self.visible_text = ""
        self.text_index = 0
        self.speech_active = True
    
        self.type_timer.start(40)
        self.speech_timer.start(9000)
        
    import subprocess
    
    def play_sound(self, filename):
        subprocess.Popen([
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel", "quiet",
            "-volume", "200",
            f"assets/speech/{filename}"
        ])