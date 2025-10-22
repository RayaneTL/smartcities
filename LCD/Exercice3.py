import machine
import utime
from lcd1602 import LCD1602 # Bibliothèque pour l'écran LCD
from dht11 import DHT       # Bibliothèque pour le capteur DHT11

# --- 1. Initialisation du Matériel (selon votre image) ---

# Potentiomètre (Température de consigne) sur A0 -> GP26
pot = machine.ADC(machine.Pin(26))

# Capteur de température DHT11 sur D18 -> GP18
dht = DHT(18)

# LED (Indicateur visuel) sur D16 -> GP16 (en PWM pour le bonus)
led_pwm = machine.PWM(machine.Pin(16))
led_pwm.freq(1000)
led_pwm.duty_u16(0) # Commencer éteint

# Buzzer (Alarme sonore) sur D20 -> GP20 (en PWM)
buzzer = machine.PWM(machine.Pin(20))
buzzer.duty_u16(0) # Commencer silencieux

# Écran LCD 16x2 I2C sur I2C1 -> SCL=GP7, SDA=GP6
i2c = machine.I2C(1, scl=machine.Pin(7), sda=machine.Pin(6), freq=400000)

# Initialise le LCD. Utilise l'adresse par défaut 0x27 (corrigé dans lcd1602.py)
lcd = LCD1602(i2c, 2, 16) 
lcd.display()
lcd.clear()

print("Système de contrôle de température démarré.")

# --- 2. Fonctions Utilitaires ---

def map_value(x, in_min, in_max, out_min, out_max):
    """Mappe une valeur d'une plage (ex: 0-65535) à une autre (ex: 15-35)."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def set_buzzer(state):
    """Active (True) ou désactive (False) le buzzer."""
    if state:
        buzzer.freq(2000)
        buzzer.duty_u16(32768) # Volume à 50%
    else:
        buzzer.duty_u16(0) # Silencieux

# --- 3. Variables Globales pour la Boucle ---
set_temp = 25.0
measured_temp = 0.0

last_sensor_read = 0
sensor_read_interval = 1000 # Lire les capteurs chaque seconde

# Variables pour le bonus LED (battement/dimmer)
breath_val = 0
breath_dir = 1
breath_step = 1310 
last_led_update = 0
led_update_interval = 20 # Mettre à jour la LED toutes les 20ms

# Variables pour le bonus Alarme (défilement)
alarm_text = "   *** ALARME *** "
scroll_pos = 0
last_alarm_update = 0
alarm_update_interval = 350 # Vitesse de défilement

# --- 4. Boucle Principale ---

while True:
    current_time = utime.ticks_ms()

    # --- TÂCHE 1: Lecture Capteurs (toutes les secondes) ---
    if utime.ticks_diff(current_time, last_sensor_read) >= sensor_read_interval:
        last_sensor_read = current_time

        # 1a. Lire le potentiomètre et mapper en T° de consigne (15-35°C)
        pot_val = pot.read_u16() 
        set_temp = map_value(pot_val, 0, 65535, 15.0, 35.0)

        # 1b. Lire le capteur DHT11
        try:
            temp, humid = dht.readTempHumid() 
            if temp is not None:
                measured_temp = temp
            print(f"Consigne: {set_temp:.1f}C, Ambiante: {measured_temp:.1f}C")
        except Exception as e:
            print(f"Erreur lecture DHT11: {e}")

        # 1c. Afficher les températures sur le LCD
        lcd.clear()
        lcd.setCursor(0, 0) # Ligne 1
        lcd.print(f"Set: {set_temp:.1f}C")
        lcd.setCursor(0, 1) # Ligne 2
        lcd.print(f"Ambient: {measured_temp:.1f}C")

    # --- TÂCHE 2: Logique de Contrôle & Sorties ---
    
    if measured_temp > set_temp + 3:
        system_state = 'ALARME'
    elif measured_temp > set_temp:
        system_state = 'CHAUD'
    else:
        system_state = 'NORMAL'

    # --- Sortie LED (avec bonus) ---
    if system_state == 'ALARME':
        # "clignote plus rapidement"
        if utime.ticks_diff(current_time, last_led_update) >= 250: # Cycle de 500ms
            last_led_update = current_time
            if led_pwm.duty_u16() > 0:
                led_pwm.duty_u16(0)
            else:
                led_pwm.duty_u16(65535) # Pleine puissance

    elif system_state == 'CHAUD':
        # "bat à une fréquence de 0,5 Hz" + "Bonus: battement progressif"
        if utime.ticks_diff(current_time, last_led_update) >= led_update_interval:
            last_led_update = current_time
            
            breath_val += breath_dir * breath_step
            
            if breath_val >= 65535:
                breath_val = 65535
                breath_dir = -1 # Descendre
            elif breath_val <= 0:
                breath_val = 0
                breath_dir = 1 # Monter
                
            led_pwm.duty_u16(breath_val)

    else: # system_state == 'NORMAL'
        led_pwm.duty_u16(0) # LED éteinte
        breath_val = 0 
        breath_dir = 1

    # --- Sortie Buzzer ---
    set_buzzer(system_state == 'ALARME') 

    # --- Sortie LCD Alarme (avec bonus) ---
    if system_state == 'ALARME':
        # "Bonus: Faire défiler le mot 'ALARM'"
        if utime.ticks_diff(current_time, last_alarm_update) >= alarm_update_interval:
            last_alarm_update = current_time
            
            lcd.setCursor(0, 0)
            scroll_slice = alarm_text[scroll_pos : scroll_pos + 16]
            lcd.print(scroll_slice)
            
            scroll_pos += 1
            if scroll_pos > len(alarm_text) - 16:
                scroll_pos = 0 
    else:
        scroll_pos = 0

    utime.sleep_ms(10)
