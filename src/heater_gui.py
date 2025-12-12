"""
Smart Home Architecture Showcase: MVC vs. EDA (Final Fix)
Feature: "Wanderlicht"-Animation und korrigierte EDA-Logik.
"""
import random
import tkinter as tk

# ============= PHYSIK KERN =============

class SimulationEnvironment:
    """Die physikalische Welt (identisch für beide)."""
    def __init__(self):
        self.temperature = 21.0
        self.outside_temp = 5.0
        self.insulation = 0.05
        self.heater_power = 0.40

    def update(self, heater_is_on):
        delta = (self.outside_temp - self.temperature) * self.insulation
        if heater_is_on:
            delta += self.heater_power
        self.temperature += delta + random.uniform(-0.05, 0.05)
        return self.temperature

# ============= GRAFIK ENGINE (Visuals) =============

class GfxEngine:
    @staticmethod
    def draw_thermometer(canvas, x, y, width, height, temp, target, is_active):
        canvas.delete("thermometer")
        min_t, max_t = 0, 40
        ratio = max(0, min(1, (temp - min_t) / (max_t - min_t)))
        
        glass, bg_fill = "#4a5568", "#2d3748"
        if is_active: fill_col = "#f56565" # Rot
        elif temp < target - 0.5: fill_col = "#4299e1" # Blau
        else: fill_col = "#48bb78" # Grün

        bulb_r = width 
        stem_w = width * 0.6
        stem_x = x + (width - stem_w) / 2
        fill_h = (height - bulb_r) * ratio
        
        # Glas
        canvas.create_rectangle(stem_x, y, stem_x+stem_w, y+height-bulb_r/2, fill=bg_fill, outline=glass, width=2, tags="thermometer")
        canvas.create_oval(x, y+height-bulb_r, x+width, y+height, fill=bg_fill, outline=glass, width=2, tags="thermometer")
        
        # Füllung
        fill_y = y + (height - bulb_r) - fill_h
        canvas.create_rectangle(stem_x+4, fill_y, stem_x+stem_w-4, y+height-bulb_r/2, fill=fill_col, outline="", tags="thermometer")
        canvas.create_oval(x+4, y+height-bulb_r+4, x+width-4, y+height-4, fill=fill_col, outline="", tags="thermometer")
        
        # Ziel
        tr = max(0, min(1, (target - min_t) / (max_t - min_t)))
        ty = y + (height - bulb_r) * (1 - tr)
        canvas.create_line(x-10, ty, x+width+10, ty, fill="#ecc94b", width=3, arrow=tk.LAST, tags="thermometer")
        
        canvas.create_text(x+width/2, y+height+20, text=f"{temp:.1f}°C", fill="white", font=("Arial", 11, "bold"), tags="thermometer")

    @staticmethod
    def draw_flame(canvas, x, y, is_on):
        canvas.delete("flame")
        outline = "#ecc94b" if is_on else "#4a5568"
        canvas.create_oval(x, y, x+60, y+60, outline=outline, width=3, tags="flame")
        
        if is_on:
            f = random.randint(-2, 2)
            points = [x+30, y+10+f, x+50, y+45, x+30, y+55, x+10, y+45]
            canvas.create_polygon(points, fill="#ed8936", outline="#f6e05e", width=2, smooth=True, tags="flame")
            canvas.create_text(x+30, y+75, text="ON", fill="#ed8936", font=("Arial", 8, "bold"), tags="flame")
        else:
            canvas.create_text(x+30, y+30, text="OFF", fill="#4a5568", font=("Arial", 10, "bold"), tags="flame")

    @staticmethod
    def draw_sensor_chip(canvas, x, y):
        canvas.delete("chip")
        canvas.create_rectangle(x, y, x+40, y+40, fill="#2b6cb0", outline="#bee3f8", width=2, tags="chip")
        canvas.create_text(x+20, y+20, text="SENS", fill="white", font=("Arial", 7, "bold"), tags="chip")
        for i in range(5, 40, 10):
            canvas.create_line(x-5, y+i, x, y+i, fill="#bee3f8", width=2, tags="chip")
            canvas.create_line(x+40, y+i, x+45, y+i, fill="#bee3f8", width=2, tags="chip")

# ============= DIAGRAMM LOGIK (Wanderlicht) =============

