"""
Smart Home Heizungssteuerung - GUI Vergleich
Zwei Architekturen: MVC vs Event-Driven (Mediator)
"""
import random
import tkinter as tk


# ============= MVC PATTERN =============


class HeaterModel:
    """Model: hält nur Zustand, keine Logik."""

    def __init__(self, root=None):
        self.current_temp = 21.0
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
    """View: GUI für MVC Pattern."""

    def __init__(self, parent, model):
        self.model = model
        self.frame = tk.Frame(parent, bg="#0f1729", padx=16, pady=16)

        title = tk.Label(
            self.frame,
            text="MVC Pattern",
            font=("Helvetica", 16, "bold"),
            bg="#0f1729",
            fg="#f5f5f5",
        )
        title.pack(anchor="w")

        self.temp_canvas = tk.Canvas(
            self.frame, width=260, height=170, bg="#101a2f", highlightthickness=0
        )
        self.temp_canvas.pack(fill="x", pady=(12, 8))

        self.current_temp_label = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 12),
            bg="#0f1729",
            fg="#e0e0e0",
            justify="center",
        )
        self.current_temp_label.pack(pady=4)

        self.status_label = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 14, "bold"),
            bg="#0f1729",
            fg="#f5f5f5",
        )
        self.status_label.pack(pady=4)

        self.flow_label = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 10),
            bg="#0f1729",
            fg="#c8d1e0",
            wraplength=340,
            justify="left",
            anchor="w",
        )
        self.flow_label.pack(fill="x", pady=(8, 0), anchor="w")

        info = tk.Label(
            self.frame,
            text="Controller orchestriert Model und View",
            font=("Helvetica", 9, "italic"),
            bg="#0f1729",
            fg="#7f8ba0",
        )
        info.pack(anchor="w", pady=(10, 0))

    def display(self):
        self.draw_thermometer()
        self.current_temp_label.config(
            text=(
                f"Aktuelle Temperatur: {self.model.current_temp:.1f}°C\n"
                f"Ziel: {self.model.target_temp:.1f}°C"
            )
        )

        if self.model.is_heater_on:
            self.status_label.config(text="HEIZT", fg="#f15b5b")
        elif self.model.current_temp > self.model.target_temp:
            self.status_label.config(text="KÜHLT AB", fg="#55c1b5")
        else:
            self.status_label.config(text="OPTIMAL", fg="#9cd67b")

    def draw_thermometer(self):
        canvas = self.temp_canvas
        canvas.delete("all")

        canvas.create_rectangle(110, 20, 150, 140, fill="#182640", outline="#e0e0e0", width=2)
        canvas.create_oval(100, 130, 160, 160, fill="#182640", outline="#e0e0e0", width=2)

        temp_ratio = (self.model.current_temp - 15) / 15
        temp_ratio = max(0, min(1, temp_ratio))
        fill_height = 120 * temp_ratio
        fill_y = 140 - fill_height

        if self.model.is_heater_on:
            color = "#f57c6c"
        elif self.model.current_temp > self.model.target_temp:
            color = "#4fb7c1"
        else:
            color = "#87d37c"

        canvas.create_rectangle(110, fill_y, 150, 140, fill=color, outline="")
        canvas.create_oval(100, 130, 160, 160, fill=color, outline="")

        for temp in range(15, 31, 5):
            y = 140 - ((temp - 15) / 15) * 120
            canvas.create_line(90, y, 110, y, fill="#e0e0e0", width=1)
            canvas.create_text(75, y, text=f"{temp}°", fill="#e0e0e0", font=("Helvetica", 9))

        target_y = 140 - ((self.model.target_temp - 15) / 15) * 120
        canvas.create_line(90, target_y, 170, target_y, fill="#fbc02d", width=2, dash=(4, 3))
        canvas.create_text(190, target_y, text="Ziel", fill="#fbc02d", font=("Helvetica", 9, "bold"))

    def update_flow(self, text):
        self.flow_label.config(text=text)


