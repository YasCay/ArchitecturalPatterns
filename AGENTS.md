**Rolle:** Du bist ein Software-Architekt und erfahrener Entwickler.
**Aufgabe:** Erstelle zwei separate, minimale Konsolen-Anwendungen (CLI) für denselben Anwendungsfall ("Smart Home Heizungssteuerung"), um zwei verschiedene Architektur-Muster zu demonstrieren.
**Sprache:** Python
**Prinzipien:** Halte den Code extrem einfach (KISS). Keine externen Frameworks/Libraries. Fokus auf die Struktur der Muster.

---

#### 1. Der Anwendungsfall (Szenario)
Wir simulieren eine einfache Heizungssteuerung.
* Ein **Sensor** misst periodisch die Temperatur (simuliert durch Zufallswerte).
* Logik: Wenn die Temperatur unter 20.0 Grad fällt, muss die **Heizung** eingeschaltet werden. Sonst ist sie aus.
* Output: Der aktuelle Status soll auf der Konsole ausgegeben werden.

---

#### 2. Implementierung A: Model-View-Controller (MVC)
Bitte implementiere das Szenario streng nach dem MVC-Muster.
* **Model:** Hält die Daten (`currentTemp`, `isHeaterOn`). Enthält KEINE Logik darüber, wann geheizt wird, nur den Status.
* **View:** Eine Klasse `ConsoleView`, die nur Daten empfängt und formatiert ausgibt (z.B. "Temp: 19°C -> Heizung: AN").
* **Controller:**
    * Enthält die Hauptschleife (Main Loop).
    * Holt den Wert vom Sensor.
    * Entscheidet über die Geschäftslogik (Ist Temp < 20?).
    * Aktualisiert das Model.
    * Ruft die View zur Anzeige auf.
* **Ziel:** Zeige, wie der Controller den Ablauf aktiv steuert (hohe Kopplung der Ablaufsteuerung).

---

#### 3. Implementierung B: Event-Driven Architecture (Mediator Topology)
Bitte implementiere das Szenario als ereignisgesteuertes System.
* **Events:** Erstelle eine einfache Klasse/Struktur `TemperatureEvent` (enthält den Messwert).
* **Event Producer (Sensor):** Erzeugt Zufallswerte und "wirft" ein Event in einen Channel/Mediator. Der Sensor darf **nichts** von der Heizung wissen.
* **Event Mediator:**
    * Abonniert den Sensor.
    * Empfängt das Event.
    * Enthält die Regel (`if event.temp < 20`).
    * Löst bei Bedarf eine Aktion bei der Heizung aus (oder sendet ein Command-Event).
* **Event Consumer (Heater):** Reagiert nur auf Befehle/Events.
* **Ziel:** Zeige die Entkopplung. Der Sensor sendet nur "blind" Daten, der Mediator reagiert darauf.

---

#### 4. Analyse & Vergleich (für den Bericht)
Nach der Generierung des Codes, erstelle bitte eine kurze Gegenüberstellung basierend auf dem Code:
* **Coupling:** Wo ist die Kopplung stärker? (MVC Controller kennt meist alles vs. EDA Sensor kennt niemanden).
* **Erweiterbarkeit:** Was passiert, wenn wir eine "Klimaanlage" hinzufügen wollen? (Muss der MVC-Controller geändert werden? Muss der Sensor im EDA geändert werden?).
* **Komplexität:** Welcher Ansatz hat mehr "Overhead" für dieses simple Problem?