class ArchitectureDiagram:
    def __init__(self, canvas, mode="MVC"):
        self.canvas = canvas
        self.mode = mode
        self.elements = {}
        self.draw_static()

    def draw_static(self):
        self.canvas.delete("all")
        if self.mode == "MVC":
            # Nodes
            self.draw_node(10, 20, "Sensor", "sens", "#2b6cb0")
            self.draw_node(110, 20, "Controller", "ctrl", "#805ad5")
            self.draw_node(50, 100, "Model", "model", "#2c5282")
            self.draw_node(170, 100, "View", "view", "#2f855a")
            # Links
            self.draw_link(90, 40, 110, 40, "s_to_c")
            self.draw_link(150, 60, 90, 100, "c_to_m")
            self.draw_link(150, 60, 210, 100, "c_to_v")
            self.draw_link(130, 120, 170, 120, "m_to_v", dashed=True)
            
        elif self.mode == "EDA":
            self.draw_node(10, 60, "Sensor", "sens", "#d69e2e")
            self.draw_node(130, 60, "Mediator", "med", "#e53e3e")
            self.draw_node(250, 60, "Heater", "heat", "#d53f8c")
            # Links
            self.draw_link(90, 80, 130, 80, "s_to_m")
            self.draw_link(210, 80, 250, 80, "m_to_h")

    def draw_node(self, x, y, text, tag, color):
        self.canvas.create_rectangle(x+3, y+3, x+80+3, y+40+3, fill="#000", outline="", tags=tag)
        rect = self.canvas.create_rectangle(x, y, x+80, y+40, fill=color, outline="white", width=1, tags=(tag, f"{tag}_rect"))
        self.canvas.create_text(x+40, y+20, text=text, fill="white", font=("Arial", 9, "bold"), tags=tag)
        self.elements[tag] = (x, y, color, rect)

    def draw_link(self, x1, y1, x2, y2, tag, dashed=False):
        d = (2, 2) if dashed else None
        self.canvas.create_line(x1, y1, x2, y2, fill="#718096", width=2, arrow=tk.LAST, dash=d, tags=tag)

    def animate_sequence(self, sequence, step_duration=500):
        """Wanderlicht: Schaltet voriges Element aus, neues an."""
        self.draw_static() # Reset
        
        for i, (tag, is_arrow) in enumerate(sequence):
            # Lambda-Trick für Loop-Variablen
            self.canvas.after(i * step_duration, lambda t=tag, arr=is_arrow: self.light_up(t, arr))
            # Optional: Altes Element ausschalten (für striktes Wanderlicht)
            if i > 0:
                prev_tag, prev_arr = sequence[i-1]
                self.canvas.after(i * step_duration, lambda t=prev_tag, arr=prev_arr: self.light_down(t, arr))
        
        # Letztes Element ausschalten
        last_tag, last_arr = sequence[-1]
        self.canvas.after(len(sequence) * step_duration, lambda t=last_tag, arr=last_arr: self.light_down(t, arr))

    def light_up(self, tag, is_arrow):
        color = "#f6e05e" # Gold
        if is_arrow:
            self.canvas.itemconfig(tag, fill=color, width=4)
        else:
            items = self.canvas.find_withtag(f"{tag}_rect")
            if items:
                self.canvas.itemconfig(items[0], outline=color, width=4)

    def light_down(self, tag, is_arrow):
        if is_arrow:
            self.canvas.itemconfig(tag, fill="#718096", width=2)
        else:
            items = self.canvas.find_withtag(f"{tag}_rect")
            if items:
                self.canvas.itemconfig(items[0], outline="white", width=1)

# ============= LOGIK (MVC & EDA) =============

class MvcController:
    def __init__(self, env, view_cb):
        self.env = env
        self.view_cb = view_cb
        self.target = 21.0
        self.heater_on = False
        self.temp = 21.0
        
    def tick(self):
        # 1. Messen
        self.temp = self.env.update(self.heater_on)
        
        # 2. Logik
        if self.temp < self.target - 0.5: self.heater_on = True
        elif self.temp > self.target + 0.5: self.heater_on = False
        
        # 3. View Update
        self.view_cb(self.temp, self.target, self.heater_on)
        
        # Sequence: Sensor -> Ctrl -> Model(implizit) -> View
        # Wir zeigen: Sensor -> Ctrl -> Model -> View
        return [("sens", False), ("s_to_c", True), ("ctrl", False), 
                ("c_to_m", True), ("model", False), ("m_to_v", True), ("view", False)]

class EdaController:
    def __init__(self, env, view_cb):
        self.env = env
        self.view_cb = view_cb
        self.target = 21.0
        self.heater_on = False
        self.temp = 21.0
        
    def tick(self):
        # 1. Sensor misst
        self.temp = self.env.update(self.heater_on)
        
        # Sequence Start
        seq = [("sens", False), ("s_to_m", True), ("med", False)]
        
        # 2. Mediator entscheidet
        # FIX: Wir senden IMMER einen Command, wenn geheizt werden soll,
        # damit man den Fluss sieht (auch wenn der Status gleich bleibt).
        command_sent = False
        
        if self.temp < self.target - 0.5:
            # Command: Heizung an
            self.heater_on = True
            command_sent = True
        elif self.temp > self.target + 0.5:
            # Command: Heizung aus
            self.heater_on = False
            command_sent = True
        else:
            # Temperatur OK - Kein Command, aber wir halten den Status
            # Wenn Heizung an ist, müssen wir sie aktiv lassen.
            # Visualisierung: Wenn Heater an ist, zeigen wir den Fluss "Keep Alive"
            if self.heater_on:
                command_sent = True

        # 3. Pfad zum Heater nur, wenn Command/Aktivität da ist
        if command_sent:
            seq.append(("m_to_h", True))
            seq.append(("heat", False))
            
        self.view_cb(self.temp, self.target, self.heater_on)
        return seq

