# Fichier: dht20.py
# Bibliothèque pour lire le capteur de température et humidité DHT20 (I2C)
# VERSION CORRIGÉE pour le TypeError

import machine
import utime

# Adresse I2C par défaut du DHT20
DHT20_I2C_ADDR = 0x38

# Commandes
CMD_TRIGGER_MEASURE = [0xAC, 0x33, 0x00]
CMD_SOFT_RESET = [0xBA]
STATUS_BUSY = 0x80
STATUS_CALIBRATED = 0x08

class DHT20:
    def __init__(self, i2c_bus, addr=DHT20_I2C_ADDR):
        self.i2c = i2c_bus
        self.addr = addr
        self.buf = bytearray(7)
        self.init()

    def _read_status(self):
        """Lit l'octet de statut"""
        try:
            # CORRECTION: Lit 1 octet dans le buffer
            self.i2c.readfrom_into(self.addr, self.buf, 1) 
            return self.buf[0]
        except OSError as e:
            print(f"Erreur I2C (read_status): {e}")
            return 0

    def _send_command(self, cmd_bytes):
        """Envoie une commande au capteur"""
        try:
            self.i2c.writeto(self.addr, bytes(cmd_bytes))
        except OSError as e:
            # Cette erreur (EIO) signifie que l'adresse I2C est fausse ou le capteur est débranché
            print(f"Erreur I2C (send_command): {e}")

    def init(self):
        """Initialise le capteur ou effectue un soft reset"""
        utime.sleep_ms(100)
        self._send_command(CMD_SOFT_RESET)
        utime.sleep_ms(100)
        
        status = self._read_status()
        if (status & STATUS_CALIBRATED) == 0:
            print("DHT20 non calibré. Vérifiez la connexion ou l'adresse I2C.")
            
    def _trigger_measurement(self):
        """Demande au capteur de prendre une nouvelle mesure"""
        self._send_command(CMD_TRIGGER_MEASURE)

    def _read_raw_data(self):
        """Lit les 7 octets de données (statut + 6 data)"""
        try:
            # CORRECTION: Lit 7 octets dans le buffer
            self.i2c.readfrom_into(self.addr, self.buf, 7) 
        except OSError as e:
            print(f"Erreur I2C (read_raw_data): {e}")
            return False
        return True

    def _is_busy(self):
        """Vérifie si le capteur est en train de mesurer"""
        return (self._read_status() & STATUS_BUSY) == STATUS_BUSY

    def read_data(self):
        """
        Effectue une mesure et retourne les valeurs brutes.
        Retourne (raw_humidity, raw_temperature) ou (None, None) en cas d'échec.
        """
        self._trigger_measurement()
        utime.sleep_ms(80) # Attente de mesure
        
        while self._is_busy():
            utime.sleep_ms(10)
            
        if not self._read_raw_data():
            return None, None # Echec de lecture I2C
        
        # Le premier octet est le statut
        raw_humidity = ((self.buf[1] << 12) | (self.buf[2] << 4) | (self.buf[3] >> 4))
        raw_temperature = (((self.buf[3] & 0x0F) << 16) | (self.buf[4] << 8) | self.buf[5])
        
        return raw_humidity, raw_temperature

    # --- Fonctions Publiques (basées sur la Leçon 10) ---

    def dht20_temperature(self):
        """Retourne la température en Celsius"""
        raw_h, raw_t = self.read_data()
        if raw_t is None:
            return 0.0 # Retourne 0 en cas d'erreur
            
        temperature_c = (raw_t / 1048576) * 200 - 50
        return temperature_c

    def dht20_humidity(self):
        """Retourne l'humidité relative en %"""
        raw_h, raw_t = self.read_data() # Note: doit lire les deux
        if raw_h is None:
            return 0.0 # Retourne 0 en cas d'erreur
            
        humidity_rh = (raw_h / 1048576) * 100
        return humidity_rh