import sys
import pywinusb.hid as hid
from time import sleep


class Control():
    USB_CFG_VENDOR_ID = 0x16C0
    USB_CFG_DEVICE_ID = 0x05DF
    # the product id and the vendor id of the relay can be obtained in Device Manager.
    filter = None
    hid_device = None
    device = None
    report = None

    def __init__(self):
        self.get_Hid_USBRelay()

    def get_Hid_USBRelay(self):
        try:
            self.filter = hid.HidDeviceFilter(vendor_id=self.USB_CFG_VENDOR_ID, product_id=self.USB_CFG_DEVICE_ID)
            self.hid_device = self.filter.get_devices()
            self.device = self.hid_device[0]
            print("The  device connected is:",self.device)
            print(type(self.device))
        except:
            print("USB device Not Connected or Not Recognised")
            sys.exit()
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
    # for closing the device connection
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
        try:
            self.get_Hid_USBRelay()
            self.open_device()
        except:
            print("ERROR FINDING THE RELAY")

    def get_report(self):
        if not self.device.is_active():
            self.report = None

        for repo in self.device.find_output_reports() + self.device.find_feature_reports():
            self.report = repo

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

    # function for turning on a particular relay
    def on_relay(self, relay_number):
        if self.write_row_data(buffer=[0, 0xFF, relay_number, 0, 0, 0, 0, 0, 1]):
            # print(f'Turning On relay{relay_number}')
            return self.read_relay_status(relay_number)
        else:
            print("Cannot put ON relay number {}".format(relay_number))
            return False

    # function for turning off a particular relay
    def off_relay(self, relay_number):
        if self.write_row_data(buffer=[0, 0xFD, relay_number, 0, 0, 0, 0, 0, 1]):
            # print(f'Relay{relay_number} turned off')
            return self.read_relay_status(relay_number)
        else:
            print("Cannot put OFF relay number {}".format(relay_number))
            return False

    # function for reading the relay status
    def read_relay_status(self, relay_number):
        buffer = self.read_status_row()
        return relay_number & buffer[8]

    def off_all(self):
        if self.write_row_data(buffer=[0, 0xFC, 0, 0, 0, 0, 0, 0, 1]):
            # print(f'Turning OFF all relays')
            return self.read_relay_status(relay_number=3)
        else:
            print("Cannot put OFF relays")
            return False

    # function to turn all relays on
    def on_all(self):
        if self.write_row_data(buffer=[0, 0xFE, 0, 0, 0, 0, 0, 0, 1]):
            # print(f'Turning ON all relays')
            return self.read_relay_status(relay_number=3)
        else:
            print("Cannot put ON relays")
            return False

    # function to print relay status
    def print_relay_status(self, relay_number):
        if self.read_relay_status(relay_number):
            return (f"R{relay_number}-ON")
        else:
            return (f"R{relay_number}-OFF")
    def delay(self,t):
        sleep(t)
    def test_relay(self,relay_number):
        self.open_device()
        self.off_all()
        sleep(0.8)
        self.on_relay(relay_number)
        sleep(0.8)
        self.off_relay(relay_number)
        sleep(0.8)
        self.on_relay(relay_number)
        sleep(0.8)
        self.off_relay(relay_number)
if __name__ == "__main__":
    rc = Control()
    rc.open_device()
    print("STATUS ROW: {}".format(rc.read_status_row()))
    # Checking the working of the program
    # minimum time delay is necessary to notice the change in relay status.

    rc.off_all()
    sleep(0.5)
    print("Last row status",rc.last_row_status)
    rc.on_relay(1)
    print(rc.print_relay_status(1))
    print(rc.print_relay_status(2))
    print("******")
    sleep(3)
    rc.on_relay(2)
    print(rc.print_relay_status(1))
    print(rc.print_relay_status(2))
    print("******")
    sleep(3)
    rc.off_relay(1)
    print(rc.print_relay_status(1))
    print(rc.print_relay_status(2))
    print("******")
    sleep(3)
    rc.off_relay(2)
    print(rc.print_relay_status(1))
    print(rc.print_relay_status(2))
    print("******")
    sleep(3)
    rc.on_all()
    print(rc.print_relay_status(1))
    print(rc.print_relay_status(2))
    print("******")
    sleep(3)
    rc.off_all()
    print(rc.print_relay_status(1))
    print(rc.print_relay_status(2))
    print("******")
