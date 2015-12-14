####Falcon

Falcon is a high precision cable-suspended camera motion control system. It offers the room-spanning motion of a drone-mounted camera, without the inherent danger and noise. Carrying a Ronin gimbal and Panasonic GH4 camera, this mechatronic system allows the user to capture stunning footage.

To learn more about Falcon, visit the [Falcon](http://poe.olin.edu/2015/falcon/) site.

##### A Quick Note: Bluetooth Configuration
To configure your linux machine to connect to Falcon's bluetooth-enabled nodes, please refer to the following steps.

1. Get the bluetooth manager packages using `sudo apt-get install bluetooth bluez-utils bluez-firmware`
2. Once installed, run `service bluetooth status` to make sure the bluetooth service is running
3. Also check to find your bluetooth card/dongle `lsusb | grep Bluetooth`. This will result in something like Bus 001 Device 005: ID 0a12:0001 Cambridge Silicon Radio, Ltd Bluetooth Dongle (HCI mode), which describes your local device.
4. Make sure all of the nodes are powered and running
5. Run `hcitool scan` to verify the bluetooth MAC addresses of all of the nodes 
6. Connect to each of the nodes initially by running `sudo bluetooth-agent <PIN of the device> <MAC address of the device>`. The default PIN for RN-41 modules is 1234.
7. From the base directory of the `falcon` repository, run `sudo cp config/rfcomm.conf /etc/bluetooth/rfcomm.conf` to copy the correct bluetooth configuration config file to your computer's bluetooth configuration directory. This configuration file will facilitate automatic bluetooth connection. 
8. Finally, run `sudo service bluetooth restart`, and everything should work!
