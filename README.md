# 🛡️ ITSec Sentinel v4.0 – Ssystem Security Dashboard

**ITSec Sentinel** to zaawansowane narzędzie do monitorowania parametrów systemowych i wykrywania anomalii w czasie rzeczywistym. Aplikacja łączy w sobie klasyczny monitoring zasobów z algorytmami uczenia maszynowego (ML) w celu identyfikacji podejrzanych zachowań sieciowych i procesowych.



## 🚀 Kluczowe Funkcje

* **📊 Monitoring Live**: Wizualizacja zużycia CPU, RAM i Dysku przy użyciu dynamicznych wykresów kołowych.
* **🌐 Analiza Ruchu Sieciowego**: Wykresy liniowe pobierania i wysyłania danych (MB/s).
* **🧠 Silnik Detekcji Anomalii**: Wykorzystanie modelu **Isolation Forest** (Scikit-Learn) do statystycznego wykrywania nietypowych skoków zużycia zasobów.
* **🔎 Skaner Portów**: Wykrywanie nowych połączeń w stanie `LISTEN` i natychmiastowe alarmowanie o potencjalnych zagrożeniach.
* **💀 Process Manager**: Możliwość podglądu 15 najbardziej obciążających procesów i ich natychmiastowego zakończenia (Kill).
* **📂 Historia Zdarzeń**: Trwały zapis anomalii w bazie **SQLite** z automatycznym czyszczeniem logów starszych niż 7 dni.

## 🛠️ Technologia

* **Język**: Python 3.10+
* **Interfejs**: CustomTkinter (Modern Dark UI)
* **Biblioteki**: 
    * `psutil` (dane systemowe)
    * `matplotlib` (wykresy)
    * `scikit-learn` (Machine Learning)
    * `sqlite3` (baza danych)

## 📦 Instalacja i Uruchomienie

### Sklonuj repozytorium
```bash
git clone [https://github.com/twoj-login/itsec-sentinel.git](https://github.com/twoj-login/itsec-sentinel.git)
cd itsec-sentinel
```
### Przygotuj środowisko wirtualne
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```
### Zainstaluj zależności
```bash
pip install -r requirements.txt
```
### Uruchom aplikacje
```bash
sudo main.py
```
