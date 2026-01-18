import psutil
import numpy as np
from sklearn.ensemble import IsolationForest

class SystemEngine:
    """Silnik analityczny monitorujący zasoby, procesy oraz bezpieczeństwo sieciowe."""
    
    def __init__(self):
        # Model Isolation Forest do wykrywania statystycznych anomalii w danych
        self.model = IsolationForest(contamination=0.01)
        self.history = []
        self.is_safe = True
        self.known_ports = set()

    def get_live_metrics(self):
        """Pobiera aktualne statystyki obciążenia systemu i ruchu sieciowego."""
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        net = psutil.net_io_counters()
        
        sent_mb = net.bytes_sent / (1024 * 1024)
        recv_mb = net.bytes_recv / (1024 * 1024)
        
        return cpu, ram, disk, sent_mb, recv_mb

    def analyze(self, data_vector, current_ports):
        """Przeprowadza wielopoziomową analizę bezpieczeństwa (ML + Reguły + Porty)."""
        self.history.append(data_vector)
        active_ports = set(p['laddr'] for p in current_ports)
        is_critical = False
        reason = ""

        # Poziom 1: Detekcja nagłego otwarcia nowych portów nasłuchujących
        if self.known_ports:
            new_discovered = active_ports - self.known_ports
            if new_discovered:
                is_critical = True
                reason = f"Wykryto nowy port: {', '.join(new_discovered)}"
        
        self.known_ports = active_ports

        # Poziom 2: Analiza behawioralna ML (wymaga min. 50 próbek do nauki wzorca)
        ml_anomaly = False
        if len(self.history) >= 50:
            train_data = np.array(self.history[-100:])
            self.model.set_params(contamination=0.01) 
            preds = self.model.fit_predict(train_data)
            ml_anomaly = preds[-1] == -1

        # Poziom 3: Sztywne progi bezpieczeństwa
        cpu, ram, disk, sent, recv = data_vector
        if cpu > 90 or ram > 95:
            is_critical = True
            reason = "Krytyczne przeciążenie zasobów"
        
        # Detekcja podejrzenia eksfiltracji danych (wysoki upload + anomalia ML)
        if sent > 50 and ml_anomaly:
            is_critical = True
            reason = "Podejrzany transfer wychodzący"

        self.is_safe = not is_critical
        return self.is_safe, reason

    def get_processes(self):
        """Zwraca listę 15 procesów najbardziej obciążających procesor."""
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                if p.info['cpu_percent'] is not None and p.info['memory_info'] is not None:
                    mem_mb = p.info['memory_info'].rss / (1024 * 1024)
                    procs.append({
                        'pid': p.info['pid'],
                        'name': p.info['name'],
                        'cpu_percent': p.info['cpu_percent'],
                        'memory_mb': mem_mb
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)[:15]

    def get_open_ports(self):
        """Skanuje system w poszukiwaniu aktywnych portów w stanie LISTEN."""
        connections = []
        try:
            # Wymaga uprawnień administratora dla pełnych wyników
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'LISTEN':
                    try:
                        proc = psutil.Process(conn.pid)
                        connections.append({
                            'pid': conn.pid,
                            'name': proc.name(),
                            'laddr': f"{conn.laddr.ip}:{conn.laddr.port}"
                        })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
        except psutil.AccessDenied:
            return [{"pid": "!", "name": "Brak uprawnień ROOT", "laddr": "Sudo wymagane"}]
            
        return connections

    def kill_proc(self, pid):
        """Próbuje bezpiecznie zakończyć proces o danym numerze PID."""
        try:
            psutil.Process(pid).terminate()
            return True
        except Exception:
            return False