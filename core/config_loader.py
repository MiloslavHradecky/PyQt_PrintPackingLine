from configparser import ConfigParser
from pathlib import Path


class ConfigLoader:
    def __init__(self, config_path: Path = Path(__file__).parent.parent / 'setup' / 'config.ini'):
        """
        Načte a zpracuje konfigurační soubor .ini pomocí Pathlib.

        :param config_path: Cesta ke konfiguračnímu souboru jako Path objekt.
        """
        if not config_path.exists():
            raise FileNotFoundError(f'Config file "{config_path}" not found.')

        self.config_path = config_path.resolve()
        self.config = ConfigParser()
        self.config.optionxform = str  # zachování velikosti písmen
        self.config.read(self.config_path)

    def get_path(self, key: str, fallback: str = None) -> Path | None:
        """
        Vrátí absolutní cestu ze sekce [Paths] jako Path objekt.

        :param key: Název klíče v sekci Paths
        :param fallback: Náhradní hodnota pokud není nalezena
        :return: Path objekt nebo None
        """
        raw = self.config.get('Paths', key, fallback=fallback)
        return Path(raw).resolve() if raw else None

    def get_trigger_values(self, section: str, trigger_name: str) -> list[str]:
        """
        Vrátí seznam hodnot pro daný trigger ze zadané sekce.

        :param section: Název sekce (např. ProductTriggerMapping)
        :param trigger_name: Název triggeru (např. C4-SMART)
        :return: Seznam hodnot
        """
        raw = self.config.get(section, trigger_name, fallback='')
        return [v.strip() for v in raw.split(',') if v.strip()]

    def get_all_triggers(self, section: str) -> dict[str, list[str]]:
        """
        Vrátí všechny triggery ze sekce jako slovník.

        :param section: Název sekce
        :return: Dict jako {trigger_name: [values]}
        """
        if section not in self.config:
            return {}

        return {
            name: [v.strip() for v in values.split(',') if v.strip()]
            for name, values in self.config[section].items()
        }

    def get_value(self, section: str, key: str, fallback: str = None) -> str | None:
        """
        Vrátí hodnotu ze zadané sekce a klíče.

        :param section: Název sekce
        :param key: Název klíče
        :param fallback: Náhradní hodnota
        :return: Hodnota jako řetězec
        """
        return self.config.get(section, key, fallback=fallback)
