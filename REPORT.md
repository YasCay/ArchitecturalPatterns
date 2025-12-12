# Architektur-Kurzbericht: Smart Home Heizungssteuerung

## I. Einleitung und Anwendungsfall-Definition

**1. Definition des Anwendungsfalls**
Der gewählte Anwendungsfall ist eine **Smart Home Heizungssteuerung**. Ein Temperatursensor misst periodisch die Raumtemperatur. Basierend auf einem definierten Zielwert entscheidet das System, ob eine Heizung ein- oder ausgeschaltet werden muss, um die Wohlfühltemperatur zu halten.

**2. Zielsetzung**
Das System muss folgende funktionale Anforderungen erfüllen:
* **Messen:** Periodische Simulation von Temperaturwerten inkl. Schwankungen.
* **Logik prüfen:** Vergleich des Ist-Werts mit einem Soll-Wert (z. B. 21°C) unter Berücksichtigung einer Hysterese (Puffer), um schnelles Ein-/Ausschalten zu vermeiden.
* **Aktion:** Senden von Steuerbefehlen (An/Aus) an das Heizungsaggregat.
* **Status ausgeben:** Visualisierung des aktuellen Zustands für den Benutzer.

**3. Muster-Auswahl**
Für die Implementierung wurden die folgenden zwei Architekturmuster gewählt:
* **Muster A: Model-View-Controller (MVC)**
* **Muster B: Event-Driven Architecture (EDA) mit Mediator-Topologie**

Diese Auswahl eignet sich hervorragend für einen Vergleich, da sie zwei fundamentale Ansätze gegenüberstellt: Die **aktive Orchestrierung** durch einen zentralen Controller (MVC) versus die **reaktive Verarbeitung** von Nachrichtenflüssen in einem entkoppelten System (EDA).

---

## II. Prototypische Implementierungen und Komponenten

### 1. Muster A: Model-View-Controller (MVC)
Im MVC-Ansatz ist die Struktur streng hierarchisch und zentral gesteuert.

* **Model (`HeaterModel`):**
    * **Rolle:** Hält den Datenzustand (`current_temp`, `is_heater_on`) und die Geschäftsdaten. Es enthält *keine* Steuerungslogik. Es informiert Beobachter (Observer) über Änderungen.
* **View (`MVCView`):**
    * **Rolle:** Ist für die Darstellung zuständig (Thermometer, Status-Label). Sie reagiert passiv auf Updates vom Model.
* **Controller (`HeaterController`):**
    * **Rolle:** Der "Chef" des Systems. Er triggert aktiv den Messvorgang (`step()`), enthält die gesamte Entscheidungslogik (`if new_temp < target...`) und manipuliert direkt das Model (`model.set_heater_state`). Er kennt sowohl Model als auch View.

### 2. Muster B: Event-Driven Architecture (EDA)
Im EDA-Ansatz (Mediator-Topologie) sind die Komponenten lose gekoppelt und kommunizieren über Nachrichten.

* **Event Producer (`TemperatureSensor`):**
    * **Rolle:** Erzeugt Temperaturdaten und publiziert diese als `TemperatureEvent`. Er weiß nicht, wer diese Daten empfängt (Fire-and-Forget).
* **Mediator (`EventMediator`):**
    * **Rolle:** Die "Spinne im Netz". Er abonniert den Sensor und empfängt die Events. Er beinhaltet die Regelwerke (Policies) und transformiert eingehende Events in ausgehende Befehle (`HeaterCommandEvent`), weiß aber nicht, wie die Heizung technisch funktioniert.
* **Event Consumer (`Heater`):**
    * **Rolle:** Ein passiver Empfänger, der nur auf Befehle reagiert (`on_heater_command`). Er kennt den Sensor nicht.

---

## III. Systematischer Vergleich (Pros & Cons)

| Kriterium | Muster A: MVC | Muster B: EDA (Mediator) |
| :--- | :--- | :--- |
| **Kopplung** | **Hoch (Eng):** Der Controller muss das Model und oft die View Schnittstellen genau kennen. Änderungen an der Model-API erfordern Änderungen am Controller. | **Niedrig (Lose):** Sensor und Heizung wissen nichts voneinander. Sie sind nur über das Event-Format (Contract) lose gekoppelt. Der Mediator entkoppelt die Logik von der Hardware. |
| **Erweiterbarkeit** | **Mittel:** Um eine Klimaanlage hinzuzufügen, muss der `HeaterController` umgeschrieben werden ("Open-Closed Principle" Verletzung). | **Hoch:** Eine Klimaanlage kann einfach als neuer Consumer hinzugefügt werden, der auf dasselbe `TemperatureEvent` hört oder vom Mediator angesteuert wird, ohne den Sensor zu ändern. |
| **Komplexität** | **Gering:** Der Ablauf ist linear und leicht lesbar ("Funktionsaufruf A folgt auf B"). Ideal für kleine Anwendungen. | **Höher:** Der Ablauf ist indirekt. Das Debugging ist schwerer, da man nicht immer sieht, wer ein Event ausgelöst hat ("Event-Hölle" Risiko bei großen Systemen). |
| **Testbarkeit** | **Mittel:** Unit-Tests für den Controller erfordern oft Mock-Objekte für Model und View. | **Hoch:** Der Mediator kann isoliert getestet werden, indem man ihm Events "zuwirft" und prüft, ob die richtigen Commands herauskommen. |

### Analytische Begründung
* **Kopplung:** Im MVC-Code (`heater_gui.py`) ruft der Controller direkt `self.model.update_temperature()` auf. Dies ist eine harte Abhängigkeit. Im EDA-Code (`eda_heater.py`) ruft der Sensor lediglich `listener.on_temperature_event(event)` auf; es ist ihm egal, ob ein Mediator oder ein Logger zuhört.
* **Overhead:** Für diesen minimalen Use-Case wirkt EDA wie "Overhead", da wir Event-Klassen und Listener-Listen definieren müssen, wo im MVC eine einfache Methode reicht. Dieser Overhead zahlt sich jedoch aus, sobald das System wächst (z. B. mehrere Sensoren).

---

## IV. Zusammenfassung und Empfehlungen

**1. Zusammenfassung**
Die Implementierung zeigt deutlich, dass **MVC** durch seine direkte Steuerungsstruktur einfacher zu verstehen und schneller umzusetzen ist, solange der Anwendungsbereich klein bleibt. **EDA** erfordert mehr initiale Boilerplate-Struktur (Events, Listener), bietet dafür aber eine exzellente Entkopplung, bei der Komponenten (wie der Sensor) komplett austauschbar sind, ohne die Geschäftslogik zu brechen.

**2. Empfehlung**
* Verwenden Sie **MVC**, wenn Sie eine in sich geschlossene Anwendung (z. B. eine Desktop-GUI oder einfache Web-App) bauen, bei der die Interaktion linear ist und der Fokus auf der schnellen Entwicklung liegt.
* Verwenden Sie **EDA**, wenn Sie ein verteiltes System (z. B. IoT, Microservices) planen, bei dem Sensoren und Aktoren unabhängig voneinander entwickelt, gewartet oder zur Laufzeit hinzugefügt werden sollen.
