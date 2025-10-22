# Exercice 1 : LED qui clignote selon le nombre d'appuis
# Matériel (Grove Shield) :
# - Button sur D16  -> GP16
# - LED sur D18     -> GP18

from machine import Pin
import time

LED_PIN = 18      # D18
BTN_PIN = 16      # D16

led = Pin(LED_PIN, Pin.OUT)
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_DOWN)  # Le bouton renvoie 1 quand pressé

mode = 0  # 0 = arrêt, 1 = 0.5 Hz, 2 = rapide
last_btn = 0
last_change_ms = 0
DEBOUNCE_MS = 200

# Temporisations par mode
# 0.5 Hz = bascule chaque 1.0 s (ON/OFF) -> clignote 0,5 fois par seconde
DELAY_BY_MODE = {
    1: 1.0,   # lent (0,5 Hz)
    2: 0.25,  # rapide
}

while True:
    now = time.ticks_ms()
    cur = btn.value()

    # Détection front montant avec anti-rebond
    if cur == 1 and last_btn == 0 and time.ticks_diff(now, last_change_ms) > DEBOUNCE_MS:
        last_change_ms = now
        # 1er appui -> mode 1, 2e -> mode 2, 3e -> stop, puis on boucle
        mode = (mode % 3) + 1
        if mode == 3:
            # 3e mode = arrêt : éteindre et rester fixe jusqu’au prochain appui
            led.value(0)

    last_btn = cur

    # Exécution selon le mode
    if mode in (1, 2):
        led.toggle()
        time.sleep(DELAY_BY_MODE[mode])
    else:
        # mode 3 (arrêt)
        time.sleep(0.05)
