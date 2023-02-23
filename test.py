import USB_RELAY

con=USB_RELAY.Control()
# #for checking the relay functioning
# con.test_relay(1) 
#operation of relay
con.open_device()
con.on_all()
con.delay(0.3)             #time delay is important to notice the change in status of relay
con.off_all()

# #similarly the following functions can be used to operate the relay.
# con.open_device() 
# con.close_device()      
# con.delay(time)                     #to give time delay. input in seconds
# con.read_relay_status(relay_number=)         #to check the statys of a particular relay
# con.on_all()                    #to turn on and off all relays
# con.off_all()
# con.on_relay(relay_number=)                  #to turn on a specific relay
# con.off_relay(relay_number=)                   #to turn off a specific relay
# con.test_relay(relay_number=)                #to check the working of a relay