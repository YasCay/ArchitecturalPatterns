"""
MVC Pattern: Smart Home Heizungssteuerung
Model-View-Controller Implementierung (Improved with Observer Pattern)
"""
import random
import time


class HeaterModel:
    """Model: Contains data AND business logic, notifies observers on changes"""
    def __init__(self, threshold=20.0):
        self.current_temp = 20.0
        self.is_heater_on = False
        self.threshold = threshold
        self._observers = []

    def attach(self, observer):
        """Observer Pattern: Register an observer (typically a View)"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Observer Pattern: Unregister an observer"""
        self._observers.remove(observer)

    def _notify(self):
        """Observer Pattern: Notify all observers of state changes"""
        for observer in self._observers:
            observer.update(self)

    def update_temperature(self, temp):
        """Update temperature and apply business logic"""
        self.current_temp = temp
        # Business logic: Model decides if heating is needed
        self.is_heater_on = self._should_heat(temp)
        # Notify observers once after all changes
        self._notify()

    def _should_heat(self, temperature):
        """Business Logic: Determine if heating should be on"""
        return temperature < self.threshold


class ConsoleView:
    """View: Observer that displays model state when notified"""
    def __init__(self):
        pass

    def update(self, model):
        """Observer Pattern: Called automatically when model changes"""
        heater_status = "AN" if model.is_heater_on else "AUS"
        print(f"Temp: {model.current_temp:.1f}°C -> Heizung: {heater_status}")

    def display(self, model):
        """Legacy method for manual display (kept for compatibility)"""
        self.update(model)


class TemperatureSensor:
    """Simuliert einen Temperatursensor"""
    def read_temperature(self):
        return round(random.uniform(17.0, 23.0), 1)


class HeaterController:
    """Controller: Thin controller that handles input and coordinates components"""
    def __init__(self, model, sensor):
        self.model = model
        self.sensor = sensor

    def run(self, iterations=5):
        """Main loop: Controller reads input and updates model (View updates automatically)"""
        print("=== MVC Pattern: Heizungssteuerung (Improved) ===\n")

        for i in range(iterations):
            # 1. Read sensor input
            temp = self.sensor.read_temperature()

            # 2. Update model (business logic in model, view notified automatically)
            self.model.update_temperature(temp)

            time.sleep(1)


def main():
    model = HeaterModel(threshold=20.0)
    view = ConsoleView()
    sensor = TemperatureSensor()

    model.attach(view)

    controller = HeaterController(model, sensor)

    controller.run(iterations=5)


if __name__ == "__main__":
    main()
