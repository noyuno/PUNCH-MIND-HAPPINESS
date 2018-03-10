import pigpio
import time
import re
from concurrent.futures import *
import sys

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
            if a[0].startswith("#"):
                melody.append({"comment":True, "measure":False, "text":" ".join(a)})
            elif a[0].startswith("+"):
                melody.append({"comment":False, "measure":True, "text":" ".join(a)})
            else:
                length=float(a[0])
                if len(a) < 2 or a[1] == "0":
                    melody.append({"comment":False, "measure":False, "length":length, "pause":True, "tanging":False})
                else:
                    sc=a[1]
                    if len(a) < 3:
                        melody.append({"comment":False, "measure":False,  "length":length, "scale":sc, "pause":False, "tanging":True})
                    else:
                        if a[2]=="n":
                            melody.append({"comment":False, "measure":False,  "length":length, "scale":sc, "pause":False, "tanging":False})
                        else:
                            melody.append({"comment":False, "measure":False,  "length":length, "scale":sc, "pause":False, "tanging":True})
    return melody

def play(scale, melody, speed, tanging, duty):
    pi1 = pigpio.pi()
    pi1.set_mode(BUZZER_GPIO_PIN, pigpio.OUTPUT)
    pi1.hardware_PWM(BUZZER_GPIO_PIN, 0, 0)
    measurestart=time.time()
    measureend=time.time()
    start=time.time()
    end=time.time()
    t=0.0
    lastlength=0.0
    lastscale=""
    measure=""
    lastpause=False
    en=False
    enable=len(sys.argv)==1
    try:
        for m in melody:
            end=time.time()
            if m["comment"]:
                continue
            if en:
                print("{0} {1}\tlen={2:.3f} want={3:.3f} act={4:.3f}\n".format(
                    measure, lastscale, lastlength, t, end-start), end="")
                start=time.time()
                en=False
            if m["measure"]:
                measureend=time.time()
                print("{0}: {1:.3f}".format(measure, measureend-measurestart))
                measure=m["text"].replace("+", "")
                if len(sys.argv)>1 and sys.argv[1]==measure:
                    enable=True
                measurestart=time.time()
                continue
            if not enable:
                continue
            en=True
            t=60.0 / speed * m["length"]
            t1=60.0 / speed / 10.0
            ordertime=0.00080
            ttang=0.0
            lastlength=m["length"]
            if m["pause"]:
                lastscale="p"
            else:
                lastscale=m["scale"]
            lastpause=m["pause"]

            if m["tanging"]:
                ttang=tanging
            if m["pause"]:
                #print("{0}: pause".format(t))
                pi1.hardware_PWM(BUZZER_GPIO_PIN, 0, 0)
                time.sleep(t - ttang-ordertime)
            else:
                #print("{0} {1} {2}".format(m["length"], m["scale"], scale[m["scale"]]))
                c=0.0
                d=duty
                tt=t-ttang
                #if lastscale=="p":
                #    tt-=ordertime
                pi1.hardware_PWM(BUZZER_GPIO_PIN, scale[m["scale"]], int(d))
                time.sleep(tt)
                #while c < tt:
                #    #print(m["scale"])
                #    if d > 0:
                #        pi1.hardware_PWM(BUZZER_GPIO_PIN, scale[m["scale"]], int(d))
                #    d-=duty/50
                #    if (tt-c-ordertime)>t1:
                #        #print("1:{0}".format(t1-ordertime))
                #        time.sleep(t1-ordertime)
                #        #time.sleep(t1)
                #    else:
                #        if (tt-c-ordertime)>0.0:
                #        #print("2:{0}".format(tt-c-ordertime))
                #            time.sleep(tt-c-ordertime)
                #    c += t1
            # tanging
            if m["tanging"]:
                pi1.hardware_PWM(BUZZER_GPIO_PIN, 0, 0)
                time.sleep(ttang-ordertime)
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
    play(scale, melody, 158*4, 0.04, 500000)

