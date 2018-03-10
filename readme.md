PUNCH☆MIND☆HAPPINES をRaspberry Pi 3に接続されたブザーで鳴らす
---

~~~
sudo apt install pigpio
sudo pigpiod
pip3 install pigpio
python3 buzzer.py
~~~

ピン番号はGPIO番号で，`BUZZER_GPIO_PIN`に記載．
抵抗は10[kΩ]くらいは入れたらいいんでね

サビから
~~~
python3 buzzer.py 38
~~~

[hook.m4a](https://raw.githubusercontent.com/noyuno/PUNCH-MIND-HAPPINESS/master/hook.m4a)

