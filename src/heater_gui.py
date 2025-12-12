"""
Smart Home Architecture Showcase: MVC vs. EDA (Final Version)
Optimierte Visualisierung mit Sensor in beiden Diagrammen.
"""
import random
import math
import tkinter as tk
from tkinter import font

# ============= PHYSIK KERN (SimulationEnvironment) =============

class SimulationEnvironment:
    """
    Simuliert die Physik. Die Temperatur sinkt natürlich ab,
    wenn nicht geheizt wird.
    """
    def __init__(self):
        self.temperature = 21.0
        self.outside_temp = 5.0   # Kalt draußen
        self.insulation = 0.05    # Dämmung
        self.heater_power = 0.40  # Heizleistung

    def update(self, heater_is_on):
        # Physik: Wärmeverlust
        delta = (self.outside_temp - self.temperature) * self.insulation
        
        # Physik: Heizung
        if heater_is_on:
            delta += self.heater_power
            
        # Rauschen
        self.temperature += delta + random.uniform(-0.05, 0.05)
        return self.temperature

# ============= VISUALISIERUNG (GfxEngine) =============

class GfxEngine:
    @staticmethod
    def draw_thermometer(canvas, x, y, width, height, temp, target, is_active):
        """Zeichnet ein hübsches Thermometer."""
        canvas.delete("thermometer")
        
        # Skalierung (0 bis 40 Grad)
        min_t, max_t = 0, 40
        ratio = max(0, min(1, (temp - min_t) / (max_t - min_t)))
        
        # Farben
        glass = "#4a5568"
        bg_fill = "#2d3748"
        
        # Logik für Flüssigkeitsfarbe
        if is_active:
            fill_col = "#f56565" # Rot (Heizt)
        elif temp < target - 0.5:
            fill_col = "#4299e1" # Blau (Zu kalt)
        else:
            fill_col = "#48bb78" # Grün (Gut)

        # Maße
        bulb_r = width 
        stem_w = width * 0.6
        stem_x = x + (width - stem_w) / 2
        fill_h = (height - bulb_r) * ratio
        
        # Glas-Körper
        canvas.create_rectangle(stem_x, y, stem_x+stem_w, y+height-bulb_r/2, fill=bg_fill, outline=glass, width=2, tags="thermometer")
        canvas.create_oval(x, y+height-bulb_r, x+width, y+height, fill=bg_fill, outline=glass, width=2, tags="thermometer")
        
        # Füllung (Animiert durch ratio)
        fill_y = y + (height - bulb_r) - fill_h
        # Stiel-Füllung
        canvas.create_rectangle(stem_x+4, fill_y, stem_x+stem_w-4, y+height-bulb_r/2, fill=fill_col, outline="", tags="thermometer")
        # Kugel-Füllung
        canvas.create_oval(x+4, y+height-bulb_r+4, x+width-4, y+height-4, fill=fill_col, outline="", tags="thermometer")
        
        # Ziel-Linie
        target_ratio = max(0, min(1, (target - min_t) / (max_t - min_t)))
        ty = y + (height - bulb_r) * (1 - target_ratio)
        canvas.create_line(x-10, ty, x+width+10, ty, fill="#ecc94b", width=3, arrow=tk.LAST, tags="thermometer")
        canvas.create_text(x+width+15, ty, text=f"{target:.0f}°", fill="#ecc94b", font=("Arial", 9, "bold"), anchor="w", tags="thermometer")
        
        # Text-Wert unten
        canvas.create_text(x+width/2, y+height+20, text=f"{temp:.1f}°C", fill="white", font=("Arial", 11, "bold"), tags="thermometer")

    @staticmethod
    def draw_flame(canvas, x, y, is_on):
        """Zeichnet ein Heizungs-Icon (Flamme)."""
        tags = "flame"
        canvas.delete(tags)
        
        # Kreis Hintergrund
        outline = "#ecc94b" if is_on else "#4a5568"
        canvas.create_oval(x, y, x+60, y+60, outline=outline, width=3, tags=tags)
        
        if is_on:
            # Flamme (Polygon)
            # Simulierter Flicker-Effekt
            f = random.randint(-2, 2)
            points = [x+30, y+10+f, x+50, y+45, x+30, y+55, x+10, y+45]
            canvas.create_polygon(points, fill="#ed8936", outline="#f6e05e", width=2, smooth=True, tags=tags)
            canvas.create_text(x+30, y+75, text="HEIZUNG AN", fill="#ed8936", font=("Arial", 8, "bold"), tags=tags)
        else:
            canvas.create_text(x+30, y+30, text="OFF", fill="#4a5568", font=("Arial", 10, "bold"), tags=tags)

    @staticmethod
    def draw_sensor_chip(canvas, x, y):
        """Zeichnet ein Sensor-Icon."""
        tags = "chip"
        canvas.delete(tags)
        # Body
        canvas.create_rectangle(x, y, x+40, y+40, fill="#2b6cb0", outline="#bee3f8", width=2, tags=tags)
        canvas.create_text(x+20, y+20, text="SENS", fill="white", font=("Arial", 7, "bold"), tags=tags)
        # Pins
        for i in range(5, 40, 10):
            canvas.create_line(x-5, y+i, x, y+i, fill="#bee3f8", width=2, tags=tags)
            canvas.create_line(x+40, y+i, x+45, y+i, fill="#bee3f8", width=2, tags=tags)


