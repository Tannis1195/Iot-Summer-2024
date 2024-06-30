# Tutorial on how to build an automatic plant watering system
Jonathan Lannerås (jl225yi) planned and carried out this project in June 2024.

This project is based on Raspberry Pi pico WH which reads the current soil moisture of two different plants and pumps water from a reservoir when the soil gets too dry. In addition to this the measures: Room temperature, Sunlight, Room Humidity, and current water level in the reservoir and uploads it to an Adafruit.io dashboard through Wifi. The system is powered by a 4000mAh power bank and a 1000mAh solar-rechargeable power bank, providing a total of approximately 5000mAh and recharging when exposed to sunlight. 

While the project was completed over three weeks with sporadic effort, an average person with a basic understanding of programming and electronics could likely complete it in approximately 10 hours.

## Objective
Are you the type of person who most often forgets that plants need water? Turns out that I am, and sadly one too many cactuses has not lived to tell the tale. In plain text I'm horrible at ensuring that my green friends get the care and attention they deserve (And desperately need), therefore, it was more than time to automate myself out of the equation and give the plants a fair chance. Although this project has not dwelled as deep into network security as I initially had hoped, it has given me a lot of new insights into the realm of home automation and also gained a fascination with the relative simplicity and cheapness of deploying small IoT projects for home improvements.

The way the system is intended to work is depicted in the flowchart below: 
<div align="center">
	<img src="https://github.com/Tannis1195/Iot-Summer-2024/blob/main/Material/FlowChart.jpg">
</div>

As seen in the flowchart the system consists of several parts and aims to both collect relevant data points, as well as continuously water the plants as needed. 

