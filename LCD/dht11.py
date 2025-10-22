# Fichier: dht11.py
from machine import Pin
import utime

class DHT:
    def __init__(self, pin_num):
        self.pin = Pin(pin_num)
        self.last_read_ok = False
        self.temperature = 0.0
        self.humidity = 0.0
        self._trigger() 

    def _trigger(self):
        self.pin.init(Pin.OUT, Pin.PULL_DOWN)
        self.pin.value(0)
        utime.sleep_ms(18) 
        self.pin.value(1)
        utime.sleep_us(30) 
        self.pin.init(Pin.IN, Pin.PULL_UP)

    def _read_data(self):
        data = bytearray(5)
        utime.sleep_us(40)
        
        if self.pin.value() == 1:
            return None 
        
        while self.pin.value() == 0: pass
        while self.pin.value() == 1: pass
        
        for i in range(5):
            for j in range(8):
                while self.pin.value() == 0: pass
                utime.sleep_us(30)
                if self.pin.value() == 1:
                    data[i] |= (1 << (7 - j))
                    while self.pin.value() == 1: pass
        
        return data

    def measure(self):
        self.last_read_ok = False
        self._trigger()
        
        data = self._read_data()
        
        if data is None:
            print("Erreur: Pas de réponse du DHT11")
            return

        if (data[0] + data[1] + data[2] + data[3]) & 0xFF != data[4]:
            print("Erreur: Checksum invalide")
            return
            
        self.humidity = float(data[0]) 
        self.temperature = float(data[2]) 
        self.last_read_ok = True

    def readTempHumid(self):
        """Fonction principale appelée par l'Exercice 3."""
        self.measure()
        if self.last_read_ok:
            return self.temperature, self.humidity
        else:
            # Retourne les dernières valeurs connues si la lecture échoue
            return self.temperature, self.humidity
