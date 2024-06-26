# Tutorial on how to build an automatic plant watering system
This project was planned and carried out by Jonathan Lannerås (jl225yi) in June 2024.

This project is based on Raspberry Pi pico WH which reads the current soil moisture of two different plants and pumps water from a reservoir when the soil gets too dry. In addition to this the measures: Room temperature, Sunlight, Room Humidity, and current water level in the reservoir and uploads it to an Adafruit.io dashboard through Wifi. The system is powered by a combination of a 4000mAh power bank and a 1000mAh solar-rechargeable power bank, providing a total of around 5000mAh and recharging when exposed to sunlight. 

While the project was completed over three weeks with sporadic effort, an average person with a basic understanding of programming and electronics could complete it in approximately 10 hours.

## Objective
Are you the type of person who most often forgets that plants need water? Turns out that I am, and sadly one too many cactuses has not lived to tell the tale. In plain text I'm horrible at ensuring that my green friends get the care and attention they deserve (And desperately need), therefore, it was more than time to automate myself out of the equation and give the plants a fair chance. Although this project has not dwelled as deep into network security as I initially had hoped, it has given me a lot of new insights into the realm of home automation and also gained a fascination with the relative simplicity and cheapness of deploying small IoT projects for home improvements.

## Material
- **Numerous Legos**<br />
  (Left unspecified as an exercise for the reader)
- **Wires**<br />
  (Enough to rule out an electrician as a career path)
- **1 Raspberry Pi Pico WH** <br />
  [Raspberry Pi Pico WH](https://www.electrokit.com/raspberry-pi-pico-wh), 109 SEK
- **1 Micro servo TS90 / SG90 1.2 kg**<br />
  [Micro servo TS90 / SG90 1.2 kg](https://www.electrokit.com/micro-servo-ts90-sg90-1.2kg), 49 SEK
- **1 DHT11 sensor**<br />
  [DHT11 Sensor](https://www.electrokit.com/digital-temperatur-och-fuktsensor-dht11), 49 SEK
- **1 Powerbank Keep-Alive Device**<br />
  [Powerbank Keep-Alive Device](https://www.electrokit.com/powerbank-keep-alive-device), 49 SEK
- **1 4xAA battery box**<br />
  [4xAA Battery Box](https://www.electrokit.com/batterihallare-4xaa-box-brytare-sladd), 29 SEK
- **2 Soil moisture sensors**<br />
  [Soil Moisture Sensor](https://www.electrokit.com/jordfuktighetssensor), 29 SEK/unit
  Total: 58 SEK
- **1 red led**<br />
  [Red LED](https://www.electrokit.com/led-5mm-rod-diffus-1500mcd), 5 SEK
- **1 photoresistor**<br />
  [Photoresistor](https://www.electrokit.com/fotomotstand-cds-4-7-kohm), 8 SEK
- **1 Ultrasonic distance sensor HCSR04**<br />
  [Ultrasonic Distance Sensor](https://www.electrokit.com/avstandsmatare-ultraljud-hc-sr04-2-400cm), 59 SEK
- **10 Kohm resistor**<br />
  [10 Kohm Resistor](https://www.electrokit.com/motstand-kolfilm-0.25w-1kohm-1k), 1 SEK
- **1 breadboard**<br />
  [Breadboard](https://www.electrokit.com/kopplingsdack-840-anslutningar), 69 SEK
- **1 relay**<br />
  (No link provided)
- **1 rechargeable powerbank**<br />
  [Rechargeable Powerbank](https://www.dormy.com/sv/varumarken/dormy/powerbank-solar-charger-14282044fik), 99 SEK
- **1 4000mAh powerbank**<br />
  (Unknown brand), ~100 SEK

The total cost of the entire project is difficult to accuratly estiamte as most of the used part are refurbished from old aurdino starter packs

## Computer setup
## Putting everything together
## Platform
## The code
## Transmitting the data / connectivity
## Presenting the data
## Finalizing the design
