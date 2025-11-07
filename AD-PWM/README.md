# Exercice 2 — Volume d’une mélodie (potentiomètre)

## 🎯 Objectif
Créer un programme MicroPython qui joue une **mélodie en boucle**, dont le **volume** est contrôlé en temps réel par un **potentiomètre**. *(Bonus : bouton pour changer de mélodie, LED qui clignote au rythme).*  
> D’après l’énoncé “EXERCICE 2 : VOLUME D’UNE MÉLODIE”. 

## ⚙️ Matériel
- Raspberry Pi Pico / Pico W  
- Grove Shield for Pico (recommandé)  
- Potentiomètre (Grove Rotary)  
- Buzzer **passif** (PWM)  
- *(Bonus)* Bouton poussoir, LED + résistance (si hors Grove)

## 🔌 Câblage (Grove)
| Élément | Port | Broche Pico |
|---|---|---|
| Potentiomètre | **A0** | GP26/ADC0 |
| Buzzer passif | **D20** | GP20 (PWM) |
| Bouton (bonus) | **D16** | GP16 |
| LED (bonus) | **D18** | GP18 |

## ▶️ Utilisation
1. Envoyer `Exercice2.py` sur le Pico .  
2. Le programme joue la mélodie en boucle.  
3. Tourner le **potentiomètre** → le **volume** change **instantanément**.  
4. *(Bonus)* Appuyer sur le **bouton (D16)** pour changer de mélodie.  
5. *(Bonus)* La **LED (D18)** clignote sur le tempo.


# Exercice 4 — Grove Sound Sensor + Grove RGB LED (P9813)

## 🎯 Objectif
Faire réagir la **LED RGB Grove (P9813)** en fonction du volume sonore capté par le **capteur de son Grove (A0)**.

## ⚙️ Matériel
- Raspberry Pi Pico / Pico W  
- Grove Shield for Pico  
- Grove Sound Sensor (A0)  
- Grove RGB LED (P9813, D16)  
- 2 câbles Grove

## 🔌 Câblage
| Élément | Port | Broche Pico | Fonction |
|----------|------|--------------|-----------|
| Sound Sensor | **A0** | GP26 (ADC0) | Entrée analogique |
| RGB LED (P9813) | **D16** | GP16 (CLK) + GP17 (DATA) | Sortie série |
| GND commun | — | GND | Masse commune |

## ▶️ Utilisation
1. Copier `P9813.py` et `main.py` sur le Pico.  
2. Connecter le micro sur A0 et la LED RGB sur D16.  
3. Parler ou faire du bruit → la LED change de couleur selon l’intensité du son.

## 🧠 Explication
- Le capteur de son fournit une tension analogique proportionnelle au volume.  
- Cette valeur est convertie (ADC) et filtrée.  
- Le module `P9813` envoie une trame série au driver RGB pour modifier la couleur.  

## ✅ Résultat attendu
La LED RGB change de couleur : vert quand calme, rouge quand le volume augmente, violet pour les sons forts.
