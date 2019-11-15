""" This script finds the routers on the network, calculates the RSSI,
converts the RSSI value into strength bars, and displays the strength bars on
LED strips within a picture frame. When the button is pressed the display
cycles between the different routers in the mess network."""

from machine import Pin
import time

BUTTON_CNT = 0
NETWORK_LIST = []

print('\n\n\n\n\n')  # Print some new lines to separate printout from garbage


class Router:
    """Create a Router class based on the router passed in"""

    def __init__(self, router):
        """Initialize Router class variables"""
        self.ssid = router[0]
        self.bssid = router[1]
        self.RSSI = router[3]
        self.bars = 0
        self.location = ""

        # LED bars - sets the pins to outputs for the LED strips
        self.bar_1 = Pin(16, Pin.OUT)
        self.bar_2 = Pin(5, Pin.OUT)
        self.bar_3 = Pin(15, Pin.OUT)
        self.bar_4 = Pin(4, Pin.OUT)
        self.bar_5 = Pin(2, Pin.OUT)

        # Call calc_bars to calculate the strength bars based on the RSSI
        self.calc_bars()
        self.find_location()

    def find_location(self):
        """Based on the known BSSID(s) determine the location in the house"""
        if self.bssid == b'\xe6\x95nE\x1f\x18':
            self.location = "bedroom"
        elif self.bssid == b'\xe6\x95nE\x1e\xfe':
            self.location = "living room"
        elif self.bssid == b'\xe6\x95nJ=J':
            self.location = "kitchen"

    def lights_on(self, num):
        """Turn the appropriate lights on depending on the signal strength (num)
            Ex. num = 2 then bar_1.on() and bar_2.on()"""
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
        """Calculate the strength bars that correspond to the read RSSI value"""
        if self.RSSI < -82:
            self.bars = 1
        elif self.RSSI < -77:
            self.bars = 2
        elif self.RSSI < -72:
            self.bars = 3
        elif self.RSSI < -67:
            self.bars = 4
        elif self.RSSI < 0:
            self.bars = 5
        self.lights_on(self.bars)
        return self.bars

    def __str__(self):

        return ("SSID: {} \n "
                "BSSID: {} \n "
                "RSSI: {} \n "
                "bars: {} \n "
                "location: {}\n\n").format(self.ssid, self.bssid, self.RSSI,
                                           self.bars, self.location)


def main():
    """Set up network connection and display router signal strength on
    LED strips"""
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('🧽', 'password')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

    network_list_all = sta_if.scan()
    print(network_list_all)
    network_list = []
    for network in network_list_all:
        if b'\xf0\x9f\xa7\xbd' in network:
            network_list.append(network)

    button_cnt = 0
    button = Pin(14, Pin.IN)
    button.irq(trigger=Pin.IRQ_RISING, handler=callback)


def callback(p):
    print(p)
    if BUTTON_CNT == 2:
        BUTTON_CNT = 0
    else:
        BUTTON_CNT += 1

    print(Router(network_list[BUTTON_CNT]))
    print(BUTTON_CNT)


# If this script is run itself, call main
if __name__ == '__main__':
    main()

# Todo:
#  Determine difference between bssid(s)?
#  Wire up and control buttons/LED strips
#  Clean up code

# Guessing bssid(s) to rooms based on signal strength in bedroom
# SSID: b'\xf0\x9f\xa7\xbd'
# BSSID: b'\xe6\x95nE\x1f\x18' - bedroom
# RSSI: -17
# bars: 5

# SSID: b'\xf0\x9f\xa7\xbd'
# BSSID: b'\xe6\x95nE\x1e\xfe' - living room
# RSSI: -58
# bars: 5

# SSID: b'\xf0\x9f\xa7\xbd'
# BSSID: b'\xe6\x95nJ=J' - kitchen
# RSSI: -80
# bars: 2