# ============= MAIN APP =============

class SmartHomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Architektur-Vergleich")
        self.geometry("950x700")
        self.configure(bg="#1a202c")
        
        self.env_mvc = SimulationEnvironment()
        self.env_eda = SimulationEnvironment()
        
        self.setup_ui()
        
        self.mvc = MvcController(self.env_mvc, self.update_mvc)
        self.eda = EdaController(self.env_eda, self.update_eda)
        
        self.running = True
        self.after(1000, self.loop)

    def setup_ui(self):
        tk.Label(self, text="Vergleich: MVC vs. Event-Driven", font=("Arial", 20, "bold"), bg="#1a202c", fg="white").pack(pady=15)
        
        grid = tk.Frame(self, bg="#1a202c")
        grid.pack(fill="both", expand=True, padx=20)
        
        # Panels
        self.p_mvc = self.create_panel(grid, "MVC (Eng gekoppelt)", 0)
        self.dia_mvc = ArchitectureDiagram(self.p_mvc['canvas'], "MVC")
        
        self.p_eda = self.create_panel(grid, "EDA (Lose gekoppelt)", 1)
        self.dia_eda = ArchitectureDiagram(self.p_eda['canvas'], "EDA")
        
        # Slider
        bg = "#2d3748"
        ct = tk.Frame(self, bg=bg, height=60)
        ct.pack(fill="x", side="bottom")
        tk.Label(ct, text="Ziel-Temperatur:", bg=bg, fg="white", font=("Arial", 12)).pack(side="left", padx=20)
        self.slider = tk.Scale(ct, from_=10, to=30, orient="horizontal", bg=bg, fg="white", length=300, command=self.on_slide)
        self.slider.set(21)
        self.slider.pack(side="left")

    def create_panel(self, parent, title, col):
        frame = tk.Frame(parent, bg="#2d3748", bd=2, relief="flat")
        frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(frame, text=title, font=("Arial", 14, "bold"), bg="#2d3748", fg="#63b3ed").pack(pady=10)
        
        cv_dia = tk.Canvas(frame, height=160, bg="#171923", highlightthickness=0)
        cv_dia.pack(fill="x", padx=10)
        
        cv_vis = tk.Canvas(frame, height=250, bg="#2d3748", highlightthickness=0)
        cv_vis.pack(fill="both", expand=True, padx=10, pady=10)
        
        lbl = tk.Label(frame, text="", font=("Courier", 10), bg="#171923", fg="#48bb78", height=2)
        lbl.pack(fill="x", padx=10, pady=10)
        
        return {'canvas': cv_dia, 'vis': cv_vis, 'lbl': lbl}

    def update_mvc(self, temp, target, on):
        GfxEngine.draw_thermometer(self.p_mvc['vis'], 60, 20, 40, 200, temp, target, on)
        GfxEngine.draw_flame(self.p_mvc['vis'], 250, 100, on)
        txt = "Status: HEIZEN" if on else "Status: STANDBY"
        self.p_mvc['lbl'].config(text=f"{txt} | T: {temp:.1f}")

    def update_eda(self, temp, target, on):
        GfxEngine.draw_sensor_chip(self.p_eda['vis'], 20, 100)
        GfxEngine.draw_thermometer(self.p_eda['vis'], 100, 20, 40, 200, temp, target, on)
        GfxEngine.draw_flame(self.p_eda['vis'], 250, 100, on)
        txt = "EVENT -> CMD: ON" if on else "EVENT -> CMD: OFF"
        if not on and temp > target - 0.5 and temp < target + 0.5: txt = "EVENT -> NO ACTION"
        self.p_eda['lbl'].config(text=txt)

    def on_slide(self, val):
        self.mvc.target = float(val)
        self.eda.target = float(val)

    def loop(self):
        if not self.running: return
        
        # 1. Berechnen
        s_mvc = self.mvc.tick()
        s_eda = self.eda.tick()
        
        # 2. Animieren (400ms pro Schritt)
        self.dia_mvc.animate_sequence(s_mvc, 400)
        self.dia_eda.animate_sequence(s_eda, 400)
        
        # Loop alle 4 Sek (damit Animation fertig wird)
        self.after(4000, self.loop)

    def destroy(self):
        self.running = False
        super().destroy()

if __name__ == "__main__":
    app = SmartHomeApp()
    app.mainloop()