"""
Event-Driven Architecture: Smart Home Heizungssteuerung
Mediator Topology - Zeigt Entkopplung durch Events
"""
import random
import time


class TemperatureEvent:
    """Event: Kapselt Temperaturmessung"""
    def __init__(self, temperature):
        self.temperature = temperature


class HeaterCommandEvent:
    """Command Event: Befehl an die Heizung"""
    def __init__(self, turn_on):
        self.turn_on = turn_on


class TemperatureSensor:
    """Event Producer: Erzeugt Temperature Events"""
    def __init__(self):
        self.listeners = []

    def subscribe(self, listener):
        """Listener können sich registrieren"""
        self.listeners.append(listener)

    def measure_and_publish(self):
        """Sensor misst und sendet Event - kennt niemanden spezifisch"""
        temperature = round(random.uniform(17.0, 23.0), 1)
        event = TemperatureEvent(temperature)

        # Event an alle Listener senden
        for listener in self.listeners:
            listener.on_temperature_event(event)


class EventMediator:
    """Mediator: Empfängt Events und enthält die Geschäftslogik"""
    def __init__(self):
        self.heater = None
        self.threshold = 20.0

    def register_heater(self, heater):
        """Heater registrieren"""
        self.heater = heater

    def on_temperature_event(self, event):
        """Event Handler: Reagiert auf Temperatur-Events"""
        print(f"Temp: {event.temperature:.1f}°C", end=" -> ")

        # Geschäftslogik im Mediator
        if event.temperature < self.threshold:
            command = HeaterCommandEvent(turn_on=True)
            self.heater.on_heater_command(command)
        else:
            command = HeaterCommandEvent(turn_on=False)
            self.heater.on_heater_command(command)


class Heater:
    """Event Consumer: Reagiert nur auf Commands"""
    def __init__(self):
        self.is_on = False

    def on_heater_command(self, command):
        """Event Handler: Reagiert auf Heater-Commands"""
        self.is_on = command.turn_on
        status = "AN" if self.is_on else "AUS"
        print(f"Heizung: {status}")


def main():
    """Hauptprogramm: Komponenten verbinden und starten"""
    print("=== Event-Driven Architecture: Heizungssteuerung ===\n")

    # Komponenten erstellen
    sensor = TemperatureSensor()
    mediator = EventMediator()
    heater = Heater()

    # Verkabelung: Sensor -> Mediator, Mediator -> Heater
    sensor.subscribe(mediator)
    mediator.register_heater(heater)

    # Event Loop: Sensor publiziert periodisch
    for i in range(5):
        sensor.measure_and_publish()
        time.sleep(1)


if __name__ == "__main__":
    main()