class HeaterController:
    """Controller: enthält die Geschäftslogik"""

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.add_observer(self.on_model_changed)

    def on_model_changed(self):
        self.view.display()

    def step(self):
        """Simuliere Sensor-Messung und wende Business-Logik an."""
        temp_change = random.uniform(-0.25, 0.25)
        if self.model.is_heater_on:
            temp_change += 0.04  # <--- Geschwindigkeit beim Heizen (größer = schneller)
        else:
            temp_change -= 0.02   # <--- Geschwindigkeit beim Abkühlen (größer = schneller)

        new_temp = max(15, min(30, self.model.current_temp + temp_change))
        self.model.update_temperature(new_temp)

        action = "lässt Zustand unverändert"
        if new_temp < self.model.target_temp - 0.2:
            self.model.set_heater_state(True)
            action = "schaltet Heizung EIN"
        elif new_temp > self.model.target_temp + 0.2:
            self.model.set_heater_state(False)
            action = "schaltet Heizung AUS"

        heater_state = "EIN" if self.model.is_heater_on else "AUS"
        return (
            f"SENSOR: {new_temp:.1f}°C\n"
            f"CONTROLLER: {action}\n"
            f"MODEL: Heizung {heater_state} -> VIEW"
        )


# ============= EVENT-DRIVEN ARCHITECTURE =============


class TemperatureEvent:
    """Event: kapselt Temperaturmessung."""

    def __init__(self, temperature):
        self.temperature = temperature


class HeaterCommandEvent:
    """Command Event: Befehl an die Heizung."""

    def __init__(self, turn_on):
        self.turn_on = turn_on


class TemperatureSensor:
    """Event Producer: erzeugt Messwerte autonom."""

    def __init__(self):
        self.listeners = []
        self.current_temp = 21.0

    def subscribe(self, listener):
        self.listeners.append(listener)

    def measure_and_publish(self, heater_is_on):
        temp_change = random.uniform(-0.25, 0.25)
        if heater_is_on:
            temp_change += 0.04  # <--- Geschwindigkeit beim Heizen (größer = schneller)
        else:
            temp_change -= 0.02   # <--- Geschwindigkeit beim Abkühlen (größer = schneller)

        self.current_temp = max(15, min(30, self.current_temp + temp_change))
        event = TemperatureEvent(self.current_temp)

        actions = []
        for listener in self.listeners:
            actions.append(listener.on_temperature_event(event))
        return self.current_temp, actions


class EventMediator:
    """Mediator: enthält die Regel und schickt Commands."""

    def __init__(self):
        self.heater = None
        self.target_temp = 21.0
        self.current_temp = 21.0

    def register_heater(self, heater):
        self.heater = heater

    def set_target_temperature(self, temp):
        self.target_temp = temp

    def on_temperature_event(self, event):
        self.current_temp = event.temperature
        action = "behält Zustand"

        if self.heater:
            if event.temperature < self.target_temp - 0.2:
                self.heater.on_heater_command(HeaterCommandEvent(True))
                action = "sendet Command EIN"
            elif event.temperature > self.target_temp + 0.2:
                self.heater.on_heater_command(HeaterCommandEvent(False))
                action = "sendet Command AUS"
            else:
                self.heater.notify_observers()

        return action


class Heater:
    """Event Consumer: reagiert nur auf Commands."""

    def __init__(self, root=None):
        self.is_on = False
        self.observers = []
        self.root = root

    def add_observer(self, callback):
        self.observers.append(callback)

    def on_heater_command(self, command):
        self.is_on = command.turn_on
        self.notify_observers()

    def notify_observers(self):
        if self.root:
            for callback in self.observers:
                self.root.after(0, callback)
        else:
            for callback in self.observers:
                callback()


