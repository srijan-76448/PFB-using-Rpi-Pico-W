from machine import *
from time import sleep


motor_info = {
    "EnA": 16,
    "EnB": 22,
    "In1": 18,
    "In2": 19,
    "In3": 20,
    "In4": 21,
    "freq": 500,
    "speed_range": (25000, 65534),
    "speed": 10
}
motor_pins = {
    "In1": Pin(motor_info["In1"], Pin.OUT),
    "In2": Pin(motor_info["In2"], Pin.OUT),
    "In3": Pin(motor_info["In3"], Pin.OUT),
    "In4": Pin(motor_info["In4"], Pin.OUT),
    "EnA": PWM(Pin(motor_info["EnA"])),
    "EnB": PWM(Pin(motor_info["EnB"]))
}

interval = 2


def interprate(x: float, xp: tuple, fp: tuple):
    left_min = xp[0]
    left_max = xp[1]
    right_min = fp[0]
    right_max = fp[1]

    leftSpan = left_max - left_min
    rightSpan = right_max - right_min
    scaleFactor = float(rightSpan) / float(leftSpan)

    return right_min + (x-left_min)*scaleFactor


def set_speed(p: int, speed_range: list = motor_info["speed_range"], percentage: list = (0, 100)):
    speed = int(interprate(p, percentage, speed_range))

    motor_pins["EnA"].freq(motor_info["freq"])
    motor_pins["EnB"].freq(motor_info["freq"])

    motor_pins["EnA"].duty_u16(speed)
    motor_pins["EnB"].duty_u16(speed)

    print("motor speed:", speed)


def stop_motor():
    set_speed(0)


def main():
    set_speed(motor_info["speed"])

    while True:
        motor_pins["In1"].value(1)
        motor_pins["In2"].value(0)
        print("Motor-A ↑")
        sleep(interval)

        motor_pins["In1"].value(0)
        motor_pins["In2"].value(0)
        motor_pins["In3"].value(0)
        motor_pins["In4"].value(0)
        sleep(interval/2)


        motor_pins["In1"].value(0)
        motor_pins["In2"].value(1)
        print("Motor-A ↓")
        sleep(interval)

        motor_pins["In1"].value(0)
        motor_pins["In2"].value(0)
        motor_pins["In3"].value(0)
        motor_pins["In4"].value(0)
        sleep(interval/2)


        motor_pins["In3"].value(1)
        motor_pins["In4"].value(0)
        print("Motor-B ↑")
        sleep(interval)

        motor_pins["In1"].value(0)
        motor_pins["In2"].value(0)
        motor_pins["In3"].value(0)
        motor_pins["In4"].value(0)
        sleep(interval/2)


        motor_pins["In3"].value(0)
        motor_pins["In4"].value(1)
        print("Motor-B ↓")
        sleep(interval)

        motor_pins["In1"].value(0)
        motor_pins["In2"].value(0)
        motor_pins["In3"].value(0)
        motor_pins["In4"].value(0)
        sleep(interval/2)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        stop_motor()
        exit()