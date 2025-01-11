import serial_data as serial
def pick_up():
    serial.send_data('-')
    serial.send_data(":095")

    serial.send_data('F')
    serial.send_data('m')
    serial.send_data('F')
    serial.send_data(":105")
    serial.delay(100)
    serial.send_data(":097")
    serial.send_data('B')
    serial.send_data('B')
    serial.send_data('B')
    serial.delay(100)
    serial.send_data(":000")


def pick_down():

    serial.send_data('-')
    serial.send_data(":094")

    serial.send_data('F')
    serial.send_data('F')
    serial.send_data('n')
    serial.delay(100)
    serial.send_data('B')
    serial.send_data('B')
    serial.send_data('B')
    serial.delay(100)
    serial.send_data(":000")


serial.send_data('m')
pick_down()