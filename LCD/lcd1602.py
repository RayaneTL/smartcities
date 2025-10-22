# Fichier: lcd1602.py
# Bibliothèque pour piloter un écran LCD 16x2 via I2C en MicroPython

from machine import I2C, Pin
import utime

# Constantes de commandes LCD
LCD_CLEAR_DISPLAY = 0x01
LCD_RETURN_HOME = 0x02
LCD_ENTRY_MODE_SET = 0x04
LCD_DISPLAY_CONTROL = 0x08
LCD_FUNCTION_SET = 0x20
LCD_SET_DDRAM_ADDR = 0x80

# Constantes pour les modes
LCD_ENTRY_LEFT = 0x02
LCD_DISPLAY_ON = 0x04
LCD_2LINE = 0x08
LCD_4BIT_MODE = 0x00

# Constantes pour le backpack I2C (PCF8574)
MASK_RS = 0x01  # P0
MASK_RW = 0x02  # P1
MASK_E = 0x04   # P2
MASK_BACKLIGHT = 0x08 # P3
# D4-D7 sont sur P4-P7

class LCD1602:
    
    def __init__(self, i2c, num_rows, num_cols, i2c_addr=0x27):
        self.i2c = i2c
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.i2c_addr = i2c_addr
        self.backlight = MASK_BACKLIGHT # Backlight allumé par défaut
        
        # Initialisation en mode 4 bits
        utime.sleep_ms(50)
        self._write_nibble(LCD_FUNCTION_SET | 0x10) # 8-bit mode (pour init)
        utime.sleep_ms(5)
        self._write_nibble(LCD_FUNCTION_SET | 0x10) # 8-bit mode
        utime.sleep_ms(1)
        self._write_nibble(LCD_FUNCTION_SET | 0x10) # 8-bit mode
        
        self._write_nibble(LCD_FUNCTION_SET | LCD_4BIT_MODE) # 4-bit mode
        
        # Configuration finale
        self._write_command(LCD_FUNCTION_SET | LCD_4BIT_MODE | LCD_2LINE)
        self._write_command(LCD_ENTRY_MODE_SET | LCD_ENTRY_LEFT)
        self.clear()
        self.display()

    def _i2c_write(self, data):
        """Écrit une donnée sur le bus I2C"""
        self.i2c.writeto(self.i2c_addr, bytes([data | self.backlight]))

    def _write_nibble(self, data):
        """Écrit un quartet (4 bits) sur le bus I2C"""
        self._i2c_write(data & 0xF0)
        self._i2c_write((data & 0xF0) | MASK_E)
        self._i2c_write((data & 0xF0))

    def _write_command(self, cmd):
        """Envoie une commande complète (8 bits)"""
        # Envoie le quartet de poids fort
        self._i2c_write(cmd & 0xF0)
        self._i2c_write((cmd & 0xF0) | MASK_E)
        self._i2c_write(cmd & 0xF0)
        
        # Envoie le quartet de poids faible
        self._i2c_write((cmd << 4) & 0xF0)
        self._i2c_write(((cmd << 4) & 0xF0) | MASK_E)
        self._i2c_write((cmd << 4) & 0xF0)
        
        if cmd == LCD_CLEAR_DISPLAY or cmd == LCD_RETURN_HOME:
            utime.sleep_ms(2) # Ces commandes sont plus longues

    def _write_data(self, data):
        """Envoie une donnée (8 bits) pour affichage"""
        # Envoie le quartet de poids fort
        self._i2c_write((data & 0xF0) | MASK_RS)
        self._i2c_write(((data & 0xF0) | MASK_RS) | MASK_E)
        self._i2c_write((data & 0xF0) | MASK_RS)
        
        # Envoie le quartet de poids faible
        self._i2c_write(((data << 4) & 0xF0) | MASK_RS)
        self._i2c_write((((data << 4) & 0xF0) | MASK_RS) | MASK_E)
        self._i2c_write(((data << 4) & 0xF0) | MASK_RS)
        
    # --- Fonctions Publiques (utilisées dans Exercice 3) ---

    def display(self):
        """Allume l'affichage (correspond à la Leçon 9)"""
        self._write_command(LCD_DISPLAY_CONTROL | LCD_DISPLAY_ON)

    def no_display(self):
        """Éteint l'affichage (correspond à la Leçon 9)"""
        self._write_command(LCD_DISPLAY_CONTROL & ~LCD_DISPLAY_ON)
        
    def clear(self):
        """Efface l'écran (correspond à la Leçon 9)"""
        self._write_command(LCD_CLEAR_DISPLAY)

    def setCursor(self, col, row):
        """Place le curseur à une position (col, row) (correspond à la Leçon 9)"""
        row_offsets = [0x00, 0x40] # Adresses de début pour les lignes 0 et 1
        self._write_command(LCD_SET_DDRAM_ADDR | (col + row_offsets[row]))

    def print(self, text):
        """Affiche une chaîne de caractères (correspond à la Leçon 9)"""
        for char in text:
            self._write_data(ord(char))