class EDAView:
    """View für Event-Driven Architecture."""

    def __init__(self, parent, mediator, heater, sensor):
        self.mediator = mediator
        self.heater = heater
        self.sensor = sensor
        self.frame = tk.Frame(parent, bg="#0f1729", padx=16, pady=16)

        title = tk.Label(
            self.frame,
            text="Event-Driven Architecture",
            font=("Helvetica", 16, "bold"),
            bg="#0f1729",
            fg="#f5f5f5",
        )
        title.pack(anchor="w")

        self.temp_canvas = tk.Canvas(
            self.frame, width=260, height=170, bg="#101a2f", highlightthickness=0
        )
        self.temp_canvas.pack(fill="x", pady=(12, 8))

        self.current_temp_label = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 12),
            bg="#0f1729",
            fg="#e0e0e0",
            justify="center",
        )
        self.current_temp_label.pack(pady=4)

        self.status_label = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 14, "bold"),
            bg="#0f1729",
            fg="#f5f5f5",
        )
        self.status_label.pack(pady=4)

        self.event_canvas = tk.Canvas(
            self.frame, width=260, height=70, bg="#101a2f", highlightthickness=0
        )
        self.event_canvas.pack(fill="x", pady=(8, 6))
        self.draw_event_flow()

        self.flow_label = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 10),
            bg="#0f1729",
            fg="#c8d1e0",
            wraplength=340,
            justify="left",
            anchor="w",
        )
        self.flow_label.pack(fill="x", pady=(8, 0), anchor="w")

        info = tk.Label(
            self.frame,
            text="Entkoppelt: Sensor → Mediator → Heater",
            font=("Helvetica", 9, "italic"),
            bg="#0f1729",
            fg="#7f8ba0",
        )
        info.pack(anchor="w", pady=(10, 0))

        self.heater.add_observer(self.display)

    def display(self):
        self.draw_thermometer()
        self.current_temp_label.config(
            text=(
                f"Aktuelle Temperatur: {self.mediator.current_temp:.1f}°C\n"
                f"Ziel: {self.mediator.target_temp:.1f}°C"
            )
        )

        if self.heater.is_on:
            self.status_label.config(text="HEIZT", fg="#f15b5b")
        elif self.mediator.current_temp > self.mediator.target_temp:
            self.status_label.config(text="KÜHLT AB", fg="#55c1b5")
        else:
            self.status_label.config(text="OPTIMAL", fg="#9cd67b")

    def draw_thermometer(self):
        canvas = self.temp_canvas
        canvas.delete("all")

        canvas.create_rectangle(110, 20, 150, 140, fill="#182640", outline="#e0e0e0", width=2)
        canvas.create_oval(100, 130, 160, 160, fill="#182640", outline="#e0e0e0", width=2)

        temp_ratio = (self.mediator.current_temp - 15) / 15
        temp_ratio = max(0, min(1, temp_ratio))
        fill_height = 120 * temp_ratio
        fill_y = 140 - fill_height

        if self.heater.is_on:
            color = "#f57c6c"
        elif self.mediator.current_temp > self.mediator.target_temp:
            color = "#4fb7c1"
        else:
            color = "#87d37c"

        canvas.create_rectangle(110, fill_y, 150, 140, fill=color, outline="")
        canvas.create_oval(100, 130, 160, 160, fill=color, outline="")

        for temp in range(15, 31, 5):
            y = 140 - ((temp - 15) / 15) * 120
            canvas.create_line(90, y, 110, y, fill="#e0e0e0", width=1)
            canvas.create_text(75, y, text=f"{temp}°", fill="#e0e0e0", font=("Helvetica", 9))

        target_y = 140 - ((self.mediator.target_temp - 15) / 15) * 120
        canvas.create_line(90, target_y, 170, target_y, fill="#fbc02d", width=2, dash=(4, 3))
        canvas.create_text(190, target_y, text="Ziel", fill="#fbc02d", font=("Helvetica", 9, "bold"))

    def draw_event_flow(self):
        canvas = self.event_canvas
        canvas.delete("all")

        canvas.create_oval(10, 20, 60, 60, fill="#4a90e2", outline="#e0e0e0", width=2)
        canvas.create_text(35, 40, text="Sensor", fill="#0f1729", font=("Helvetica", 9, "bold"))

        canvas.create_rectangle(105, 20, 155, 60, fill="#e94b3c", outline="#e0e0e0", width=2)
        canvas.create_text(130, 40, text="Mediator", fill="#0f1729", font=("Helvetica", 9, "bold"))

        canvas.create_oval(200, 20, 250, 60, fill="#f39c12", outline="#e0e0e0", width=2)
        canvas.create_text(225, 40, text="Heater", fill="#0f1729", font=("Helvetica", 9, "bold"))

        canvas.create_line(60, 40, 105, 40, fill="#e0e0e0", width=2, arrow=tk.LAST)
        canvas.create_line(155, 40, 200, 40, fill="#e0e0e0", width=2, arrow=tk.LAST)

    def update_flow(self, text):
        self.flow_label.config(text=text)


class EDAController:
    """Steuert den Event-Loop (hier getaktet über Tk)."""

    def __init__(self, sensor, mediator, view):
        self.sensor = sensor
        self.mediator = mediator
        self.view = view

    def step(self):
        sensor_value, actions = self.sensor.measure_and_publish(self.view.heater.is_on)
        action = actions[0] if actions else "kein Empfänger"
        heater_status = "EIN" if self.view.heater.is_on else "AUS"
        flow_text = (
            f"SENSOR EVENT: {sensor_value:.1f}°C\n"
            f"MEDIATOR: {action}\n"
            f"HEATER: {heater_status} -> VIEW"
        )
        self.view.display()
        return flow_text