## Material
| Quantity | Link                                                                                            | Price (SEK) |
|----------|--------------------------------------------------------------------------------------------------|-------------|
| Numerous | Just a random mix-match of childhood legos                                                         | -           |
| 1 | Just a large container to use as the water reservoir                                                       | -           |
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
| 1        | [Battery Pack](https://www.electrokit.com/batterihallare-4xaa-box-brytare-sladd)                         | 29          |
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
The development of the project went both very well and very badly at the same time which was not all that surprising. Large portions of time went into redesigning the wiring of the system to make it as clean as possible (when looking at the wiring later, take note that it was much worse earlier). I also rebuilt the Lego structure approximately five times as the testing of the system proved more demanding than anticipated. Furthermore, I spent countless hours debugging and testing the code to ensure functionality, a major timewaster was the sporadic behavior of the "Lightsleep" function, after some digging I learned that "Deepsleep" was the way to go. Lastly, I had to redo quite a bit of work as I learned that having the pump and servo connected to the same power source was unwise when the pump started the servo started as well (For some reason), and after some digging, I learned that servos need to be run on a pretty consistent line without power fluctuation. I therefore tried to connect the servo to an external power pack but it did not wanna work therefore I hooked the pump up to the external instead and kept the servo on the 5V on the breadbord and this worked fine. But despite these hick-up most of the development rolled on quite nicely after I had gotten a costume to the technologies, case-in-point was the dashboard which was finalized an hour after I had created my Adafruit account.

### Wiring 
The wiring diagram of the project is displayed below:
![Wireing diagram](https://github.com/Tannis1195/Iot-Summer-2024/blob/main/Material/BreadBoard.png)
In real life, this wiring is a tad bit more chaotic but it is all wired the same. The reason for my wiring work closely resembling a birds nest is that I lacked appropriate lengthed wires which lead to a lot of suboptimal decisions, also the entire structure is built out of a miss match of old Lego I had laying around so the ability to plan and structure a sensible wiring approach was difficult. Thirdly, I'm also not that good at wiring so I'm certain that a more skilled practitioner who had access to the same supplies would have done more "presentable" work, but hey it works, and that's all that matters.
![Wireing](https://github.com/Tannis1195/Iot-Summer-2024/blob/main/Material/Plant%203.jpg)
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
In this project, all data is transmitted and stored in [Adafruit.io](https://io.adafruit.com/). My reasoning for choosing Adafruit instead of other options was based on two factors: Cost and ease of use. First of all, Adafruit is free to a limited extent and given the relatively low amounts of data I'm transmitting I was able to operate within these limits. Secondly, the ease of sending data to Adafruit using API made this a very attractive alternative as I'm familiar with how APIs work and was comfortable sending the data this way. Additionally, the way Adafruit has chosen to structure incoming data using different "feeds" which then can be used within dashboards was very straightforward and user-friendly, which was greatly appreciated on my part. It should, however, be noted that I found the free version of Adafruit to be quite limited in terms of data analytics and data representation but given the rather basic nature of the project, the need for either is close to non-existent. It would, however, have been neat to run a forecasting model on the data to determine when at what time the next refill of the water reservoir is bound to happen. This can of course be presumed offline by downloading the uploaded data from Adafruit and inputting it into analytical software such as **R** or **Python**. Additionally, using the free version of Adafruits services greatly impairs the scalability of the project as one is limited to 10 feeds in total, and currently the project is at 7 meaning that 3 additional plants could get added (Given that they are near the other plants) before one runs out of feeds.   <br />

Furthermore, my decision to use Adafruit in this project was also driven by the fact that I wanted to try out a cloud-based approach to IoT, and this project seemed like a good starting point. Why I deemed this project appropriate because of the fairly non-sense data I'm transmitting, for instance, I'm not transmitting live audio and video of my living room, because if this data leaks or gets intercepted the attacker will only gain some very detailed info about a mismanaged houseplant (and I can live with that).   
## The code

## Transmitting the data / connectivity
I use the Adafruit platform to both store and visualize my data, given that I'm monitoring plants the need for all too frequent updates was deemed unnecessary therefore transmittions occur once every hour. In this project, I chose to use Wifi as the wireless protocol. The reasoning behind this was that the project was launched in my private residence which has WiFi, therefore the use of more sophisticated methods seemed a bit extreme especially as there was no TTPs coverage nor any helium hotspots where I lived, which means I would have needed to invest in LoRaWAN equipment, which in all honesty seemed overkill for this deployment. I mentioned earlier that one key selling point for using Adafruit was the ability to send data using APIs, this is something that is achieved using HTTP/HTTPS as a transport protocol, in greater detail, I'm using HTTP post requests to deliver my data to the Adafruit server. One drawback of sending the data to Adafruit in this manner is that one can only send one data value at a time, meaning that one can not group all data and send it through post request instead you have to send one post request for each data point you want to upload, which consumes more energy. On the topic of energy, it should be noted that my decision to use WiFi had a fairly significant impact on the battery, however, as the WiFi is disconnected directly after the transmission is finalized thereby, power consumption is minimized.  <br />

Additionally, a decision taken by me was that the connection was only established one way, meaning that I sent data to Adafruit but Adafruit was unable to send data back. This impairs my ability to control anything on the pico over the internet using Adafruit, like watering a plant by pressing a button. Although this could be seen as a bit limiting it serves several purposes, first this is an automatic watering system and there should never occur a situation where I need to interact with the system over the internet. Secondly, if I was to be able to interact with the system over Adafruit I would need to be uplinked to Wifi constantly, which would drain far too much power. Thirdly, having a PICO constantly uplinked to the internet seems like an unnecessary risk as it is a possible point of attack against my network which I do not favor, I have on the other hand placed the PICO on its own VLAN as a security precaution but better safe than sorry.  
## Presenting the data
As previously mentioned, I'm using the Adafruit platform to both, store and visualize the data. The data is transmitted to Adafruit once every hour. Using Adafruit for this purpose is well suited for my project as Adafruit allows me to save 1KB in each feed for 30 days, the 30 days of storage is plenty given the needs of the project, however, the 1KB of storage is on the low side as all my data transitions are around 8 bytes each meaning that I have around five days of transmission before I reach the cap. However, as I'm not performing any data analytics on past data, this is not a major problem in this project. In the picture below I display how I have structured my Adafruit.Io dashboard:

I have structured the dashboard to quickly convey the data to the user. Firstly, for all measurements, I'm conveying the current state both numerically and graphically. Secondly, for the soil moisture, I'm also including a line graph highlighting how the soil moisture level has developed, giving a more detailed oversight on this data is obvious as the entire system is centered around ensuring the well-being and watering of the plants. Thirdly, I have also attached a terminal that displays the raw data that has been incorporated from the different feeds and when this data was uploaded to the dashboard, which provides the user with an understanding of the freshness of the data. Lastly, a terminal displaying information regarding watering events is also present in the dashboard, which informs a user regarding past watering events (Eg. if a plant has been watered or if a plant should have been watered but the reservoir was too low). All in all, I believe the dashboard provides adequate insight into the current situation of the plants, without drowning the user in data.  I mentioned earlier that I am not allowing Adafruit to send data back to the PICO meaning which explains why the dashboard lacks any interactive features, such as buttons or sliders, however, I do not feel like these would add much to the user experience in this case. 
## Finalizing the design
After many hours, more than I want to admit, I was able to finalize my build. I must admit that I have seen more aesthetically pleasing lego builds in my life, however, I'm more of a function-oriented person, and I'm quite satisfied with how it works. 

<div align="center">
	<img src="https://github.com/Tannis1195/Iot-Summer-2024/blob/main/Material/Plant%208.jpg">
</div>

<div align="center">
	<img src="https://github.com/Tannis1195/Iot-Summer-2024/blob/main/Material/Plant%2010.jpg">
</div>

<div align="center">
	<img src="https://github.com/Tannis1195/Iot-Summer-2024/blob/main/Material/Plant%206.jpg">
</div>

<div align="center">
	<img src="https://github.com/Tannis1195/Iot-Summer-2024/blob/main/Material/Plant%209.jpg">
</div>

<div align="center">
	<img src="https://github.com/Tannis1195/Iot-Summer-2024/blob/main/Material/Plant%207.jpg">
</div>

As I'm not exactly aware when the watering will take place I hard coded in that both plants needed water to be able to record the video below showcasing the system in action :) (The dedicated viewer can see that a little bit of water always escape in to the other plant, this is because the lego seal is not exactly submarine rated) 

[Watering Session Video](https://youtu.be/nqmDZlCsAVM)


Additionally, for me, this project is only viewed as an early version of an automated plant watering system and is something that I will continue to develop in the future. The currently assembled project is not home decor at its finest and is likely to be disabled soon as to reuse the parts in my V2! 
