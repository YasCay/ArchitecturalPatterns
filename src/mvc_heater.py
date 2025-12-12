"""
MVC Pattern: Smart Home Heizungssteuerung
Model-View-Controller Implementierung
"""
import random
import time


class HeaterModel:
    """Model: Hält nur die Daten, KEINE Logik"""
    def __init__(self):
        self.current_temp = 20.0
        self.is_heater_on = False

    def update_temperature(self, temp):
        self.current_temp = temp

    def set_heater_state(self, state):
        self.is_heater_on = state


class ConsoleView:
    """View: Nur für die Anzeige zuständig"""
    def display(self, model):
        heater_status = "AN" if model.is_heater_on else "AUS"
        print(f"Temp: {model.current_temp:.1f}°C -> Heizung: {heater_status}")


class TemperatureSensor:
    """Simuliert einen Temperatursensor"""
    def read_temperature(self):
        return round(random.uniform(17.0, 23.0), 1)


class HeaterController:
    """Controller: Steuert den gesamten Ablauf und enthält die Geschäftslogik"""
    def __init__(self, model, view, sensor):
        self.model = model
        self.view = view
        self.sensor = sensor
        self.threshold = 20.0

    def run(self, iterations=5):
        """Hauptschleife: Controller orchestriert alles"""
        print("=== MVC Pattern: Heizungssteuerung ===\n")

        for i in range(iterations):
            # 1. Sensor auslesen
            temp = self.sensor.read_temperature()

            # 2. Model aktualisieren
            self.model.update_temperature(temp)

            # 3. Geschäftslogik: Controller entscheidet
            if temp < self.threshold:
                self.model.set_heater_state(True)
            else:
                self.model.set_heater_state(False)

            # 4. View zur Anzeige aufrufen
            self.view.display(self.model)

            time.sleep(1)


def main():
    # Komponenten erstellen
    model = HeaterModel()
    view = ConsoleView()
    sensor = TemperatureSensor()
    controller = HeaterController(model, view, sensor)

    # Controller startet die Anwendung
    controller.run(iterations=5)


if __name__ == "__main__":
    main()
