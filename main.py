import os
import sys
import ctypes
import customtkinter as ctk
from engine import SystemEngine
from translator import ProcessTranslator
from database import DbHandler
from charts import CircularChart, LiveChart

def is_admin():
    """Sprawdza, czy aplikacja posiada uprawnienia administratora/root."""
    try:
        if sys.platform == 'win32':
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.getuid() == 0
    except Exception:
        return False

class AdminApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ITSec Sentinel v4.0 - Final Edition")
        self.geometry("1100x850")
        ctk.set_appearance_mode("dark")

        # Inicjalizacja modułów logicznych
        self.engine = SystemEngine()
        self.trans = ProcessTranslator()
        self.db = DbHandler()

        # Budowa interfejsu (TabView)
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)
        self.tab1 = self.tabs.add("Monitoring")
        self.tab2 = self.tabs.add("Procesy")
        self.tab3 = self.tabs.add("Bezpieczeństwo")
        self.tab4 = self.tabs.add("Otwarte Porty")

        self.setup_monitoring()
        self.setup_processes()
        self.setup_security()
        self.setup_ports()
        
        # Start głównej pętli odświeżania danych
        self.loop()

    def setup_monitoring(self):
        """Konfiguracja zakładki z wykresami kołowymi i liniowymi."""
        self.mon_cont = ctk.CTkFrame(self.tab1, fg_color="transparent")
        self.mon_cont.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Wiersz górny: Wykresy kołowe (CPU, RAM, DYSK)
        self.top_row = ctk.CTkFrame(self.mon_cont, fg_color="transparent")
        self.top_row.pack(fill="x", pady=5)
        self.top_row.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.cpu_circ = CircularChart(self.top_row, "CPU", "#1f538d")
        self.cpu_circ.canvas_widget.grid(row=0, column=0, padx=5)
        
        self.ram_circ = CircularChart(self.top_row, "RAM", "#2fa572")
        self.ram_circ.canvas_widget.grid(row=0, column=1, padx=5)
        
        self.disk_circ = CircularChart(self.top_row, "DYSK", "#a58d2f")
        self.disk_circ.canvas_widget.grid(row=0, column=2, padx=5)

        # Wiersz dolny: Wykresy liniowe (Network)
        self.bot_row = ctk.CTkFrame(self.mon_cont, fg_color="transparent")
        self.bot_row.pack(fill="both", expand=True, pady=5)
        self.bot_row.grid_columnconfigure((0, 1), weight=1)
        
        self.down_chart = LiveChart(self.bot_row, "Pobieranie (MB)", "#1f8d8d")
        self.down_chart.canvas_widget.grid(row=0, column=0, padx=5, sticky="nsew")
        
        self.up_chart = LiveChart(self.bot_row, "Wysyłanie (MB)", "#a52f2f")
        self.up_chart.canvas_widget.grid(row=0, column=1, padx=5, sticky="nsew")

        # Panele informacyjne pod wykresami
        self.info_f = ctk.CTkFrame(self.tab1, fg_color="transparent", height=100)
        self.info_f.pack(fill="x", padx=15, pady=(5, 25)) 
        self.info_f.pack_propagate(False) 
        
        self.res_info = ctk.CTkLabel(self.info_f, text="", font=("Arial", 12), fg_color="#333333", corner_radius=8)
        self.res_info.pack(side="left", fill="both", expand=True, padx=5)
        
        self.net_info = ctk.CTkLabel(self.info_f, text="", font=("Arial", 12), fg_color="#333333", corner_radius=8)
        self.net_info.pack(side="left", fill="both", expand=True, padx=5)
        
    def setup_processes(self):
        """Konfiguracja listy aktywnych procesów."""
        self.proc_header = ctk.CTkLabel(self.tab2, text=f"{'PID':<10} | {'APLIKACJA':<30} | {'CPU':<10} | {'RAM':<10}", font=("Courier New", 12, "bold"))
        self.proc_header.pack(fill="x", padx=20, pady=10)
        
        self.proc_scroll = ctk.CTkScrollableFrame(self.tab2, fg_color="transparent")
        self.proc_scroll.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.ctrl = ctk.CTkFrame(self.tab2, fg_color="transparent")
        self.ctrl.pack(fill="x", padx=10, pady=5)
        
        self.pid_in = ctk.CTkEntry(self.ctrl, placeholder_text="Wpisz PID do zabicia")
        self.pid_in.pack(side="left", padx=5, expand=True, fill="x")
        
        self.kill_b = ctk.CTkButton(self.ctrl, text="ZAKOŃCZ PROCES", fg_color="#a52f2f", command=self.kill_action)
        self.kill_b.pack(side="left", padx=5)

    def setup_ports(self):
        """Konfiguracja widoku otwartych portów (Skaner sieciowy)."""
        self.port_header = ctk.CTkLabel(self.tab4, text=f"{'PID':<10} | {'PROCES':<25} | {'ADRES LOKALNY (PORT)':<25}", font=("Courier New", 12, "bold"))
        self.port_header.pack(fill="x", padx=20, pady=10)
        
        self.port_scroll = ctk.CTkScrollableFrame(self.tab4, fg_color="transparent")
        self.port_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_security(self):
        """Panel logowania anomalii i statusu ML."""
        self.status_b = ctk.CTkButton(self.tab3, text="STATUS: SYSTEM BEZPIECZNY", font=("Arial", 16, "bold"), height=50)
        self.status_b.pack(fill="x", padx=20, pady=10)
        
        self.sec_controls = ctk.CTkFrame(self.tab3, fg_color="transparent")
        self.sec_controls.pack(fill="x", padx=20, pady=5)
        
        self.clear_btn = ctk.CTkButton(self.sec_controls, text="🗑️ WYCZYŚĆ HISTORIĘ LOGÓW", fg_color="#a52f2f", command=self.clear_logs_action)
        self.clear_btn.pack(side="right", pady=5)
        
        self.hist_box = ctk.CTkTextbox(self.tab3, font=("Courier New", 12))
        self.hist_box.pack(fill="both", expand=True, padx=20, pady=10)

    def clear_logs_action(self):
        self.db.clear_all_logs()
        self.hist_box.delete("1.0", "end")

    def copy_pid(self, pid):
        self.clipboard_clear()
        self.clipboard_append(str(pid))

    def kill_action(self):
        try:
            pid = int(self.pid_in.get())
            if self.engine.kill_proc(pid): 
                self.pid_in.delete(0, 'end')
        except Exception: 
            pass

    def loop(self):
        """Główna pętla aplikacji odświeżana co 2000ms."""
        # 1. Pobieranie danych z silnika systemowego
        cpu, ram, disk, sent, recv = self.engine.get_live_metrics()
        ports = self.engine.get_open_ports()

        # 2. Aktualizacja wizualizacji i tekstów
        self.cpu_circ.update(cpu)
        self.ram_circ.update(ram)
        self.disk_circ.update(disk)
        self.down_chart.update(recv)
        self.up_chart.update(sent)
        
        self.res_info.configure(text=f"📊 ZASOBY SYSTEMOWE\nCPU: {cpu}% | RAM: {ram}%\nDYSK: {disk}%")
        self.net_info.configure(text=f"🌐 RUCH SIECIOWY\nPOBIERANIE: {recv:.2f} MB\nWYSYŁANIE: {sent:.2f} MB")

        # 3. Odświeżanie listy procesów (Top CPU)
        for w in self.proc_scroll.winfo_children(): w.destroy()
        procs = self.engine.get_processes()
        for p in procs:
            row = ctk.CTkFrame(self.proc_scroll, height=38, fg_color="#242424", corner_radius=6)
            row.pack(fill="x", pady=2, padx=5)
            row.pack_propagate(False)
            
            # Kolorowanie statystyk na podstawie obciążenia
            cpu_c = "#ff4d4d" if p['cpu_percent'] >= 80 else "#ffaf4d" if p['cpu_percent'] >= 50 else "#2fa572" if p['cpu_percent'] >= 20 else "#e0e0e0"
            ram_c = "#ff4d4d" if p['memory_mb'] >= 1024 else "#ffaf4d" if p['memory_mb'] >= 500 else "#2fa572" if p['memory_mb'] >= 100 else "#e0e0e0"

            name = self.trans.get_clean_name(p['name'])
            n_l = p['name'].lower()
            icon = "🤖" if any(x in n_l for x in ["gpt", "gemini", "perplexity", "claude", "ollama"]) else "⚙️"
            
            base = f" {icon} {name[:20]:<20} | {p['pid']:<7} | "
            ctk.CTkLabel(row, text=base, font=("Courier New", 12)).pack(side="left", padx=15)
            ctk.CTkLabel(row, text=f"CPU: {p['cpu_percent']:>4}%", font=("Courier New", 12, "bold"), text_color=cpu_c).pack(side="left")
            ctk.CTkLabel(row, text=f" | RAM: {p['memory_mb']:>6.0f} MB", font=("Courier New", 12, "bold"), text_color=ram_c).pack(side="left")
            ctk.CTkButton(row, text="Kopiuj", width=45, height=22, command=lambda x=p['pid']: self.copy_pid(x)).pack(side="right", padx=10)

        # 4. Odświeżanie skanera portów
        for w in self.port_scroll.winfo_children(): w.destroy()
        for prt in ports:
            row = ctk.CTkFrame(self.port_scroll, height=35, fg_color="#242424", corner_radius=6)
            row.pack(fill="x", pady=2, padx=5)
            row.pack_propagate(False)
            name = self.trans.get_clean_name(prt['name'])
            txt = f" {prt['pid']:<8} | {name[:20]:<20} | {prt['laddr']:<25}"
            ctk.CTkLabel(row, text=txt, font=("Courier New", 12)).pack(side="left", padx=15)
            ctk.CTkButton(row, text="IP:PORT", width=55, height=22, command=lambda x=prt['laddr']: self.copy_pid(x)).pack(side="right", padx=10)

        # 5. Silnik Analizy Anomalii (ML + Sieć)
        is_safe, reason = self.engine.analyze([cpu, ram, disk, sent, recv], ports)
        if not is_safe:
            self.status_b.configure(text=f"⚠️ ANOMALIA: {reason.upper()}", fg_color="#a52f2f")
            self.db.log_anomaly("Alert Bezpieczeństwa", reason)
        else:
            self.status_b.configure(text="✅ SYSTEM BEZPIECZNY", fg_color="#2fa572")

        # Aktualizacja logów historycznych w interfejsie
        self.hist_box.delete("1.0", "end")
        for h in self.db.fetch_history():
            self.hist_box.insert("end", f"[{h[1]}] {h[2]}: {h[3]}\n")

        # Planowanie kolejnego odczytu
        self.after(2000, self.loop)

if __name__ == "__main__":
    # Automatyczne podnoszenie uprawnień przy starcie
    if not is_admin():
        if sys.platform == 'win32':
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        else:
            os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
    else:
        app = AdminApp()
        app.mainloop()