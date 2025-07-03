import logging
import configparser
from pathlib import Path


class Logger:
    """
    Třída pro správu logování aplikace.
    Podporuje dvě metody logování:
    'log_with_code()' – zapisuje zprávu s 'error_code'
    'log_no_code()' – zapisuje zprávu bez 'error_code'
    """

    class IconFormatter(logging.Formatter):
        """Přizpůsobený formatter pro přidání ikon k úrovním logů."""
        ICONS = {
            'INFO': 'ℹ️ INFO   ',
            'WARNING': '⚠️ WARNING',
            'ERROR': '❌ ERROR  '  # ✅ Extra mezera pro zarovnání!
        }

        def format(self, record):
            max_width = 12  # ✅ Maximální šířka úrovní logu (pro zarovnání)
            record.levelname = self.ICONS.get(record.levelname, record.levelname)  # ✅ Přidání ikonky
            return super().format(record)

    def __init__(self, config_file='config.ini', spaced=False):
        """
        Inicializuje 'Logger' a nastaví parametry pro logování.

        :param config_file: Cesta ke konfiguračnímu souboru ('config.ini')
        :param spaced: Určuje, zda se před logem přidá prázdný řádek ('True'/'False')
        """
        self.spaced = spaced  # ✅ Určuje, zda přidáme prázdný řádek před logem

        # 📌 Načtení konfigurace
        config = configparser.ConfigParser()
        config.optionxform = str  # ✅ Zajistí zachování velikosti písmen
        config.read(config_file)

        # 📌 Načtení cesty k log souboru (převod relativní cesty na absolutní)
        self.log_file_path = Path(config.get('Paths', 'log_file_path')).resolve()

        # 📌 Vytvoření adresáře pro log soubor, pokud neexistuje
        self.log_path = self.log_file_path.parent
        self.log_path.mkdir(parents=True, exist_ok=True)

        # 📌 Nastavení základní konfigurace logování
        logging.basicConfig(
            filename=self.log_file_path,
            level=logging.INFO,  # ✅ Nastavení úrovně logování
            encoding='utf-8',
            format='%(asctime)s - %(levelname)s >>> %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 📌 Odstranění výpisu do konzole (pouze souborový log)
        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)

        # 📌 Aplikace vlastního formatteru na souborový log
        file_handler = logging.FileHandler(self.log_file_path, encoding='utf-8')
        file_handler.setFormatter(self.IconFormatter('%(asctime)s - %(levelname)s >>> %(message)s'))
        logging.getLogger().addHandler(file_handler)

    def log(self, level, message, error_code='GENERIC'):
        """
        Zapisuje log zprávu do souboru podle zvolené úrovně ('Info', 'Warning', 'Error').

        - Pokud je 'spaced=True', přidá se před logem prázdný řádek
        - Podporuje úrovně logování: 'Info', 'Warning', 'Error'
        - Každý log obsahuje unikátní ID chyby

        :param level: Úroveň logování ('Info', 'Warning', 'Error')
        :param message: Textová zpráva k zápisu do logu
        :param error_code: Unikátní ID chyby ('DB1001', 'NET2002', 'AUTH3003' apod.)
        """
        if self.spaced:
            with Path(self.log_file_path).open('a') as f:
                f.write('\n')  # ✅ Přidání prázdného řádku pokud je 'spaced=True'

        log_message = f'{message.ljust(50)} (ID: {error_code})'

        if level == 'Info':
            logging.info(log_message)
        elif level == 'Warning':
            logging.warning(log_message)
        elif level == 'Error':
            logging.error(log_message)

    def clear_log(self, level, message):

        if self.spaced:
            with Path(self.log_file_path).open('a') as f:
                f.write('\n')  # ✅ Přidání prázdného řádku pokud je 'spaced=True'

        log_message = message.ljust(50)

        if level == 'Info':
            logging.info(log_message)
        elif level == 'Warning':
            logging.warning(log_message)
        elif level == 'Error':
            logging.error(log_message)

# # 📌 Testování loggeru - Debug
# if __name__ == '__main__':
#     normal_logger = Logger(spaced=False)  # ✅ Klasický logger
#     normal_logger.log('Info', f'Aplikace byla spuštěna.', 'NET2002')
#     normal_logger.log('Warning', f'Aplikace byla opět spuštěna.', 'NET2005')
#     normal_logger.log('Error', f'Aplikace byla opět spuštěna.', 'ERR2007')
#
#     spaced_logger = Logger(spaced=True)  # ✅ Logger s prázdným řádkem
#     spaced_logger.log('Info', f'Toto je log s mezerou.')
#     spaced_logger.log('Error', f'Chyba: Něco se pokazilo!', 'AUTH3003')
