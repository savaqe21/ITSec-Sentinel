import sqlite3
from datetime import datetime, timedelta

class DbHandler:
    """Obsługuje trwałe przechowywanie logów zdarzeń i anomalii w bazie SQLite."""
    
    def __init__(self):
        # Inicjalizacja połączenia z bazą danych
        self.conn = sqlite3.connect("itsec_data.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        """Tworzy strukturę tabeli, jeśli jeszcze nie istnieje."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS anomalies 
            (id INTEGER PRIMARY KEY, date DATETIME, type TEXT, details TEXT)''')
        self.conn.commit()

    def log_anomaly(self, event_type, details):
        """Zapisuje nową anomalię i uruchamia automatyczne czyszczenie starej historii."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO anomalies (date, type, details) VALUES (?, ?, ?)", 
                           (now, event_type, details))
        self.conn.commit()
        self.cleanup()

    def cleanup(self):
        """Usuwa wpisy starsze niż 7 dni, aby zoptymalizować rozmiar bazy."""
        limit = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("DELETE FROM anomalies WHERE date < ?", (limit,))
        self.conn.commit()

    def fetch_history(self):
        """Pobiera wszystkie logi, sortując od najnowszych."""
        self.cursor.execute("SELECT * FROM anomalies ORDER BY id DESC")
        return self.cursor.fetchall()

    def clear_all_logs(self):
        """Całkowicie czyści historię zdarzeń na żądanie użytkownika."""
        self.cursor.execute("DELETE FROM anomalies")
        self.conn.commit()