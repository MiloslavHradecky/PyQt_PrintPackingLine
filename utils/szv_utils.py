import hashlib
import configparser
from core.logger import Logger
from pathlib import Path
from core.messenger import Messenger

# 📌 Globální proměnná uchovávající prefix hodnoty
value_prefix = None


def get_value_prefix():
    """
    Vrátí hodnotu 'value_prefix' bez použití 'global'.
    :return: Aktuální hodnota 'value_prefix'
    """
    return value_prefix


class SzvDecrypt:
    """
    Třída pro dekódování souboru a ověření přihlášení pomocí SHA-256 hashe.
    - Čte zakódovaný soubor obsahující přihlašovací údaje
    - Dekóduje obsah souboru pomocí XOR operace
    - Ověřuje uživatelské heslo proti uloženým hodnotám
    """

    def __init__(self, config_file: Path = Path(__file__).parent.parent / 'setup' / 'config.ini'):
        """
        Inicializuje třídu SzvDecrypt a nastaví cestu k vstupnímu souboru a loggeru.
        :param config_file: Cesta ke konfiguračnímu souboru ('config.ini').
        """
        # 📌 Inicializace loggerů
        self.normal_logger = Logger(spaced=False)  # ✅ Klasický logger
        self.spaced_logger = Logger(spaced=True)  # ✅ Logger s prázdným řádkem

        # 📌 Inicializace messengeru
        self.messenger = Messenger()  # ✅ Inicializujeme instanci 'Messenger' pro správu zpráv

        config = configparser.ConfigParser()
        config.optionxform = str  # ✅ Zajistí zachování velikosti písmen
        config.read(config_file)

        if not config.sections():
            self.spaced_logger.log('Error', f'Config file nebyl nalezen: {config_file}', 'MOD001')
            self.messenger.show_error('Error', f'Config file nebyl nalezen: {config_file}', 'MOD001', True)

        self.szv_input_file = config.get('Paths', 'szv_input_file', fallback='T:/Prikazy/DataTPV/SZV.dat')

        # 📌 Uchovávání dekódovaných hodnot
        self.value_surname = None
        self.value_name = None
        self.value_prefix = None

    def log_decoded_file(self):
        """
        Zaloguje dekódovaný obsah vstupního souboru, pokud existuje.
        """
        try:
            with Path(self.szv_input_file).open('r') as infile:
                for line in infile:
                    byte_array = bytearray.fromhex(line.strip())
                    decoded_line = self.decoding_line(byte_array)
                    self.normal_logger.clear_log('Info', f'Dekódovaný řádek: {decoded_line}')
        except Exception as e:
            self.normal_logger.log('Error', f'Při čtení souboru došlo k chybě: {str(e)}', 'MOD002')

    @staticmethod
    def decoding_line(encoded_data):
        """
        Dekóduje daná zakódovaná data XOR operací.
        :param encoded_data: Zakódovaná data jako 'bytearray'.
        :return: Dekódovaná data jako seznam stringů.
        """
        int_xor = len(encoded_data) % 32
        decoded_data = bytearray(len(encoded_data))

        for i in range(len(encoded_data)):
            decoded_data[i] = encoded_data[i] ^ (int_xor ^ 0x6)
            int_xor = (int_xor + 5) % 32

        return decoded_data.decode('windows-1250').split('\x15')

    def check_login(self, password):
        """
        Zkontroluje, zda zadané heslo odpovídá některému dekódovanému řádku ve vstupním souboru.
        :param password: Heslo k ověření.
        :return: 'True', pokud heslo odpovídá, jinak 'False'.
        """
        global value_prefix  # ✅ Umožňuje upravit globální proměnnou
        try:
            decoded_data = self.decoding_file()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            for decoded_line in decoded_data:
                if hashed_password == decoded_line[0]:
                    if len(decoded_line) > 1:
                        parts = decoded_line[1].split(',')
                        if len(parts) >= 4:
                            self.value_surname = parts[2].strip()
                            self.value_name = parts[3].strip()
                            self.value_prefix = parts[4].strip()
                            global value_prefix
                            value_prefix = self.value_prefix  # ✅ Aktualizace globální proměnné
                            self.spaced_logger.clear_log('Info', f'Logged: {self.value_surname} {self.value_name} {self.value_prefix}')
                            return True
                        else:
                            self.normal_logger.log('Warning', f'Řádek neobsahuje dostatek částí: {decoded_line[1]}', 'MOD003')
                            return False
                    else:
                        self.normal_logger.log('Warning', f'Řádek neobsahuje další části: {decoded_line}', 'MOD004')
                        return False

            self.spaced_logger.log('Warning', f'Zadané heslo ({password}) nebylo nalezeno v souboru ({self.szv_input_file}).', 'MOD005')

            return False

        except Exception as e:
            self.normal_logger.log('Error', f'Neočekávaná chyba při ověřování hesla: {str(e)}', 'MOD006')
            self.messenger.show_error('Error', f'{str(e)}', 'MOD006', True)
            return False

    def decoding_file(self):
        """
        Načte a dekóduje obsah vstupního souboru.
        :return: Seznam dekódovaných řádků, kde každý řádek je seznam obsahující hash hesla a dekódovaná data.
        """
        decoded_lines = []
        try:
            with Path(self.szv_input_file).open('r') as infile:
                for line in infile:
                    byte_array = bytearray.fromhex(line.strip())
                    decoded_line = self.decoding_line(byte_array)
                    decoded_lines.append([hashlib.sha256(decoded_line[0].encode()).hexdigest(), ','.join(decoded_line)])
        except Exception as e:
            self.normal_logger.log('Error', f'Při čtení souboru došlo k chybě: {str(e)}', 'MOD007')
            self.messenger.show_error('Error', f'{str(e)}', 'MOD007', True)
            return False
        finally:
            if 'infile' in locals():
                infile.close()  # ✅ Zajistí uzavření souboru

        return decoded_lines
