import pigpio
import time
import re

BUZZER_GPIO_PIN = 12


def readscale():
    scale={}
    with open("scale", "r") as f:
        for line in f:
            line2=line.replace("\n", "")
            a = re.split(" +", line2)
            if len(a) < 2:
                continue
            key = a[0]
            value = int(float(a[1]))
            scale[key] = value
    return scale

def readmelody():
    melody = []
    with open("melody", "r") as f:
        for line in f:
            line2=line.replace("\n", "")
            a = re.split(" +", line2)
            if a[0] == "":
                continue
            length=float(a[0])
            if len(a) < 2 or a[1] == "0":
                melody.append({"length":length, "pause":True})
            else:
                sc=a[1]
                melody.append({"length":length, "scale":sc, "pause":False})
    return melody

def play(scale, melody, speed, tanging):
    pi1 = pigpio.pi()
    pi1.set_mode(BUZZER_GPIO_PIN, pigpio.OUTPUT)
    pi1.hardware_PWM(BUZZER_GPIO_PIN, 0, 0)
    try:
        for m in melody:
            t=60.0 / speed * m["length"]
            if m["pause"]:
                #print("{0}: pause".format(t))
                pi1.hardware_PWM(BUZZER_GPIO_PIN, 0, 500000)
            else:
                #print("{0}: {1}".format(t, scale[m["scale"]]))
                pi1.hardware_PWM(BUZZER_GPIO_PIN, scale[m["scale"]], 500000)
            time.sleep(t - tanging / 1000.0)
            # tanging
            pi1.hardware_PWM(BUZZER_GPIO_PIN, 0, 500000)
            time.sleep(tanging / 1000.0)
    except Exception as err:
        print("error: {0}".format(err))
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        pi1.hardware_PWM(BUZZER_GPIO_PIN, 0, 0)
        pi1.set_mode(BUZZER_GPIO_PIN, pigpio.INPUT)
        pi1.stop()

if __name__ == '__main__':
    scale = readscale()
    melody = readmelody()
    #print(melody)
    play(scale, melody, 580, 40)

