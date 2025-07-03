import configparser
from io import StringIO

config = configparser.ConfigParser()
config.optionxform = str  # Zachová původní velká písmena!

# Sekce Window pro title
config['Window'] = {
    'title': '2N IP Verso 2.0'
}

# Sekce Paths
config['Paths'] = {
    'reports_path': 'T:/reporty/',
    'output_file_path_product': 'C:/Users/Home/Documents/Coding/Python/PyQt/Etikety/02 product.txt',
    'output_file_path_c4_product': 'C:/Users/Home/Documents/Coding/Python/PyQt/Etikety/C4-SMART.txt',
    'output_file_path_my2n': 'C:/Users/Home/Documents/Coding/Python/PyQt/Etikety/my2n.txt',
    'szv_input_file': 'T:/Prikazy/DataTPV/SZV.dat',
    'log_file_path': 'log/app.log',
    'bartender_path': 'C:/Program Files (x86)/Seagull/BarTender Suite/bartend.exe',
    'tl_file_path': 'C:/Users/Home/Documents/Coding/Python/PyQt/Spoustece/TestLine.tl'
}

config['ProductTriggerMapping'] = {
    '68x20_80x30-Etikety2_01': '9155211C, 9155211CB',
    '68x20_80x30-Etikety2_02': '9155211, 9155211B',
    '68x20_80x30-Etikety2_C4': '9155211C-C4, 9155211CB-C4',
    '80x30-EtiketaBalic_VCCI': '0',
    'C4-SMART': '9155211C-C4, 9155211CB-C4',
    'savant_68x20_80x30': 'VSA-211C, VSA-211CB'
}

config['AxisTriggerMapping'] = {
    '80x30-EtiketaAxis': '9155211C, 9155211CB'
}

config['My2nTriggerMapping'] = {
    'SF_MY2N_A': '9155211, 9155211B, 9155211C, 9155211CB, 9155211CB B'
}

# Write configuration to StringIO for testing
configfile = StringIO()
config.write(configfile)

# Output StringIO contents to verify functionality
print(configfile.getvalue())

with open('config.ini', mode='w') as file:
    file.write(configfile.getvalue())
