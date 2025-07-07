# ⚙️ ConfigLoader – parses INI files into typed accessors using Pathlib
# Načítá hodnoty z .ini konfiguračního souboru jako cesty, seznamy nebo hodnoty

from configparser import ConfigParser
from pathlib import Path


class ConfigLoader:
    def __init__(self, config_path: Path = Path(__file__).parent.parent / 'setup' / 'config.ini'):
        """
        Initializes and loads the config file.
        Inicializuje a načte konfigurační soubor .ini pomocí Pathlib.

        :param config_path: Path to config file (default is ../setup/config.ini)
                           Cesta ke konfiguračnímu souboru
        """
        if not config_path.exists():
            raise FileNotFoundError(f'Config file "{config_path}" not found.')

        self.config_path = config_path.resolve()
        self.config = ConfigParser()
        self.config.optionxform = str  # 🟩 Preserve casing / zachování velikosti písmen
        self.config.read(self.config_path)

    def get_path(self, key: str, fallback: str = None, section: str = 'Paths') -> Path | None:
        """
        Returns a resolved Path from the specified section.
        Vrací absolutní cestu ze zadané sekce podle klíče.

        :param key: Key name / Název klíče
        :param fallback: Default value if key not found / Výchozí hodnota
        :param section: Name of section to search (default is "Paths") / Název sekce (výchozí je "Paths")
        :return: Resolved Path object or None
        """
        raw = self.config.get(section, key, fallback=fallback)
        return Path(raw).resolve() if raw else None

    def get_trigger_values(self, section: str, trigger_name: str) -> list[str]:
        """
        Returns list of values for a given trigger in the specified section.
        Vrací seznam hodnot pro konkrétní trigger v dané sekci.

        :param section: Section name / Název sekce (např. ProductTriggerMapping)
        :param trigger_name: Key name / Název triggeru (např. C4-SMART)
        :return: List of trimmed values / Seznam hodnot
        """
        raw = self.config.get(section, trigger_name, fallback='')
        return [v.strip() for v in raw.split(',') if v.strip()]

    def get_all_triggers(self, section: str) -> dict[str, list[str]]:
        """
        Returns all triggers from section as a dictionary.
        Vrací všechny triggery v dané sekci jako slovník.

        :param section: Section name / Název sekce
        :return: Dict of {trigger_name: [values]} / Slovník
        """
        if section not in self.config:
            return {}

        return {
            name: [v.strip() for v in values.split(',') if v.strip()]
            for name, values in self.config[section].items()
        }

    def get_value(self, section: str, key: str, fallback: str = None) -> str | None:
        """
        Returns a value from any section as string.
        Vrátí hodnotu z libovolné sekce jako řetězec.

        :param section: Section name / Název sekce
        :param key: Key name / Název klíče
        :param fallback: Default value / Náhradní hodnota
        :return: String or None
        """
        return self.config.get(section, key, fallback=fallback)