# ============= ARCHITEKTUR DIAGRAMM =============

class ArchitectureDiagram:
    def __init__(self, canvas, mode="MVC"):
        self.canvas = canvas
        self.mode = mode
        self.arrows = {}
        self.nodes = {}
        self.draw_static()

    def draw_static(self):
        self.canvas.delete("all")
        
        if self.mode == "MVC":
            # Struktur: Sensor -> Controller -> Model -> View
            # Wir zeigen Sensor links oben, Controller mitte oben
            
            # Nodes
            self.draw_box(10, 20, "Sensor", "sens", "#2b6cb0")
            self.draw_box(110, 20, "Controller", "ctrl", "#805ad5")
            self.draw_box(50, 100, "Model", "model", "#2c5282")
            self.draw_box(170, 100, "View", "view", "#2f855a")
            
            # Arrows
            self.draw_arrow(10+80, 40, 110, 40, "s_to_c")      # Sens -> Ctrl
            self.draw_arrow(110+40, 60, 50+40, 100, "c_to_m")  # Ctrl -> Model
            self.draw_arrow(110+40, 60, 170+40, 100, "c_to_v") # Ctrl -> View (Update)
            self.draw_arrow(50+80, 120, 170, 120, "m_to_v", dashed=True) # Model -> View
            
        elif self.mode == "EDA":
            # Struktur: Sensor -> Mediator -> Heater
            self.draw_box(10, 60, "Sensor", "sens", "#d69e2e")
            self.draw_box(120, 60, "Mediator", "med", "#e53e3e")
            self.draw_box(230, 60, "Heater", "heat", "#d53f8c")
            
            # Arrows
            self.draw_arrow(10+80, 80, 120, 80, "s_to_m") # Event
            self.draw_arrow(120+80, 80, 230, 80, "m_to_h") # Command

    def draw_box(self, x, y, text, tag, color):
        # Schatten
        self.canvas.create_rectangle(x+3, y+3, x+80+3, y+40+3, fill="#000", outline="", tags=tag)
        # Box
        self.canvas.create_rectangle(x, y, x+80, y+40, fill=color, outline="white", width=1, tags=(tag, "box"))
        self.canvas.create_text(x+40, y+20, text=text, fill="white", font=("Arial", 9, "bold"), tags=tag)

    def draw_arrow(self, x1, y1, x2, y2, tag, dashed=False):
        dash = (2, 2) if dashed else None
        line = self.canvas.create_line(x1, y1, x2, y2, fill="#718096", width=2, arrow=tk.LAST, dash=dash, tags=tag)
        self.arrows[tag] = line

    def highlight_sequence(self, sequence):
        """Spielt die Animations-Schritte ab."""
        # Reset colors first
        self.draw_static()
        
        delay_per_step = 600 # ms
        
        for i, (tag, is_arrow) in enumerate(sequence):
            self.canvas.after(i * delay_per_step, lambda t=tag, a=is_arrow: self.glow(t, a))

    def glow(self, tag, is_arrow):
        color = "#f6e05e" # Gelb/Gold
        if is_arrow:
            self.canvas.itemconfig(self.arrows[tag], fill=color, width=4)
        else:
            # Box outline
            self.canvas.itemconfig(self.canvas.find_withtag(tag)[1], outline=color, width=3)


