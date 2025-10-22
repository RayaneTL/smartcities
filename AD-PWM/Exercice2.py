# Exercice 2 — Volume d'une mélodie (potentiomètre) + bonus bouton/LED
# Matériel (Grove Shield) :
#  - Potentiomètre  A0 -> GP26/ADC0
#  - Buzzer passif D20 -> GP20 (PWM)
#  - Bouton       (opt) D16 -> GP16 (IN, PULL_DOWN)
#  - LED          (opt) D18 -> GP18 (OUT)

from machine import Pin, ADC, PWM
import time

# ---- Broches ----
pot = ADC(26)                 # A0
buz = PWM(Pin(20))            # D20 (PWM pour volume)
buz.freq(440)
buz.duty_u16(0)               # muet au démarrage

try:
    btn = Pin(16, Pin.IN, Pin.PULL_DOWN)   # D16 (optionnel)
except:
    btn = None

try:
    led = Pin(18, Pin.OUT)                 # D18 (optionnel)
except:
    led = None

# ---- Fréquences des notes (A4 = 440 Hz) ----
N = {
 'C4':262, 'D4':294, 'E4':330, 'F4':349, 'G4':392, 'A4':440, 'B4':494,
 'C5':523, 'D5':587, 'E5':659, 'F5':698, 'G5':784, 'A5':880, 'B5':988,
 'R': 0  # Rest (silence)
}

# Deux petites mélodies (note, durée_en_noires)
MELODY_1 = [
    ('E5',1), ('D5',1), ('C5',1), ('D5',1),
    ('E5',1), ('E5',1), ('E5',2),
    ('D5',1), ('D5',1), ('D5',2),
    ('E5',1), ('G5',1), ('G5',2),
]

MELODY_2 = [
    ('C5',1), ('E5',1), ('G5',1), ('C5',1),
    ('B4',1), ('G4',1), ('E4',1), ('C4',1),
    ('R', 1), ('C5',1), ('G4',1), ('E4',1),
]

melodies = [MELODY_1, MELODY_2]
mel_idx = 0

# Tempo (noire) en millisecondes
BPM = 120
BEAT_MS = int(60000 / BPM)     # 500 ms à 120 BPM

# Anti-rebond bouton
last_btn = 0
last_btn_ms = 0
DEBOUNCE = 200

# LED timing
last_led_ms = time.ticks_ms()
LED_HALF = BEAT_MS // 2

def read_volume_u16():
    """Map ADC 0..65535 -> duty 0..32768 (évite saturation)"""
    raw = pot.read_u16()
    # courbe douce (gamma ~2) pour un volume perçu plus régulier
    duty = int(((raw / 65535) ** 2) * 32768)
    return duty

def play_note(freq_hz, note_ms, duty):
    """Lecture non-bloquante d'une note avec volume ajustable en temps réel."""
    global last_led_ms
    t0 = time.ticks_ms()

    # Configure fréquence / silence
    if freq_hz <= 0:
        buz.duty_u16(0)
    else:
        buz.freq(freq_hz)
        buz.duty_u16(duty)

    while time.ticks_diff(time.ticks_ms(), t0) < note_ms:
        # Ajuste le volume à la volée
        buz.duty_u16(read_volume_u16())

        # Clignote au rythme (option LED)
        if led:
            now = time.ticks_ms()
            if time.ticks_diff(now, last_led_ms) >= LED_HALF:
                led.toggle()
                last_led_ms = now

        # Changement de mélodie (option bouton)
        if btn:
            now = time.ticks_ms()
            cur = btn.value()
            global mel_idx, last_btn, last_btn_ms
            if cur == 1 and last_btn == 0 and time.ticks_diff(now, last_btn_ms) > DEBOUNCE:
                last_btn_ms = now
                mel_idx = (mel_idx + 1) % len(melodies)
            last_btn = cur

        time.sleep_ms(5)

    # Fin de note
    buz.duty_u16(0)
    if led:
        led.value(0)

# ---- Boucle principale : joue la mélodie en boucle ----
while True:
    for note, beats in melodies[mel_idx]:
        dur = BEAT_MS * beats
        freq = N[note]
        play_note(freq, dur, read_volume_u16())
