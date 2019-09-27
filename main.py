

from machine import Pin
import time
import network
print('\n\n\n\n\n')


class Router():

    def __init__(self, router):
        self.ssid = router[0]
        self.bssid = router[1]
        self.RSSI = router[3]
        self.bars = 0

        # LED bars
        self.bar_1 = Pin(16, Pin.OUT)
        self.bar_2 = Pin(5, Pin.OUT)
        self.bar_3 = Pin(4, Pin.OUT)
        self.bar_4 = Pin(0, Pin.OUT)
        self.bar_5 = Pin(2, Pin.OUT)

    def lights_on(self, num):
        self.bar_1.off()
        self.bar_2.off()
        self.bar_3.off()
        self.bar_4.off()
        self.bar_5.off()
        if num >= 1:
            self.bar_1.on()
        if num >= 2:
            self.bar_2.on()
        if num >= 3:
            self.bar_3.on()
        if num >= 4:
            self.bar_4.on()
        if num >= 5:
            self.bar_5.on()

    def calc_bars(self):
        if self.RSSI < -82:
            self.bars = 1
        if self.RSSI < -77:
            self.bars = 2
        if self.RSSI < -72:
            self.bars = 3
        if self.RSSI < -67:
            self.bars = 4
        if self.RSSI < 0:
            self.bars = 5
        self.lights_on(self.bars)
        return self.bars


def main():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('🧽', '***REMOVED***')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

    network_list_all = sta_if.scan()
    print(network_list_all)
    network_list = []
    for network in network_list_all:
        if b'\xf0\x9f\xa7\xbd' in network:
            network_list.append(network)

    for router in network_list:
        Router(router)


main()

led = Pin(5, Pin.OUT)
led.off()



# def calc_bars(strength):
#     if strength < -82:
#         return 1
#     if strength < -77:
#         return 2
#     if strength < -72:
#         return 3
#     if strength < -67:
#         return 4
#     if strength < 0:
#         return 5
#
#
# sta_if = network.WLAN(network.STA_IF)
# if not sta_if.isconnected():
#     print('connecting to network...')
#     sta_if.active(True)
#     sta_if.connect('🧽', '***REMOVED***')
#     while not sta_if.isconnected():
#         pass
# print('network config:', sta_if.ifconfig())
# network_list_all = sta_if.scan()
# print(network_list_all)
# network_list = []
# for network in network_list_all:
#     if b'\xf0\x9f\xa7\xbd' in network:
#         network_list.append(network)
#
# for network in network_list:
#     strength = network[3]
#     bars = calc_bars(strength)
#     print(strength, bars)

# Todo:
#  Determine difference between bssid(s)
#  Clean up code (make functions)
#  Wire up and control buttons/LED strips


