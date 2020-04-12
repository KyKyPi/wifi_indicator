

from machine import Pin


class LEDS:

    def __init__(self):
        self.percent = 0
        self.total_bars = 5

        # LED bars - sets the pins to outputs for the LED strips
        self.bar_1 = Pin(5, Pin.OUT)
        self.bar_2 = Pin(16, Pin.OUT)
        self.bar_3 = Pin(15, Pin.OUT)
        self.bar_4 = Pin(4, Pin.OUT)
        self.bar_5 = Pin(2, Pin.OUT)

    def percent_2_bars(self, percent):
        return round((percent * self.total_bars) / 100)

    def get_bars(self):
        return self.percent_2_bars(self.percent)

    def get_percent(self):
        return self.percent

    def set_percent(self, percent):
        self.percent = percent
        self.set_bars()

    def set_bars(self):
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

    def __init__(self, ssid, bssid, rssi):
        self.ssid = ssid
        self.bssid = bssid
        self.rssi = rssi

    def get_signal_percent(self):
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

        return ("SSID: {} \n "
                "BSSID: {} \n "
                "RSSI: {} \n "
                "Strength %: {} \n\n").format(self.ssid, self.bssid, self.rssi,
                                              self.get_signal_percent())


class Wifi:

    def get_all_routers(self):
        import network
        sta_if = network.WLAN(network.STA_IF)
        all_routers = sta_if.scan()

        routers = []
        for router_tuple in all_routers:
            router = Router(router_tuple[0], router_tuple[1], router_tuple[3])
            routers.append(router)

        return routers

    def get_routers_with_name(self, router_name):
        routers = []

        for router in self.get_all_routers():
            if router.ssid == router_name:
                routers.append(router)

        return routers


class Button:
    def __init__(self, pin_num, button_func):
        self.pin = Pin(pin_num, Pin.IN)
        print(pin_num, button_func)
        self.pin.irq(trigger=Pin.IRQ_RISING, handler=button_func)


class Main:

    def __init__(self):
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        self.current_button_num = -1
        self.wifi = Wifi()
        self.leds = LEDS()
        # all_routers = wifi.get_all_routers()
        # print("all_routers: " + str(all_routers))
        self.sponge_routers = self.wifi.get_routers_with_name(b'\xf0\x9f\xa7\xbd')
        # for router in self.sponge_routers:
        self.button = Button(14, self.button_func)

    def button_func(self, pin):
        self.current_button_num += 1
        # ToDo - make button number wrap around
        print(self.current_button_num)
        current_router = self.sponge_routers[self.current_button_num]
        print("sponge_router: " + str(current_router))

        signal_percent = current_router.get_signal_percent()
        print("Signal percent:", signal_percent)
        self.leds.set_percent(signal_percent)
        print("LED percent", self.leds.percent)
        print("Bars:", self.leds.get_bars())


def main():
    Main()


# If this script is run itself, call main
if __name__ == '__main__':
    main()
