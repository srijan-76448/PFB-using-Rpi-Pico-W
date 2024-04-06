from machine import *
from time import sleep


IR_sensor_io_pins = [8,9,10,11,12,13,14,15]
reverse = {
    "IRc": True,
    "IRl": True
}
interval = 0.5

IR_sensor_pins = [Pin(pin) for pin in IR_sensor_io_pins]
if reverse["IRl"]: IR_sensor_pins = IR_sensor_pins[::-1]


def read_IR_sensor_values() -> str:
    '''DEFAULT:
    Black -> False

    REVERSE:
    Black -> True
    '''

    ret = [bool(sensor.value()) for sensor in IR_sensor_pins]

    if reverse["IRc"]:
        ret = [not bool(r) for r in ret]

    p = '[ '

    for i in range(len(ret)):
        v = ret[i]
        
        if v:
            p += f"\033[1;32mIR{i}\033[0m "
        elif not v:
            p += f"\033[1;31mIR{i}\033[0m "

    p += ']'

    print(p)


if __name__ == "__main__":
    try:
        while True:
            read_IR_sensor_values()
            sleep(interval)

    except KeyboardInterrupt:
        exit()