# ============= MAIN GUI APPLICATION =============


class HeaterGUI:
    """Haupt-GUI Anwendung."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Home Heizungssteuerung - Architekturvergleich")
        self.root.configure(bg="#0b1220")
        self.root.columnconfigure(0, weight=1)

        header = tk.Label(
            self.root,
            text="Smart Home Heizungssteuerung",
            font=("Helvetica", 20, "bold"),
            bg="#0b1220",
            fg="#f5f5f5",
            pady=8,
        )
        header.pack()

        subheader = tk.Label(
            self.root,
            text="Links: MVC steuert den Ablauf. Rechts: Events binden Sensor und Heater lose zusammen.",
            font=("Helvetica", 10),
            bg="#0b1220",
            fg="#c8d1e0",
        )
        subheader.pack(pady=(0, 10))

        container = tk.Frame(self.root, bg="#0b1220")
        container.pack(fill="both", expand=True, padx=14, pady=8)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        mvc_model = HeaterModel(self.root)
        mvc_view = MVCView(container, mvc_model)
        mvc_view.frame.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        self.mvc_controller = HeaterController(mvc_model, mvc_view)

        sensor = TemperatureSensor()
        mediator = EventMediator()
        heater = Heater(self.root)
        sensor.subscribe(mediator)
        mediator.register_heater(heater)

        eda_view = EDAView(container, mediator, heater, sensor)
        eda_view.frame.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        self.eda_controller = EDAController(sensor, mediator, eda_view)

        control_frame = tk.Frame(self.root, bg="#0f1729", padx=16, pady=14)
        control_frame.pack(fill="x", padx=14, pady=12)

        control_title = tk.Label(
            control_frame,
            text="Gemeinsamer Zielwert",
            font=("Helvetica", 14, "bold"),
            bg="#0f1729",
            fg="#f5f5f5",
        )
        control_title.pack(anchor="w")

        self.target_temp = 21.0
        self.target_slider = tk.Scale(
            control_frame,
            from_=18,
            to=25,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self.on_target_change,
            length=600,
            label="Zieltemperatur (°C) – gilt für MVC und EDA",
            bg="#0f1729",
            fg="#f5f5f5",
            troughcolor="#0b1220",
            highlightthickness=0,
            bd=0,
            showvalue=False,
        )
        self.target_slider.set(self.target_temp)
        self.target_slider.pack(fill="x", pady=(10, 0))

        self.target_value_label = tk.Label(
            control_frame,
            text=f"Zieltemperatur: {self.target_temp:.1f}°C",
            font=("Helvetica", 10),
            bg="#0f1729",
            fg="#c8d1e0",
        )
        self.target_value_label.pack(anchor="w", pady=(4, 2))

        hint = tk.Label(
            control_frame,
            text=(
                "Der Sensor bewegt sich automatisch. Verändere den gemeinsamen Zielwert und beobachte,\n"
                "wie Controller bzw. Mediator reagieren und schneller heizen oder kühlen."
            ),
            font=("Helvetica", 9),
            bg="#0f1729",
            fg="#7f8ba0",
            justify="left",
        )
        hint.pack(anchor="w", pady=(4, 0))

        self.mvc_model = mvc_model
        self.mediator = mediator
        self.mvc_view = mvc_view
        self.eda_view = eda_view
        self.running = True
        self.tick_interval_ms = 450

        self.mvc_model.set_target_temperature(self.target_temp)
        self.mediator.set_target_temperature(self.target_temp)

        self.run_cycle()
        self.root.after(self.tick_interval_ms, self.loop)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def loop(self):
        if not self.running:
            return
        self.run_cycle()
        self.root.after(self.tick_interval_ms, self.loop)

    def run_cycle(self):
        mvc_flow = self.mvc_controller.step()
        eda_flow = self.eda_controller.step()
        self.mvc_view.update_flow(mvc_flow)
        self.eda_view.update_flow(eda_flow)

    def on_target_change(self, value):
        self.target_temp = float(value)
        self.target_value_label.config(text=f"Zieltemperatur: {self.target_temp:.1f}°C")
        self.mvc_model.set_target_temperature(self.target_temp)
        self.mediator.set_target_temperature(self.target_temp)
        self.run_cycle()

    def on_closing(self):
        self.running = False
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
    app = HeaterGUI()
    app.run()


if __name__ == "__main__":
    main()