# ============= LOGIK (Muster Implementierung) =============

# --- MVC ---
class MvcModel:
    def __init__(self, env):
        self.env = env
        self.data_temp = 0.0
        self.data_heater = False
        self.target = 21.0

    def set_state(self, t, h):
        self.data_temp = t
        self.data_heater = h

class MvcController:
    def __init__(self, model, view_cb):
        self.model = model
        self.view_cb = view_cb # Die View ist hier abstrahiert als Callback
        
    def run_cycle(self):
        # 1. Input lesen (Sensor)
        current_temp = self.model.env.update(self.model.data_heater)
        
        # 2. Logik Entscheiden
        heater_on = self.model.data_heater
        if current_temp < self.model.target - 0.5:
            heater_on = True
        elif current_temp > self.model.target + 0.5:
            heater_on = False
            
        # 3. Model updaten
        self.model.set_state(current_temp, heater_on)
        
        # 4. View informieren
        self.view_cb(current_temp, self.model.target, heater_on)
        
        # Rückgabe der Animations-Schritte
        return [
            ("sens", False), ("s_to_c", True), # Sensor -> Controller
            ("ctrl", False), ("c_to_m", True), # Ctrl -> Model
            ("model", False), ("m_to_v", True), # Model -> View (Notify)
            ("view", False)
        ]

# --- EDA ---
class EdaSensor:
    def __init__(self, env):
        self.env = env
    
    def produce_event(self, heater_status):
        # Sensor liest nur physikalischen Wert
        temp = self.env.update(heater_status)
        return temp

class EdaMediator:
    def __init__(self):
        self.target = 21.0
    
    def handle_event(self, temp_event, current_heater_state):
        # Empfängt Event, prüft Regel
        command = None
        if temp_event < self.target - 0.5:
            command = True # Befehl: AN
        elif temp_event > self.target + 0.5:
            command = False # Befehl: AUS
        
        return command

class EdaSystem:
    """Wrapper für die EDA Komponenten"""
    def __init__(self, env, view_cb):
        self.sensor = EdaSensor(env)
        self.mediator = EdaMediator()
        self.heater_state = False
        self.view_cb = view_cb
        
    def run_cycle(self):
        # 1. Sensor feuert Event
        temp = self.sensor.produce_event(self.heater_state)
        
        # Animation Start
        seq = [("sens", False), ("s_to_m", True)]
        
        # 2. Mediator verarbeitet
        seq.append(("med", False))
        command = self.mediator.handle_event(temp, self.heater_state)
        
        # 3. Falls Command -> Heater reagiert
        if command is not None:
            # Nur wenn sich Status ändert oder explizit gesteuert wird
            if command != self.heater_state:
                seq.append(("m_to_h", True))
                seq.append(("heat", False))
            self.heater_state = command
            
        self.view_cb(temp, self.mediator.target, self.heater_state)
        return seq


# ============= MAIN APP (TKINTER) =============

class SmartHomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Architektur-Vergleich: MVC vs. EDA")
        self.geometry("1000x700")
        self.configure(bg="#1a202c")
        
        # 2 getrennte Umgebungen für fairen Vergleich
        self.env_mvc = SimulationEnvironment()
        self.env_eda = SimulationEnvironment()
        
        self.setup_ui()
        
        # Logik-Instanzen
        self.mvc = MvcController(MvcModel(self.env_mvc), self.update_mvc_ui)
        self.eda = EdaSystem(self.env_eda, self.update_eda_ui)
        
        # Loop starten
        self.running = True
        self.after(1000, self.game_loop)

    def setup_ui(self):
        # Header
        tk.Label(self, text="Smart Home Heating: Architecture Comparison", font=("Arial", 22, "bold"), bg="#1a202c", fg="white").pack(pady=20)
        
        # Main Grid
        grid = tk.Frame(self, bg="#1a202c")
        grid.pack(fill="both", expand=True, padx=20)
        
        # --- MVC Panel ---
        self.p_mvc = self.create_panel(grid, "MVC Architecture", "Der Controller steuert aktiv den Ablauf.", 0)
        self.dia_mvc = ArchitectureDiagram(self.p_mvc['canvas'], "MVC")
        
        # --- EDA Panel ---
        self.p_eda = self.create_panel(grid, "Event-Driven Architecture", "Komponenten reagieren lose auf Events.", 1)
        self.dia_eda = ArchitectureDiagram(self.p_eda['canvas'], "EDA")
        
        # Slider
        bg = "#2d3748"
        ct = tk.Frame(self, bg=bg, height=60)
        ct.pack(fill="x", side="bottom")
        tk.Label(ct, text="Ziel-Temperatur setzen:", bg=bg, fg="white", font=("Arial", 12)).pack(side="left", padx=20)
        self.slider = tk.Scale(ct, from_=10, to=30, orient="horizontal", bg=bg, fg="white", length=400, highlightthickness=0, command=self.on_slide)
        self.slider.set(21)
        self.slider.pack(side="left")

    def create_panel(self, parent, title, sub, col):
        frame = tk.Frame(parent, bg="#2d3748", bd=2, relief="flat")
        frame.grid(row=0, column=col, padx=15, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(frame, text=title, font=("Arial", 16, "bold"), bg="#2d3748", fg="#63b3ed").pack(pady=(15,5))
        tk.Label(frame, text=sub, font=("Arial", 10, "italic"), bg="#2d3748", fg="#cbd5e0").pack(pady=(0,15))
        
        # Oben: Diagramm
        cv_dia = tk.Canvas(frame, height=150, bg="#171923", highlightthickness=0)
        cv_dia.pack(fill="x", padx=10)
        
        # Unten: Visualisierung (Thermometer etc.)
        cv_vis = tk.Canvas(frame, height=250, bg="#2d3748", highlightthickness=0)
        cv_vis.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Status Text
        lbl = tk.Label(frame, text="...", font=("Courier", 10), bg="#171923", fg="#48bb78", height=2)
        lbl.pack(fill="x", padx=10, pady=(0,10))
        
        return {'canvas': cv_dia, 'vis': cv_vis, 'lbl': lbl}

    def update_mvc_ui(self, temp, target, heater):
        cv = self.p_mvc['vis']
        cv.delete("all")
        # Links Thermometer, Rechts Heizung, Links daneben Sensor-Chip (implizit)
        GfxEngine.draw_thermometer(cv, 60, 20, 40, 200, temp, target, heater)
        GfxEngine.draw_flame(cv, 250, 100, heater)
        
        txt = f"Status: {'HEIZEN' if heater else 'STANDBY'}  T: {temp:.1f}°C"
        self.p_mvc['lbl'].config(text=txt)

    def update_eda_ui(self, temp, target, heater):
        cv = self.p_eda['vis']
        cv.delete("all")
        
        # Sensor Icon explizit zeichnen
        GfxEngine.draw_sensor_chip(cv, 20, 100)
        
        # Thermometer
        GfxEngine.draw_thermometer(cv, 100, 20, 40, 200, temp, target, heater)
        
        # Heizung
        GfxEngine.draw_flame(cv, 250, 100, heater)
        
        txt = f"EVENT: TEMP_CHANGE -> CMD: {'ON' if heater else 'OFF'}"
        self.p_eda['lbl'].config(text=txt)

    def on_slide(self, val):
        v = float(val)
        self.mvc.model.target = v
        self.eda.mediator.target = v

    def game_loop(self):
        if not self.running: return
        
        # 1. Simulation Steps berechnen
        seq_mvc = self.mvc.run_cycle()
        seq_eda = self.eda.run_cycle()
        
        # 2. Animationen triggern
        self.dia_mvc.highlight_sequence(seq_mvc)
        self.dia_eda.highlight_sequence(seq_eda)
        
        # Loop Geschwindigkeit: 3.5 Sekunden
        self.after(3500, self.game_loop)

    def destroy(self):
        self.running = False
        super().destroy()

if __name__ == "__main__":
    app = SmartHomeApp()
    app.mainloop()