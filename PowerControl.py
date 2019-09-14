#################################################################################################################################################################
#  GND  #GPIO26 #GPIO19 #GPIO13 # GPIO6 # GPIO5 #  DNC  #  GND  #GPIO11 # GPIO9 #GPIO10 #  3.3V #GPIO22 #GPIO27 #GPIO17 #  GND  # GPIO4 # GPIO3 # GPIO2 # 3.3V  #
#################################################################################################################################################################
#   39  #   37  #   35  #   33  #   31  #   29  #   27  #   25  #   23  #   21  #   19  #   17  #   15  #   13  #   11  #   9   #   7   #   5   #   3   #   1   #
#################################################################################################################################################################
#   40  #   38  #   36  #   34  #   32  #   30  #   28  #   26  #   24  #   22  #   20  #   18  #   16  #   14  #   12  #   10  #   8   #   6   #   4   #   2   #
#################################################################################################################################################################
#GPIO21 #GPIO20 #GPIO16 #  GND  #GPIO12 #  GND  #  DNC  # GPIO7 # GPIO8 #GPIO25 #  GND  #GPIO24 #GPIO23 #  GND  #GPIO18 #GPIO15 #GPIO14 #  GND  #  5V   #  5V   #
#################################################################################################################################################################

# GPIO21        -- Зелёный - управляющий всей нагрузкой
# GPIO20        -- Жёлтый  - камеры
# GPIO16        -- Белый   - Teltonika
# pin 17 (3.3V) -- Чёрный  - реле +
# GPIO22        -- Чёрный  - реле (считывание)
# pin 4 (5V)    -- Жёлтый  - Питание +
# pin 6 (GND)   -- Чёрный  - Питание -

# GPIO.LOW  == 0    # Верхний уровень сигнала (3.3V)
# GPIO.HIGH == 1    # Нижний уровень сигнала (0V)

# IMPORT SECTION #
import RPi.GPIO as GPIO
import time
import requests
import os
# ================= #

# GLOBAL VARS #
net_restart = "sudo /etc/init.d/networking restart"
router_ip = "192.168.0.1"
startDT = 0

pinControl = 21 # Зёлный пин
pinCamera = 20 # Жёлтый пин
pinTeltonika = 16 # Белый пин
pinRely = 22 # Чёрный GPIO пин
# ================= #

# GLOBAL SETTINGS #
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(pinControl, GPIO.OUT)
GPIO.setup(pinCamera, GPIO.OUT)
GPIO.setup(pinTeltonika, GPIO.OUT)

GPIO.setup(pinRely, GPIO.IN)
# ================= #

# DEBUG PRESET #
#GPIO.output(20, GPIO.HIGH)
#GPIO.output(21, GPIO.LOW)
#GPIO.output(16, GPIO.LOW)
# ================= #

# MAIN PROGRAM #
try:
    while True:
        networkResponse = os.system("ping -c 1 -w 1 " + router_ip) # Наличие подключения сети
        time.sleep(2)
        relyConnect = GPIO.input(pinRely) # Наличие замыкания на реле

        print("--== [ DEBUG INFO ] ==--")
        print("rely_truth = " + str(relyConnect))

        if networkResponse == 0:
            networkResponse = 1
        else:
            networkResponse = 0
        
        print("rely = " + str(relyConnect))
        print("net = " + str(networkResponse))
        if startDT != 0:
            print("DT = " + str(int(time.time() - startDT)))
        print("--== [ END OF DEBUG INFO ] ==--")
        time.sleep(1)

        if relyConnect == 1 or networkResponse == 1:
            startDT = 0
        
        if relyConnect == 1:
            GPIO.output(pinControl, GPIO.LOW)
            GPIO.output(pinCamera, GPIO.LOW)
            GPIO.output(pinTeltonika, GPIO.LOW)
        elif networkResponse == 1:
            GPIO.output(pinControl, GPIO.LOW)
            GPIO.output(pinCamera, GPIO.HIGH)
            GPIO.output(pinTeltonika, GPIO.HIGH)
        else:
            if startDT == 0:
                startDT = time.time()
                print("Downtime timer started!")
            elif int(time.time() - startDT) >= 1200: # Время до даунтайма в секундах. (1200 = 20 min)
                GPIO.output(pinCamera, GPIO.HIGH)
                GPIO.output(pinTeltonika, GPIO.HIGH)
                GPIO.output(pinControl, GPIO.HIGH)
        time.sleep(2)
except KeyboardInterrupt:
    print("Exit by pressed Ctrl+C.")
except:
    print("There are unexpected program interruption.")
finally:
    GPIO.cleanup()
    print("--===[ END OF PROGRAM ]===--")
# ================= #
