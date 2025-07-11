# 📄 Logger – application logging system with icon-based formatting
# Modul pro správu logování aplikace s ikonami a podporou oddělení zpráv

import logging
import configparser
from pathlib import Path


class Logger:
    """
    Application logger with dual modes: with or without spacing.
    Logování aplikace s podporou volitelného prázdného řádku mezi logy.

    'log_with_code()' - writes message with 'error_code'
    'log_no_code()' - writes message without 'error_code'
    """

    class IconFormatter(logging.Formatter):
        """
        Custom formatter that adds icons to log levels.
        Vlastní formatter pro přidání ikony k úrovním logu.
        """
        ICONS = {
            'INFO': 'ℹ️ INFO   ',
            'WARNING': '⚠️ WARNING',
            'ERROR': '❌ ERROR  '
        }

        def format(self, record):
            max_width = 12  # ✅ Maximum width of log levels (for alignment) / Maximální šířka úrovní logu (pro zarovnání)
            record.levelname = self.ICONS.get(record.levelname, record.levelname)
            return super().format(record)

    def __init__(self, config_file: Path = Path('setup') / 'config.ini', spaced=False):
        """
        Initializes logging to a file, optionally with spacing.
        Inicializuje logování do souboru, případně s volitelným prázdným řádkem.

        :param config_file: Path to config file / Cesta ke konfiguračnímu souboru
        :param spaced: If True, adds empty lines between logs / Přidá prázdný řádek před logem
        """
        self.spaced = spaced  # ✅ Specifies whether to add a blank line before the log / Určuje, zda přidáme prázdný řádek před logem

        # 🔧 Load config / Načtení konfigurace
        config = configparser.ConfigParser()
        config.optionxform = str  # ✅ Ensures preservation of letter size / Zajistí zachování velikosti písmen
        config.read(config_file)

        # 📁 Resolve log file path from config / Získání logovací cesty z configu
        relative_log_path = config.get('Paths', 'log_file_path')
        self.log_file_path = Path(relative_log_path)
        self.log_file_path = self.log_file_path.resolve()
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)

        # 📌 Setting the basic logging configuration / Nastavení základní konfigurace logování
        logging.basicConfig(
            filename=self.log_file_path,
            level=logging.INFO,
            encoding='utf-8',
            format='%(asctime)s - %(levelname)s >>> %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 📌 Disable console output from default logging / Odstranění výpisu do konzole (pouze souborový log)
        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)

        # 📌 Apply icon-enhanced formatter to file output / Aplikace vlastního formatteru na souborový log
        file_handler = logging.FileHandler(self.log_file_path, encoding='utf-8')
        file_handler.setFormatter(self.IconFormatter('%(asctime)s - %(levelname)s >>> %(message)s'))
        logging.getLogger().addHandler(file_handler)

    def log(self, level, message, error_code='GENERIC'):
        """
        Logs a message with level and error code.
        Zapíše zprávu včetně úrovně a ID chyby.

        :param level: Log level (Info, Warning, Error)
        :param message: Text message to log
        :param error_code: Optional error ID to tag
        """
        if self.spaced:
            with Path(self.log_file_path).open('a', encoding='utf-8') as f:
                f.write('\n')  # ✅ Adding an empty row if 'spaced=True' / Přidání prázdného řádku pokud je 'spaced=True'

        log_message = f'{message.ljust(50)} (ID: {error_code})'

        if level == 'Info':
            logging.info(log_message)
        elif level == 'Warning':
            logging.warning(log_message)
        elif level == 'Error':
            logging.error(log_message)

    def clear_log(self, level, message):
        """
        Logs a message without error code (for clear/logical actions).
        Zapíše zprávu bez ID chyby (např. pro ladění nebo přehled).

        :param level: Log level
        :param message: Text to log
        """

        if self.spaced:
            with Path(self.log_file_path).open('a', encoding='utf-8') as f:
                f.write('\n')  # ✅ Adding an empty row if 'spaced=True' / Přidání prázdného řádku pokud je 'spaced=True'

        log_message = message.ljust(50)

        if level == 'Info':
            logging.info(log_message)
        elif level == 'Warning':
            logging.warning(log_message)
        elif level == 'Error':
            logging.error(log_message)

    def add_blank_line(self):
        """
        Inserts a single blank line into the log file.
        Vloží jeden prázdný řádek do logovacího souboru.
        """
        with Path(self.log_file_path).open('a', encoding='utf-8') as f:
            f.write('\n')

# # 📌 Logger Testing - Debug / Testování loggeru - Debug
# if __name__ == '__main__':
#     normal_logger = Logger(spaced=False)
#     normal_logger.log('Info', f'Aplikace byla spuštěna.', 'NET2002')
#     normal_logger.log('Warning', f'Aplikace byla opět spuštěna.', 'NET2005')
#     normal_logger.log('Error', f'Aplikace byla opět spuštěna.', 'ERR2007')
#
#     spaced_logger = Logger(spaced=True)
#     spaced_logger.log('Info', f'Toto je log s mezerou.')
#     spaced_logger.log('Error', f'Chyba: Něco se pokazilo!', 'AUTH3003')
