"""
Smart Home Heizungssteuerung - Animierte GUI Vergleich
MVC vs Event-Driven Architecture
"""
import tkinter as tk
from tkinter import ttk
import random
import threading
import time


# ============= MVC PATTERN =============

class HeaterModel:
    """Model: Hält die Daten"""
    def __init__(self, root=None):
        self.current_temp = 20.0
        self.target_temp = 21.0
        self.is_heater_on = False
        self.observers = []
        self.root = root

    def add_observer(self, callback):
        self.observers.append(callback)

    def update_temperature(self, temp):
        self.current_temp = temp
        self.notify_observers()

    def set_target_temperature(self, temp):
        self.target_temp = temp
        self.notify_observers()

    def set_heater_state(self, state):
        self.is_heater_on = state
        self.notify_observers()

    def notify_observers(self):
        if self.root:
            for callback in self.observers:
                self.root.after(0, callback)
        else:
            for callback in self.observers:
                callback()


class MVCView:
    """View: GUI für MVC Pattern"""
    def __init__(self, parent, model):
        self.model = model
        self.frame = tk.Frame(parent, bg="#1a1a2e", padx=20, pady=20)

        # Titel
        title = tk.Label(
            self.frame,
            text="MVC Pattern",
            font=("Arial", 18, "bold"),
            bg="#1a1a2e",
            fg="#eee"
        )
        title.pack(pady=(0, 20))

        # Temperatur Display
        self.temp_canvas = tk.Canvas(
            self.frame,
            width=300,
            height=200,
            bg="#16213e",
            highlightthickness=0
        )
        self.temp_canvas.pack(pady=10)

        # Aktueller Temperaturtext
        self.current_temp_label = tk.Label(
            self.frame,
            text="",
            font=("Arial", 14),
            bg="#1a1a2e",
            fg="#fff"
        )
        self.current_temp_label.pack(pady=5)

        # Status
        self.status_label = tk.Label(
            self.frame,
            text="",
            font=("Arial", 16, "bold"),
            bg="#1a1a2e",
            fg="#fff"
        )
        self.status_label.pack(pady=10)

        # Architektur Info
        info = tk.Label(
            self.frame,
            text="Controller orchestriert\nModel ↔ View",
            font=("Arial", 10, "italic"),
            bg="#1a1a2e",
            fg="#888",
            justify="center"
        )
        info.pack(pady=(20, 0))

    def display(self):
        """View aktualisieren"""
        # Thermometer zeichnen
        self.draw_thermometer()

        # Temperatur Text
        self.current_temp_label.config(
            text=f"Aktuelle Temperatur: {self.model.current_temp:.1f}°C\nZiel: {self.model.target_temp:.1f}°C"
        )

        # Status
        if self.model.is_heater_on:
            self.status_label.config(
                text="🔥 HEIZT",
                fg="#ff6b6b"
            )
        else:
            if self.model.current_temp > self.model.target_temp:
                self.status_label.config(
                    text="❄️ KÜHLT AB",
                    fg="#4ecdc4"
                )
            else:
                self.status_label.config(
                    text="✓ OPTIMAL",
                    fg="#95e1d3"
                )

    def draw_thermometer(self):
        """Animiertes Thermometer zeichnen"""
        canvas = self.temp_canvas
        canvas.delete("all")

        # Thermometer Hintergrund
        canvas.create_rectangle(120, 30, 180, 170, fill="#2d3561", outline="#fff", width=2)
        canvas.create_oval(110, 160, 190, 180, fill="#2d3561", outline="#fff", width=2)

        # Temperatur-Füllung (animiert)
        temp_ratio = (self.model.current_temp - 15) / (30 - 15)  # 15-30°C Skala
        temp_ratio = max(0, min(1, temp_ratio))

        fill_height = 130 * temp_ratio
        fill_y = 170 - fill_height

        # Farbe basierend auf Heiz/Kühl-Status
        if self.model.is_heater_on:
            # Heizen - Rot/Orange Gradient
            color = f"#{255:02x}{int(107 + (1-temp_ratio)*100):02x}{107:02x}"
        else:
            # Kühlen/Normal - Blau/Cyan Gradient
            color = f"#{int(78 + temp_ratio*100):02x}{int(205 - temp_ratio*100):02x}{196:02x}"

        canvas.create_rectangle(120, fill_y, 180, 170, fill=color, outline="")
        canvas.create_oval(110, 160, 190, 180, fill=color, outline="")

        # Skala
        for temp in range(15, 31, 5):
            y = 170 - ((temp - 15) / (30 - 15)) * 130
            canvas.create_line(100, y, 120, y, fill="#fff", width=1)
            canvas.create_text(85, y, text=f"{temp}°", fill="#fff", font=("Arial", 9))

        # Zieltemperatur Linie
        target_y = 170 - ((self.model.target_temp - 15) / (30 - 15)) * 130
        canvas.create_line(100, target_y, 200, target_y, fill="#ffd93d", width=2, dash=(5, 5))
        canvas.create_text(230, target_y, text="Ziel", fill="#ffd93d", font=("Arial", 10, "bold"))


