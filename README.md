# Architectural Patterns - Smart Home Heizungssteuerung

Dieses Projekt demonstriert zwei verschiedene Architektur-Muster anhand desselben Anwendungsfalls: einer einfachen Smart Home Heizungssteuerung.

## Anwendungsfall

Eine simulierte Heizungssteuerung mit folgender Logik:
- Ein Sensor misst periodisch die Temperatur (simuliert durch Zufallswerte zwischen 17°C und 23°C)
- Wenn die Temperatur unter 20°C fällt, wird die Heizung eingeschaltet
- Sonst bleibt die Heizung aus
- Der aktuelle Status wird auf der Konsole ausgegeben

## Implementierungen

### 1. Model-View-Controller (MVC)
**Datei:** [mvc_heater.py](mvc_heater.py)

Zeigt das klassische MVC-Pattern mit:
- **Model:** Hält nur Daten (`currentTemp`, `isHeaterOn`)
- **View:** Formatierte Ausgabe auf der Konsole
- **Controller:** Orchestriert den gesamten Ablauf und enthält die Geschäftslogik

**Ausführen:**
```bash
python mvc_heater.py
```

**Charakteristik:** Der Controller kennt alle Komponenten und steuert den Ablauf aktiv.

### 2. Event-Driven Architecture (EDA)
**Datei:** [eda_heater.py](eda_heater.py)

Zeigt ereignisgesteuerte Architektur mit Mediator Topology:
- **Event Producer (Sensor):** Erzeugt `TemperatureEvent`, kennt niemanden spezifisch
- **Event Mediator:** Empfängt Events, enthält Geschäftslogik, sendet Commands
- **Event Consumer (Heater):** Reagiert nur auf `HeaterCommandEvent`

**Ausführen:**
```bash
python eda_heater.py
```

**Charakteristik:** Lose gekoppelte Komponenten kommunizieren über Events.

## Detaillierter Vergleich

Eine ausführliche Analyse und Gegenüberstellung der beiden Ansätze findest du in [VERGLEICH.md](VERGLEICH.md).

Die Analyse behandelt:
- Coupling (Kopplung)
- Erweiterbarkeit
- Komplexität
- Testbarkeit
- Empfehlungen für den Einsatz

## Prinzipien

Beide Implementierungen folgen KISS (Keep It Simple, Stupid):
- Keine externen Frameworks oder Libraries
- Minimaler, fokussierter Code
- Klare Demonstration der Architektur-Muster
- Gut kommentiert

## Projektstruktur

```
ArchitecturalPatterns/
├── README.md              # Dieses Dokument
├── AGENTS.md              # Ursprüngliche Aufgabenstellung
├── VERGLEICH.md           # Detaillierte Analyse
├── mvc_heater.py          # MVC Implementierung
└── eda_heater.py          # Event-Driven Implementierung
```

## Anforderungen

- Python 3.6+
- Keine externen Dependencies

## Ausgabe

Beide Programme erzeugen ähnliche Ausgaben:

```
=== [Pattern Name]: Heizungssteuerung ===

Temp: 19.3°C -> Heizung: AN
Temp: 21.7°C -> Heizung: AUS
Temp: 18.2°C -> Heizung: AN
Temp: 22.1°C -> Heizung: AUS
Temp: 19.8°C -> Heizung: AN
```

## Lernziele

Dieses Projekt hilft zu verstehen:
1. Wie sich Architektur-Muster auf Code-Struktur auswirken
2. Trade-offs zwischen Einfachheit und Erweiterbarkeit
3. Unterschiede in Kopplung und Abhängigkeiten
4. Wann welches Pattern geeignet ist
