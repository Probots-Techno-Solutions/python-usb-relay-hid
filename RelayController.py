import pywinusb.hid as hid
from time import sleep


class RelayController:
    USB_CFG_VENDOR_ID = 0x16c0  # /* 5824 = voti.nl */
    USB_CFG_DEVICE_ID = 0x05DF  # /* obdev's shared PID for HIDs */
    USB_RELAY_VENDOR_NAME = "www.dcttech.com"
    USB_RELAY_NAME_PREF = "USBRelay"  # /* can be relay1... relay8 */
    USB_RELAY_ID_STR_LEN = 5  # /* length of "unique serial number" in the devices */

    filter = None
    hid_device = None
    device = None
    report = None

    last_row_status = None

    def __init__(self):
        self.get_Hid_USBRelay()

    def get_Hid_USBRelay(self):
        self.filter = hid.HidDeviceFilter(vendor_id=self.USB_CFG_VENDOR_ID, product_id=self.USB_CFG_DEVICE_ID)
        self.hid_device = self.filter.get_devices()
        self.device = self.hid_device[0]

    def open_device(self):
        if self.device.is_active():
            if not self.device.is_opened():
                self.device.open()
                self.get_report()
                return True
            else:
                print("Device already opened")
                return True
        else:
            print("Device is not active")

        return False

    def close_device(self):
        if self.device.is_active():
            if self.device.is_opened():
                self.device.close()
                return True
            else:
                print("Device already closed")
        else:
            print("Device is not active")

        return True

    def refresh(self):
        self.get_Hid_USBRelay()
        self.open_device()

    def get_report(self):
        if not self.device.is_active():
            self.report = None

        for rep in self.device.find_output_reports() + self.device.find_feature_reports():
            self.report = rep

    def read_status_row(self):
        if self.report is None:
            print("Cannot read report")
            self.last_row_status = [0, 1, 0, 0, 0, 0, 0, 0, 3]
        else:
            self.last_row_status = self.report.get()
        return self.last_row_status

    def write_row_data(self, buffer: list):
        if self.report is not None:
            self.report.send(raw_data=buffer)
            return True
        else:
            print("Cannot write in the report. check if your device is still plugged")
            return False

    def on_all(self):
        if self.write_row_data(buffer=[0, 0xFE, 0, 0, 0, 0, 0, 0, 1]):
            return self.read_relay_status(relay_number=3)
        else:
            print("Cannot put ON relays")
            return False

    def off_all(self):
        if self.write_row_data(buffer=[0, 0xFC, 0, 0, 0, 0, 0, 0, 1]):
            return self.read_relay_status(relay_number=3)
        else:
            print("Cannot put OFF relays")
            return False

    def on_relay(self, relay_number):
        if self.write_row_data(buffer=[0, 0xFF, relay_number, 0, 0, 0, 0, 0, 1]):
            return self.read_relay_status(relay_number)
        else:
            print("Cannot put ON relay number {}".format(relay_number))
            return False

    def off_relay(self, relay_number):
        if self.write_row_data(buffer=[0, 0xFD, relay_number, 0, 0, 0, 0, 0, 1]):
            return self.read_relay_status(relay_number)
        else:
            print("Cannot put OFF relay number {}".format(relay_number))
            return False

    def read_relay_status(self, relay_number):
        buffer = self.read_status_row()
        return relay_number & buffer[8]

    def is_relay_on(self, relay_number):
        return self.read_relay_status(relay_number) > 0


if __name__ == "__main__":
    rc = RelayController()
    rc.open_device()
    print(" --- read_status_row: {}".format(rc.read_status_row()))
    print(" --- off all: {}".format(rc.off_all()))
    rc.off_all()
    for i in range(1, 5):
        print("Iteration {}".format(i))
        print("ON >1: {} \t- 2: {}".format(rc.on_relay(1), rc.read_relay_status(2)))
        sleep(0.3)
        print("1: {} \t- ON >2: {}".format(rc.read_relay_status(1), rc.on_relay(2)))
        sleep(0.3)
        print("OFF >1: {} \t- 2: {}".format(rc.off_relay(1), rc.read_relay_status(2)))
        sleep(0.3)
        print("1: {} \t- OFF >2: {}".format(rc.read_relay_status(1), rc.off_relay(2)))
        sleep(0.3)

    print("ON ALL: {}".format(rc.on_all()))
    sleep(1)
    print("OFF ALL: {}".format(rc.off_all()))
    print("END")