class HeaterController:
    """Controller: Enthält die Geschäftslogik"""
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = False
        self.thread = None

        # Observer Pattern
        self.model.add_observer(self.on_model_changed)

    def on_model_changed(self):
        """Callback wenn Model sich ändert"""
        self.view.display()

    def start(self):
        """Controller starten"""
        self.running = True
        self.thread = threading.Thread(target=self.run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def run_loop(self):
        """Hauptschleife: Controller orchestriert alles"""
        while self.running:
            # 1. Temperatur simulieren (mit kleinen Änderungen)
            temp_change = random.uniform(-0.05, 0.05)

            # Wenn Heizung an ist, Temperatur erhöhen
            if self.model.is_heater_on:
                temp_change += 0.15
            else:
                # Natürliches Abkühlen zur Raumtemperatur
                if self.model.current_temp > 20:
                    temp_change -= 0.05

            new_temp = self.model.current_temp + temp_change
            new_temp = max(15, min(30, new_temp))  # Begrenzung

            # 2. Model aktualisieren
            self.model.update_temperature(new_temp)

            # 3. Geschäftslogik: Controller entscheidet
            if self.model.current_temp < self.model.target_temp - 0.5:
                self.model.set_heater_state(True)
            elif self.model.current_temp > self.model.target_temp + 0.5:
                self.model.set_heater_state(False)

            time.sleep(0.5)


# ============= EVENT-DRIVEN ARCHITECTURE =============

class TemperatureEvent:
    """Event: Kapselt Temperaturmessung"""
    def __init__(self, temperature):
        self.temperature = temperature


class HeaterCommandEvent:
    """Command Event: Befehl an die Heizung"""
    def __init__(self, turn_on):
        self.turn_on = turn_on


class TemperatureSensor:
    """Event Producer"""
    def __init__(self):
        self.listeners = []
        self.current_temp = 20.0

    def subscribe(self, listener):
        self.listeners.append(listener)

    def update_temperature(self, temp):
        """Externe Temperaturänderung"""
        self.current_temp = temp

    def measure_and_publish(self):
        """Sensor misst und sendet Event"""
        # Kleine Schwankung
        temp_change = random.uniform(-0.05, 0.05)
        self.current_temp += temp_change
        self.current_temp = max(15, min(30, self.current_temp))

        event = TemperatureEvent(self.current_temp)

        # Event an alle Listener senden
        for listener in self.listeners:
            listener.on_temperature_event(event)


class EventMediator:
    """Mediator: Enthält die Geschäftslogik"""
    def __init__(self):
        self.heater = None
        self.target_temp = 21.0
        self.current_temp = 20.0

    def register_heater(self, heater):
        self.heater = heater

    def set_target_temperature(self, temp):
        self.target_temp = temp

    def on_temperature_event(self, event):
        """Event Handler: Reagiert auf Temperatur-Events"""
        self.current_temp = event.temperature

        # Geschäftslogik im Mediator
        if event.temperature < self.target_temp - 0.5:
            command = HeaterCommandEvent(turn_on=True)
            self.heater.on_heater_command(command)
        elif event.temperature > self.target_temp + 0.5:
            command = HeaterCommandEvent(turn_on=False)
            self.heater.on_heater_command(command)


class Heater:
    """Event Consumer"""
    def __init__(self, root=None):
        self.is_on = False
        self.observers = []
        self.root = root

    def add_observer(self, callback):
        self.observers.append(callback)

    def on_heater_command(self, command):
        """Event Handler: Reagiert auf Commands"""
        old_state = self.is_on
        self.is_on = command.turn_on

        # Bei Statusänderung auch Temperatur beeinflussen
        if self.is_on != old_state:
            self.notify_observers()

    def notify_observers(self):
        if self.root:
            for callback in self.observers:
                self.root.after(0, callback)
        else:
            for callback in self.observers:
                callback()


class EDAView:
    """View für Event-Driven Architecture"""
    def __init__(self, parent, mediator, heater, sensor):
        self.mediator = mediator
        self.heater = heater
        self.sensor = sensor
        self.frame = tk.Frame(parent, bg="#1a1a2e", padx=20, pady=20)

        # Titel
        title = tk.Label(
            self.frame,
            text="Event-Driven Architecture",
            font=("Arial", 18, "bold"),
            bg="#1a1a2e",
            fg="#eee"
        )
        title.pack(pady=(0, 20))

        # Temperatur Display
        self.temp_canvas = tk.Canvas(
            self.frame,
            width=300,
            height=200,
            bg="#16213e",
            highlightthickness=0
        )
        self.temp_canvas.pack(pady=10)

        # Aktueller Temperaturtext
        self.current_temp_label = tk.Label(
            self.frame,
            text="",
            font=("Arial", 14),
            bg="#1a1a2e",
            fg="#fff"
        )
        self.current_temp_label.pack(pady=5)

        # Status
        self.status_label = tk.Label(
            self.frame,
            text="",
            font=("Arial", 16, "bold"),
            bg="#1a1a2e",
            fg="#fff"
        )
        self.status_label.pack(pady=10)

        # Event Flow Visualisierung
        self.event_canvas = tk.Canvas(
            self.frame,
            width=280,
            height=80,
            bg="#16213e",
            highlightthickness=0
        )
        self.event_canvas.pack(pady=10)
        self.draw_event_flow()

        # Architektur Info
        info = tk.Label(
            self.frame,
            text="Entkoppelt durch Events\nSensor → Mediator → Heater",
            font=("Arial", 10, "italic"),
            bg="#1a1a2e",
            fg="#888",
            justify="center"
        )
        info.pack(pady=(10, 0))

        # Observer registrieren
        self.heater.add_observer(self.display)

    def display(self):
        """View aktualisieren"""
        # Thermometer zeichnen
        self.draw_thermometer()

        # Temperatur Text
        self.current_temp_label.config(
            text=f"Aktuelle Temperatur: {self.mediator.current_temp:.1f}°C\nZiel: {self.mediator.target_temp:.1f}°C"
        )

        # Status
        if self.heater.is_on:
            self.status_label.config(
                text="🔥 HEIZT",
                fg="#ff6b6b"
            )
            self.animate_event_flow()
        else:
            if self.mediator.current_temp > self.mediator.target_temp:
                self.status_label.config(
                    text="❄️ KÜHLT AB",
                    fg="#4ecdc4"
                )
            else:
                self.status_label.config(
                    text="✓ OPTIMAL",
                    fg="#95e1d3"
                )

    def draw_thermometer(self):
        """Animiertes Thermometer zeichnen"""
        canvas = self.temp_canvas
        canvas.delete("all")

        # Thermometer Hintergrund
        canvas.create_rectangle(120, 30, 180, 170, fill="#2d3561", outline="#fff", width=2)
        canvas.create_oval(110, 160, 190, 180, fill="#2d3561", outline="#fff", width=2)

        # Temperatur-Füllung (animiert)
        temp_ratio = (self.mediator.current_temp - 15) / (30 - 15)
        temp_ratio = max(0, min(1, temp_ratio))

        fill_height = 130 * temp_ratio
        fill_y = 170 - fill_height

        # Farbe basierend auf Heiz/Kühl-Status
        if self.heater.is_on:
            color = f"#{255:02x}{int(107 + (1-temp_ratio)*100):02x}{107:02x}"
        else:
            color = f"#{int(78 + temp_ratio*100):02x}{int(205 - temp_ratio*100):02x}{196:02x}"

        canvas.create_rectangle(120, fill_y, 180, 170, fill=color, outline="")
        canvas.create_oval(110, 160, 190, 180, fill=color, outline="")

        # Skala
        for temp in range(15, 31, 5):
            y = 170 - ((temp - 15) / (30 - 15)) * 130
            canvas.create_line(100, y, 120, y, fill="#fff", width=1)
            canvas.create_text(85, y, text=f"{temp}°", fill="#fff", font=("Arial", 9))

        # Zieltemperatur Linie
        target_y = 170 - ((self.mediator.target_temp - 15) / (30 - 15)) * 130
        canvas.create_line(100, target_y, 200, target_y, fill="#ffd93d", width=2, dash=(5, 5))
        canvas.create_text(230, target_y, text="Ziel", fill="#ffd93d", font=("Arial", 10, "bold"))

    def draw_event_flow(self):
        """Event Flow Diagramm"""
        canvas = self.event_canvas
        canvas.delete("all")

        # Sensor
        canvas.create_oval(10, 25, 50, 65, fill="#4a90e2", outline="#fff", width=2)
        canvas.create_text(30, 45, text="📡", font=("Arial", 16))

        # Mediator
        canvas.create_rectangle(110, 25, 170, 65, fill="#e94b3c", outline="#fff", width=2)
        canvas.create_text(140, 45, text="⚙️", font=("Arial", 16))

        # Heater
        canvas.create_oval(230, 25, 270, 65, fill="#f39c12", outline="#fff", width=2)
        canvas.create_text(250, 45, text="🔥", font=("Arial", 16))

        # Pfeile
        canvas.create_line(50, 45, 110, 45, fill="#fff", width=2, arrow=tk.LAST)
        canvas.create_line(170, 45, 230, 45, fill="#fff", width=2, arrow=tk.LAST)

    def animate_event_flow(self):
        """Animierte Event-Pulse"""
        canvas = self.event_canvas

        # Pulse-Effekt auf den Verbindungen
        canvas.create_oval(75, 40, 85, 50, fill="#ffd93d", outline="", tags="pulse")
        canvas.create_oval(195, 40, 205, 50, fill="#ffd93d", outline="", tags="pulse")

        # Nach kurzer Zeit wieder entfernen
        canvas.after(300, lambda: canvas.delete("pulse"))


class EDAController:
    """Controller für Event-Driven System"""
    def __init__(self, sensor, mediator, view):
        self.sensor = sensor
        self.mediator = mediator
        self.view = view
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def run_loop(self):
        """Event Loop"""
        while self.running:
            # Temperatur mit Heizungseffekt anpassen
            if self.view.heater.is_on:
                self.sensor.current_temp += 0.15
            else:
                if self.sensor.current_temp > 20:
                    self.sensor.current_temp -= 0.05

            # Event publizieren
            self.sensor.measure_and_publish()
            self.view.display()

            time.sleep(0.5)


# ============= MAIN GUI APPLICATION =============

class HeaterGUI:
    """Haupt-GUI Anwendung"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Home Heizungssteuerung - Architekturvergleich")
        self.root.configure(bg="#0f0f1e")

        # Haupttitel
        title = tk.Label(
            self.root,
            text="🏠 Smart Home Heizungssteuerung",
            font=("Arial", 24, "bold"),
            bg="#0f0f1e",
            fg="#fff",
            pady=20
        )
        title.pack()

        # Container für beide Ansätze
        container = tk.Frame(self.root, bg="#0f0f1e")
        container.pack(padx=20, pady=10)

        # ===== MVC Setup =====
        mvc_model = HeaterModel(self.root)
        mvc_view = MVCView(container, mvc_model)
        mvc_view.frame.grid(row=0, column=0, padx=10)
        self.mvc_controller = HeaterController(mvc_model, mvc_view)

        # ===== EDA Setup =====
        sensor = TemperatureSensor()
        mediator = EventMediator()
        heater = Heater(self.root)

        sensor.subscribe(mediator)
        mediator.register_heater(heater)

        eda_view = EDAView(container, mediator, heater, sensor)
        eda_view.frame.grid(row=0, column=1, padx=10)
        self.eda_controller = EDAController(sensor, mediator, eda_view)

        # ===== Control Panel =====
        control_frame = tk.Frame(self.root, bg="#1a1a2e", padx=30, pady=20)
        control_frame.pack(pady=20, padx=20, fill="x")

        # Slider für Zieltemperatur
        slider_label = tk.Label(
            control_frame,
            text="🎯 Zieltemperatur einstellen:",
            font=("Arial", 14, "bold"),
            bg="#1a1a2e",
            fg="#fff"
        )
        slider_label.pack(pady=(0, 10))

        self.temp_slider = tk.Scale(
            control_frame,
            from_=15,
            to=30,
            resolution=0.5,
            orient=tk.HORIZONTAL,
            length=500,
            label="Temperatur (°C)",
            font=("Arial", 12),
            bg="#16213e",
            fg="#fff",
            troughcolor="#0f0f1e",
            activebackground="#4ecdc4",
            highlightthickness=0,
            command=self.on_temp_change
        )
        self.temp_slider.set(21.0)
        self.temp_slider.pack(pady=10)

        # Info Text
        info = tk.Label(
            control_frame,
            text="Bewege den Slider um die Zieltemperatur zu ändern.\n"
                 "Beobachte wie beide Architekturen unterschiedlich reagieren!",
            font=("Arial", 10, "italic"),
            bg="#1a1a2e",
            fg="#888",
            justify="center"
        )
        info.pack(pady=(10, 0))

        # Referenzen speichern
        self.mvc_model = mvc_model
        self.mediator = mediator

        # Controller starten
        self.mvc_controller.start()
        self.eda_controller.start()

        # Initiale Anzeige
        mvc_view.display()
        eda_view.display()

        # Cleanup beim Schließen
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_temp_change(self, value):
        """Callback wenn Slider bewegt wird"""
        temp = float(value)
        self.mvc_model.set_target_temperature(temp)
        self.mediator.set_target_temperature(temp)

    def on_closing(self):
        """Cleanup beim Schließen"""
        self.mvc_controller.stop()
        self.eda_controller.stop()
        self.root.destroy()

    def run(self):
        """GUI starten"""
        self.root.mainloop()


def main():
    app = HeaterGUI()
    app.run()


if __name__ == "__main__":
    main()
