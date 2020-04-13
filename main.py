# ToDo - Add LCD

from machine import Pin


class LEDS:
    """Control LEDS."""

    def __init__(self):
        self.percent = 0
        self.total_bars = 5

        # LED bars - sets the pins to outputs for the LED strips
        self.bar_1 = Pin(16, Pin.OUT)   # D0
        self.bar_2 = Pin(5, Pin.OUT)    # D1
        self.bar_3 = Pin(4, Pin.OUT)    # D2
        self.bar_4 = Pin(2, Pin.OUT)    # D4
        self.bar_5 = Pin(14, Pin.OUT)   # D5

    def percent_2_bars(self, percent):
        """Calculate LED bars based on percentage."""
        return round((percent * self.total_bars) / 100)

    def get_bars(self):
        """Turn the current bars based on the current stored percentage."""
        return self.percent_2_bars(self.percent)

    def get_percent(self):
        """Return the current percentage."""
        return self.percent

    def set_percent(self, percent):
        """Set the LEDS class percentage and turn on corresponding LEDS."""
        self.percent = percent
        self.set_bars()

    def set_bars(self):
        """Turn on leds based on percentage."""
        bars = self.percent_2_bars(self.percent)

        self.bar_1.off()
        self.bar_2.off()
        self.bar_3.off()
        self.bar_4.off()
        self.bar_5.off()
        if bars >= 1:
            self.bar_1.on()
        if bars >= 2:
            self.bar_2.on()
        if bars >= 3:
            self.bar_3.on()
        if bars >= 4:
            self.bar_4.on()
        if bars >= 5:
            self.bar_5.on()


class Router:
    """Contain Router specifications."""

    def __init__(self, ssid, bssid, rssi):
        """ssid = mesh network identifier
           bssid = router unique identifier
           rssi = signal strength"""
        self.ssid = ssid
        self.bssid = bssid
        self.rssi = rssi

    def get_signal_percent(self):
        """Return the signal percent based on the RSSI value."""
        # RSSI or this signal value is measured in decibels from 0 (zero) to
        # -120 (minus 120). The closer the value to 0 (zero), the stronger the
        # signal will be.
        if self.rssi < -80:
            return 20
        elif self.rssi < -70:
            return 40
        elif self.rssi < -60:
            return 60
        elif self.rssi < -50:
            return 80
        elif self.rssi <= 0:
            return 100
        else:
            return 0

    def __str__(self):
        """String print format for Router."""
        return ("SSID: {} \n "
                "BSSID: {} \n "
                "RSSI: {} \n "
                "Strength %: {} \n\n").format(self.ssid, self.bssid, self.rssi,
                                              self.get_signal_percent())


class Wifi:
    """Return specified Router instances."""

    def get_all_routers(self):
        """Return a list of Router instances for all scanned routers."""
        import network
        sta_if = network.WLAN(network.STA_IF)
        all_routers = sta_if.scan()

        routers = []
        for router_tuple in all_routers:
            router = Router(router_tuple[0], router_tuple[1], router_tuple[3])
            routers.append(router)

        return routers

    def get_routers_with_name(self, router_name):
        """Return a list of Router instances with the SSID = router_name."""
        routers = []

        for router in self.get_all_routers():
            if router.ssid == router_name:
                routers.append(router)

        return routers


class Button:
    """Connect button pin number with button functionality function."""

    def __init__(self, pin_num, button_func):
        """pin_num = pin number of button
           button_func = function that contains desired button functionality"""
        self.pin = Pin(pin_num, Pin.IN)
        print(pin_num, button_func)
        self.pin.irq(trigger=Pin.IRQ_RISING, handler=button_func)


class Main:
    """Create connections between the Wifi, Router, Button, and LEDS classes."""

    def __init__(self):
        print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
        self.button_pin = 12
        self.current_button_num = -1
        self.wifi = Wifi()
        self.leds = LEDS()
        self.sponge_routers = \
            self.wifi.get_routers_with_name(b'\xf0\x9f\xa7\xbd')
        self.len_sponge_routers = len(self.sponge_routers)
        self.button = Button(self.button_pin, self.button_func)  # D6

    def button_func(self, pin):
        """Set LEDS and print current router info based on button press."""
        if self.current_button_num == self.len_sponge_routers - 1:
            self.current_button_num = 0
        else:
            self.current_button_num += 1
        print(self.current_button_num)
        current_router = self.sponge_routers[self.current_button_num]
        print("sponge_router: " + str(current_router))

        signal_percent = current_router.get_signal_percent()
        print("Signal percent:", signal_percent)
        self.leds.set_percent(signal_percent)
        print("LED percent", self.leds.percent)
        print("Bars:", self.leds.get_bars())


def main():
    """Create an instance of the Main class."""
    Main()


# If this script is run itself, call main
if __name__ == '__main__':
    main()
