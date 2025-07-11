# 🔐 Utility module for decrypting user credentials via SZV.dat
# Pomocný modul pro dekódování přihlašovacích údajů ze souboru SZV.dat

import hashlib
import configparser
from core.logger import Logger
from pathlib import Path
from core.messenger import Messenger

# 🏷️ Global variable for prefix after login / Globální proměnná pro uložený prefix
value_prefix = None


def get_value_prefix():
    """
    Returns globally stored value_prefix.
    Vrací globálně uložený prefix pro další části aplikace.
    """
    return value_prefix


class SzvDecrypt:
    """
    Decryption and login verification via XOR and SHA-256.
    Třída zajišťující dekódování a ověření přihlášení.

    - Reads encrypted lines from SZV file
    - Decodes content using XOR
    - Verifies hashed credentials
    """

    def __init__(self, config_file: Path = Path(__file__).parent.parent / 'setup' / 'config.ini'):
        """
        Initializes decryption class and loads configuration.
        Inicializuje dekodér a načte cestu k šifrovanému souboru.
        """
        # 📌 Logger initialization / Inicializace loggerů
        self.normal_logger = Logger(spaced=False)  # ✅ Klasický logger
        self.spaced_logger = Logger(spaced=True)  # ✅ Logger s prázdným řádkem

        # 📌 Initializing messenger / Inicializace messengeru
        self.messenger = Messenger()

        config = configparser.ConfigParser()
        config.optionxform = str  # ✅ Preserve key casing / Zajistí zachování velikosti písmen
        config.read(config_file)

        if not config.sections():
            self.spaced_logger.log('Error', f'Config file nebyl nalezen: {config_file}', 'SZVUT001')
            self.messenger.show_error('Error', f'Config file nebyl nalezen: {config_file}', 'SZVUT001', True)

        self.szv_input_file = config.get('Paths', 'szv_input_file', fallback='T:/Prikazy/DataTPV/SZV.dat')

        # 📌 Decoded user info / Uchovávání dekódovaných hodnot
        self.value_surname = None
        self.value_name = None
        self.value_prefix = None

    def log_decoded_file(self):
        """
        Logs entire decrypted content from SZV file.
        Zaloguje dekódovaný obsah pro ladicí účely.
        """
        try:
            with Path(self.szv_input_file).open('r') as infile:
                for line in infile:
                    byte_array = bytearray.fromhex(line.strip())
                    decoded_line = self.decoding_line(byte_array)
                    self.normal_logger.clear_log('Info', f'Dekódovaný řádek: {decoded_line}')
        except Exception as e:
            self.normal_logger.log('Error', f'Při čtení souboru došlo k chybě: {str(e)}', 'SZVUT002')

    def decoding_line(self, encoded_data):
        """
        Decodes line using XOR bitwise transformation.
        Provádí dekódování jednoho řádku XOR transformací.

        :param encoded_data: Encrypted bytearray
        :return: List of decoded segments
        """
        try:
            int_xor = len(encoded_data) % 32
            decoded_data = bytearray(len(encoded_data))

            for i in range(len(encoded_data)):
                decoded_data[i] = encoded_data[i] ^ (int_xor ^ 0x6)
                int_xor = (int_xor + 5) % 32

            return decoded_data.decode('windows-1250').split('\x15')
        except Exception as e:
            self.normal_logger.log('Error', f'Dekódování selhalo: {e}', 'SZVUT003')
            self.messenger.show_error('Error', f'{e}', 'SZVUT003', True)
            return []

    def check_login(self, password):
        """
        Validates user password against decoded SHA-256 hashes.
        Ověří přihlášení uživatele podle hesla (ID karty).

        :param password: User-provided password string
        :return: True if login is valid, False otherwise
        """
        global value_prefix
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
                            value_prefix = self.value_prefix  # ❗ Global variable update / Aktualizace globální proměnné
                            self.spaced_logger.clear_log('Info', f'Logged: {self.value_surname} {self.value_name} {self.value_prefix}')
                            return True
                        else:
                            self.normal_logger.log('Warning', f'Řádek neobsahuje dostatek částí: {decoded_line[1]}', 'SZVUT004')
                            return False
                    else:
                        self.normal_logger.log('Warning', f'Řádek neobsahuje další části: {decoded_line}', 'SZVUT005')
                        return False

            self.spaced_logger.log('Warning', f'Zadané heslo ({password}) nebylo nalezeno v souboru ({self.szv_input_file}).', 'SZVUT006')

            return False

        except Exception as e:
            self.normal_logger.log('Error', f'Neočekávaná chyba při ověřování hesla: {str(e)}', 'SZVUT007')
            self.messenger.show_error('Error', f'{str(e)}', 'SZVUT007', True)
            return False

    def decoding_file(self):
        """
        Loads and decodes the encrypted SZV file.
        Načte a dekóduje obsah šifrovaného souboru.

        :return: List of [hash, decoded_string]
        """
        decoded_lines = []
        try:
            with Path(self.szv_input_file).open('r') as infile:
                for line in infile:
                    byte_array = bytearray.fromhex(line.strip())
                    decoded_line = self.decoding_line(byte_array)
                    if decoded_line and len(decoded_line) >= 1:
                        decoded_lines.append([hashlib.sha256(decoded_line[0].encode()).hexdigest(), ','.join(decoded_line)])
                    else:
                        self.normal_logger.log('Error', f'Přeskočen chybný dekódovaný řádek.', 'SZVUT008')
                        self.messenger.show_error('Error', f'Přeskočen chybný dekódovaný řádek.', 'SZVUT008', False)
        except Exception as e:
            self.normal_logger.log('Error', f'Při čtení souboru došlo k chybě: {str(e)}', 'SZVUT009')
            self.messenger.show_error('Error', f'{str(e)}', 'SZVUT009', True)
            return []

        return decoded_lines

    # ⚠️ Checklist file, leave a comment! / Kontrolní výpis souboru, nech zakomentováno!
    # def print_decoded_file(self):
    #     """
    #     Prints all decoded lines to console.
    #     Vytiskne všechny dekódované řádky do konzole (ladicí režim).
    #     """
    #     try:
    #         decoded_data = self.decoding_file()
    #         print('\n🟢 DEKÓDOVANÝ OBSAH SZV.dat:')
    #         for idx, decoded_line in enumerate(decoded_data, start=1):
    #             hash_val = decoded_line[0]
    #             decoded_text = decoded_line[1]
    #             print(f'🔹 [{idx}] {decoded_text}  ← (hash: {hash_val[:8]}...)')
    #     except Exception as e:
    #         print(f'[CHYBA] Nepodařilo se dekódovat soubor: {e}')

# 🧪 Dev-only: run this file to see decoded content / Pro ladění: spustit tento soubor samostatně k výpisu obsahu
# if __name__ == "__main__":
#     print("🛠️ Dekódování souboru SZV.dat...")
#     decryptor = SzvDecrypt()
#     decryptor.print_decoded_file()
