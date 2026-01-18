class ProcessTranslator:
    """Klasa odpowiedzialna za mapowanie technicznych nazw procesów na czytelne nazwy użytkownika."""
    
    def __init__(self):
        # Słownik mapowania: klucz (fragment nazwy systemowej) -> czytelna etykieta
        self.mapping = {
            # --- AI & LLM Tools ---
            "ollama": "Ollama (Lokalne AI)",
            "lm studio": "LM Studio (LLM)",
            "chatgpt": "ChatGPT Desktop",
            "claude": "Claude AI App",
            "perplexity": "Perplexity AI",
            "gemini": "Google Gemini App",
            "diffusion": "Stable Diffusion UI",
            
            # --- Biuro i Produktywność ---
            "word": "MS Word",
            "winword": "MS Word",
            "excel": "MS Excel",
            "powerpnt": "MS PowerPoint",
            "powerpoint": "MS PowerPoint",
            "outlook": "MS Outlook (Poczta)",
            "onenote": "MS OneNote",
            "teams": "Microsoft Teams",
            
            # --- Komunikacja ---
            "discord": "Discord",
            "whatsapp": "WhatsApp Desktop",
            "messenger": "FB Messenger",
            "slack": "Komunikator Slack",
            "telegram": "Telegram Desktop",
            "thunderbird": "Klient Poczty Thunderbird",
            "mail": "Apple Mail",
            "spark": "Spark Email",
            
            # --- System operacyjny ---
            "kernel_task": "Jądro Systemu (Kernel)",
            "windowserver": "Interfejs Systemu",
            "mdworker": "Indeksowanie Spotlight",
            "finder": "Finder",
            "explorer.exe": "Eksplorator Plików",
            
            # --- Narzędzia Deweloperskie ---
            "code": "Visual Studio Code",
            "iterm2": "Terminal iTerm2",
            "terminal": "Terminal Systemowy",
            "python": "Dashboard Sentinel (Python)",
            "docker": "Kontenery Docker",
            "git": "System Git"
        }

    def get_clean_name(self, raw_name):
        """
        Przekształca surową nazwę procesu na czytelną formę.
        Zwraca oryginalną nazwę, jeśli nie znaleziono dopasowania.
        """
        name_lower = raw_name.lower()
        
        # Inteligentne dopasowanie: sprawdza czy klucz ze słownika występuje w nazwie procesu
        for key, friendly_name in self.mapping.items():
            if key in name_lower:
                return friendly_name
                
        return raw_name