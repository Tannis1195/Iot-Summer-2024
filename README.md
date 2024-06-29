# Tutorial on how to build an automatic plant watering system
Jonathan Lannerås (jl225yi) planned and carried out this project in June 2024.

This project is based on Raspberry Pi pico WH which reads the current soil moisture of two different plants and pumps water from a reservoir when the soil gets too dry. In addition to this the measures: Room temperature, Sunlight, Room Humidity, and current water level in the reservoir and uploads it to an Adafruit.io dashboard through Wifi. The system is powered by a 4000mAh power bank and a 1000mAh solar-rechargeable power bank, providing a total of approximately 5000mAh and recharging when exposed to sunlight. 

While the project was completed over three weeks with sporadic effort, an average person with a basic understanding of programming and electronics could likely complete it in approximately 10 hours.

## Objective
Are you the type of person who most often forgets that plants need water? Turns out that I am, and sadly one too many cactuses has not lived to tell the tale. In plain text I'm horrible at ensuring that my green friends get the care and attention they deserve (And desperately need), therefore, it was more than time to automate myself out of the equation and give the plants a fair chance. Although this project has not dwelled as deep into network security as I initially had hoped, it has given me a lot of new insights into the realm of home automation and also gained a fascination with the relative simplicity and cheapness of deploying small IoT projects for home improvements.

## Material
| Quantity | Link                                                                                            | Price (SEK) |
|----------|--------------------------------------------------------------------------------------------------|-------------|
| Numerous | Just a random mix-match of childhood legos                                                         | -           |
| 1        | [Male-male Wires](https://www.electrokit.com/kopplingstrad-byglar-for-kopplingsdack-mjuka-65st) | 39          |
| 1        | [Male-female Wires](https://www.electrokit.com/labsladd-1-pin-hane-hona-150mm-10-pack)          | 29          |
| 1        | [Raspberry Pi Pico WH](https://www.electrokit.com/raspberry-pi-pico-wh)                         | 109         |
| 1        | [Micro servo TS90 / SG90 1.2 kg](https://www.electrokit.com/micro-servo-ts90-sg90-1.2kg)        | 49          |
| 1        | [DHT11 Sensor](https://www.electrokit.com/digital-temperatur-och-fuktsensor-dht11)              | 49          |
| 1        | [Powerbank Keep-Alive Device](https://www.electrokit.com/powerbank-keep-alive-device)            | 49          |
| 2        | [Soil Moisture Sensor](https://www.electrokit.com/jordfuktighetssensor)                          | 58 (total)  |
| 1        | [Red LED](https://www.electrokit.com/led-5mm-rod-diffus-1500mcd)                                 | 5           |
| 1        | [Photoresistor](https://www.electrokit.com/fotomotstand-cds-4-7-kohm)                            | 8           |
| 1        | [Ultrasonic Distance Sensor](https://www.electrokit.com/avstandsmatare-ultraljud-hc-sr04-2-400cm) | 59          |
| 1        | [220 ohm Resistor](https://se.rs-online.com/web/p/through-hole-resistors/0131176?gb=s)                  | 1           |
| 1        | [Breadboard](https://www.electrokit.com/kopplingsdack-840-anslutningar)                          | 69          |
| 1        | [1000 mAh Rechargeable Powerbank](https://www.dormy.com/sv/varumarken/dormy/powerbank-solar-charger-14282044fik) | 99          |
| 1        | [Just a standard no brand 4000mAh powerbank](https://www.netonnet.se/art/hem-fritid/el-batterier/powerbank/on-powerbank-4000-mah-1a-blue/1032352.13728/) | ~50        |




The total cost of the entire project is difficult to accurately estimate as most of the used parts are refurbished from old Aurdino starter packs, but after finding most parts (or similar) I have calculated an estimated cost of **~700 Sek**

## Computer setup
During this project, all MicroPython code was written in the Thonny IDE. I ran Thonny on a Surface Pro 7, which was connected to the Raspberry Pi Pico via its micro USB port. Here’s how I set it up:

1. Downloaded and installed [Thonny](https://thonny.org/)
2. Hold down the BOOTSEL button (Located on the pico) while connecting the Pico to the computer (This engaged BOOTLOADER mode)
3. Open Thonny
4. Click **Run**
5. Click **Select interpreter**
6. In the dropdown list choose **MicroPython (Raspberry Pi Pico)**
7. Click **Install or update firmware** and follow the directions given in the popup window
8. Press **OK** and you are good to go!

Note that it is mandatory to test out the software in the following way: 
1. Start a new **.py** file in Thonny
2. Enter the code: <br />
`print ("Hello World")`
3. Ensure that you are using the MicroPython (Raspberry Pi Pico) as your interpreter 
4. Run the code by pressing **Run current script**
5. If all went according to plan, you should expect a nice treat in the terminal :) 

As ample guides exist on how to get Micropython installed on a Raspberry Pi Pico, I will not cover it in greater detail in this tutorial! I can, however, recommend [How to Setup a Raspberry Pi Pico and Code with Thonny](https://www.youtube.com/watch?v=_ouzuI_ZPLs), which provides an excellent and detailed walkthrough! 
## Putting everything together
![Wireing](https://github.com/Tannis1195/Iot-Summer-2024/blob/main/BreadBoard.png)
### Power consumption 
Sadly, I could not get an accurate and long-term reading of power consumption, as I lacked access to the correct equipment. I tried to measure the current and voltage of the PICO using a multimeter and then calculate power consumption through (W = A*V), however, I was unable to get an accurate current reading of the PICO. I also tried measuring the power consumption through a wall-outlet power meter, this particular meter measures in KWh, and due to the fairly low consumption of the pico it was unable to get a reading. However, if we run some quick guesstimate for a day:
| Device                         | Operation Description                                    | Duration       | Current (mA) | Consumption (mAh) |
|--------------------------------|----------------------------------------------------------|----------------|--------------|-------------------|
| Pico in Deepsleep              | Pico in deepsleep mode (60 minutes between each of 24 readings) | 23 hours       | 0.25         | 5.75              |
| Pico in action (With wifi on)  | Pico in operation (2-3 minutes for each of 24 instances) while wifi is on | 1 hour         | 45           | 225               |
| Servo switch                   | Servo switch operation (1 activation)                    | 2 seconds      | 500          | 0.278             |
| Water pump                     | Water pump operation (1 activation)                      | 1 second       | 100          | 0.03              |
| Ultrasonic sensor HCSR0415     | Ultrasonic sensor operation (24 readings of water level) | 6 seconds      | 15           | 0.025             |
| Powerbank Keep-Alive Device (active) | Powerbank wake-up pulse every 45 seconds                | 192 seconds    | 70           | 3.733             |
| Powerbank Keep-Alive Device (idle) | Powerbank idle state                                    | ~24 hours      | 1            | 23.947            |
| Soil moisture readings (per sensor) | Soil moisture sensor operation (24 readings per sensor) | 720 seconds    | 15           | 3 (per sensor)   |
| DHT11 sensor                   | DHT11 sensor operation (24 readings of temperature and humidity) | 2.4 seconds    | 2.5          | 0.002             |

If we sum these estimates up we land at around 300 (~265) mAh per day. Given that I have around 5000 mAh in powerbank (without recharge) this indicates around 19 days of usage before having to recharge, which from experience seems probable but optimistic.     


## Platform 
## The code
## Transmitting the data / connectivity
## Presenting the data
## Finalizing the design
