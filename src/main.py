from machine import *


IR_sensor_io_pins = [8,9,10,11,12,13,14,15]
motor_info = {
    "EnA": 16,
    "EnB": 17,
    "In1": 18,
    "In2": 19,
    "In3": 20,
    "In4": 21,
    "freq": 500,
    "speed_range": (25000, 65534)
}
reverse = {
    "RM": False,
    "LM": False,
    "IRc": False,
    "IRl": True
}
line_width = 2
LED = 'LED'
led_opt = 0
stdout = False
speed = 10


motor_pins = {
    "In1": Pin(motor_info["In1"], Pin.OUT),
    "In2": Pin(motor_info["In2"], Pin.OUT),
    "In3": Pin(motor_info["In3"], Pin.OUT),
    "In4": Pin(motor_info["In4"], Pin.OUT),
    "EnA": PWM(Pin(motor_info["EnA"])),
    "EnB": PWM(Pin(motor_info["EnB"]))
}

led_pin = Pin(LED, Pin.OUT)
led_opt_pin = Pin(led_opt, Pin.OUT)

IR_sensor_pins = [Pin(pin) for pin in IR_sensor_io_pins]
if reverse["IRl"]: IR_sensor_pins = IR_sensor_pins[::-1]


def show(x):
    if stdout:
        print(x)


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


def move_fwd(IN1, IN2):
    show('fwd')
    IN1.value(1)
    IN2.value(0)


def move_bwd(IN1, IN2):
    show('bwd')
    IN1.value(0)
    IN2.value(1)


def stop(IN1, IN2):
    show('stop')
    IN1.value(0)
    IN2.value(0)


def read_IR_sensor_values():
    '''DEFAULT:
    Black -> False

    REVERSE:
    Black -> True
    '''

    ret = [bool(sensor.value()) for sensor in IR_sensor_pins]

    if reverse["IRc"]:
        ret = [not(bool(sensor.value())) for sensor in IR_sensor_pins]

    return ret


def move_to() -> dict:
    IR_values = read_IR_sensor_values()
    left_index = int((len(IR_sensor_pins)/2)-(line_width//2))
    riht_index = int((len(IR_sensor_pins)/2)+(line_width//2))

    ret = {
        "fwd": False,
        "rht": False,
        "lft": False
    }

    if IR_values[left_index] or IR_values[riht_index-1]:
        ret["fwd"] = True

    elif IR_values[left_index-1]:
        ret["lft"] = True

    elif IR_values[riht_index]:
        ret["rht"] = True

    elif IR_values[left_index-1] and IR_values[left_index] and IR_values[riht_index-1] and IR_values[riht_index]:
        ret["lft"] = False
        ret["rht"] = False
        ret["fwd"] = True

    show(IR_values)

    return ret


def check_point():
    if read_IR_sensor_values()[0] and read_IR_sensor_values()[-1]:
        led_opt_pin.value(1)
    else:
        led_opt_pin.value(0)


def main():
    led_pin.value(1)
    set_speed(speed)

    while True:
        direct = move_to()

        if direct['fwd']:
            move_fwd(motor_pins["In1"], motor_pins["In2"])
            move_fwd(motor_pins["In3"], motor_pins["In4"])

        if direct['lft']:
            stop(motor_pins["In1"], motor_pins["In2"])
            # move_bwd(motor_pins["In1"], motor_pins["In2"])
            move_fwd(motor_pins["In3"], motor_pins["In4"])

        if direct['rht']:
            move_fwd(motor_pins["In1"], motor_pins["In2"])
            # move_bwd(motor_pins["In3"], motor_pins["In4"])
            stop(motor_pins["In3"], motor_pins["In4"])

        if not (direct['fwd'] or direct['lft'] or direct['rht']):
            stop(motor_pins["In1"], motor_pins["In2"])
            stop(motor_pins["In3"], motor_pins["In4"])

        check_point()


if __name__ == "__main__":
    try:
        print("\033[1;33mRunning Bot\033[0m")
        main()

    except KeyboardInterrupt:
        exit()
