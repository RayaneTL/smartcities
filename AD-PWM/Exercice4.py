from p9813 import P9813
from machine import ADC
import time

mic = ADC(26)
led = P9813(clk_pin=16, data_pin=17, num_leds=1)

# --- Paramètres ---
alpha = 0.1        # filtrage
env = 0

print("Parlez près du micro : la LED réagit au son 🎵")

while True:
    val = mic.read_u16()
    env = alpha * val + (1 - alpha) * env  # filtrage simple
    # mappe env (0..65535) → 0..255
    level = int(min(255, env / 256))

    # Couleur = plus de rouge quand volume fort
    r = level
    g = 255 - level
    b = level // 2

    led.set_led(0, r, g, b)
    led.show()

    time.sleep_ms(30)
