from machine import Pin, ADC, time_pulse_us,deepsleep
import time
import network
import urequests
import dht
import gc 

### ---------- Setting pins -------------------
pump_relay = Pin(21,Pin.OUT) # Pin which is connected to the water pump 
water_Switch_pin = Pin(0, Pin.OUT) # Pin which is connected to the Servo 
alarm_Pin = Pin(10,Pin.OUT) # Pin which connected to the alarm Led
humidity_Sensor = dht.DHT11(Pin(11)) # Pin which is connected to the DHT11 sensor
trig_SoundSensor = Pin(12,Pin.OUT) # Pin which is connected to the trig pin of the Ultrasonic Distance Sensor
echo_SoundSensor = Pin(13,Pin.IN)# Pin which is connected to the echo pin of the Ultrasonic Distance Sensor
sensorVCC = Pin(15, Pin.OUT) # Power to mostiure Sensors
light_Reader = ADC(Pin(26))# Pin which is connected to the Photoresistor
right_Soil_Sensor = ADC(Pin(27)) # Read value from mostiure Sensor in the right plant 
left_Soil_Sensor = ADC(Pin(28)) # Read value from mostiure Sensor in the left plant 

### ---------- Support functions -------------------
# This function is used to clean an array of outliers (Bad values)
def outlier_Deleter(value_Array):
    value_Array = sorted(value_Array)
    n = len(value_Array)
    q1_Pos = (n + 1) / 4
    q3_Pos = 3 * (n + 1) / 4
    # This function is used to calculate the quartile values
    def qurtile_calc(pos):
        lower = value_Array[int(pos)-1]
        upper = value_Array[int(pos)]
        return lower + (pos%1)*(upper - lower)
    q1 = qurtile_calc(q1_Pos) # quartile 1
    q3 = qurtile_calc(q3_Pos)# quartile 1
    iqr = q3-q1# inter quartile range
    lower_Bound = q1 - (1.5*iqr)
    upper_Bound = q3 + (1.5*iqr)
    filtered_array = list(filter(lambda x:lower_Bound<=x<=upper_Bound,value_Array))
    return filtered_array
### ---------- Uploading to Adafruit functions -------------------
# This function is used to connect the pico to wifi
def connect_To_Wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    connection_wait = 10 # How long im allowing the connection to take
    connection_Fails = 0 # Index used to keep track of how many times connection failed
    max_Connection_Tries = 5 # How many failes I allow
    while connection_Fails < max_Connection_Tries: # Runs till the max number of connection attemps has been reached
        initiation_Start_Time = time.time()
        wlan.connect("ENTER YOUR ssid HERE","ENTER YOUR password HERE") # Please create a .py file called secrets and place these credentials there and retrive them this way: secrets["ssid"],secrets["password"]
        while not wlan.isconnected(): # Runs till connected to Wifi
            if time.time() - initiation_Start_Time > connection_wait: # If connection is not made in a timly manner
                connection_Fails +=1
                print("Connection failed :(")
                for _ in range(20): # Runs a blinking led to indicate failiure
                    alarm_Pin.value(1)
                    time.sleep(0.5)
                    alarm_Pin.value(0)
                    time.sleep(0.5)
                break #Exit While loop
            time.sleep(0.5)
            
        if wlan.isconnected(): # If a connection was made
            break
        
    return wlan.isconnected(),wlan # 
# This function is used to send data to a Adafruit stream
def send_To_Adafruit(data, feed):
    adafruit_API_URL = "https://io.adafruit.com/api/v2/{}/feeds/{}/data".format("INSERT YOUR aio_username HERE", feed) # Sets API link | Please create a .py file called secrets and place these credentials there and retrive them this way: secrets["aio_username"]
    headers = {"Content-Type":"application/json","X-AIO-Key":"INSERT YOUR aio_key here"} # Defining headers of API post | Please create a .py file called secrets and place these credentials there and retrive them this way: secrets["aio_key"]
    data = {"value":data} # Creating Json
    try:
        adafruit_Response = urequests.post(adafruit_API_URL, json = data, headers = headers) # HTTP post requests
        if adafruit_Response.status_code == 200: # If data transmission was sucessful 
            print ("Mission control: Data handover was a success")
        else: # If not 
            print("Huston we had a problem: ", adafruit_Respons.status_code)
            print(adafruit_Respons.text)
    
    except Exception as error: # If an error occure 
            print ("Huston we had a RequestException error: ",error)
    gc.collect() #Delete nonsense data to preserve memory!
### ---------- Soil functions -------------------
# Function used to transform the Raw moisture value into a precentage between 0-100
def moisture_Precent(curr_Val):  
    dry_Soil_Value = 65535 # Max value, The high seas 
    wet_Soil_Value = 0 # Min value, Desert 
    percent = (curr_Val - dry_Soil_Value) * (100) / (wet_Soil_Value - dry_Soil_Value)
    return round(percent, 2)

# Function used to collect the moisture value in each plant
def read_Sensor_Average(samples, plant_Reader, plantVCC):
    total = []
    return_Array = []
    for _ in range(samples): # Run samples time
        plantVCC.value(1)  
        time.sleep(0.005)
        single_Mesure_Array = []
        for sensor in plant_Reader: # Loop over all plants
            single_Mesure_Array.append(sensor.read_u16()) # Create array [Value plant1, Value plant2,...]
        total.append(single_Mesure_Array) # Create array [[Value plant1, Value plant2,...],[Value plant1, Value plant2,...]]
        plantVCC.value(0)  
        time.sleep(0.005)
    for i in range(len(plant_Reader)):# Loop over the number of plants 
        clean_Value_array = outlier_Deleter([row[i] for row in total]) # Take out the values associate with the plant and clean the array from outliers
        moisture = moisture_Precent(sum(clean_Value_array) / len(clean_Value_array)) # Send the average value of the raw values to calculate the precentage between 0-100
        return_Array.append(moisture) # Append mosture level to retrun array [Moist_Level_Plant_1, Moist_Level_Plant_2,...]
    gc.collect()  # Delete nonsense data, Keep memory free!
    return return_Array

# Function used to collect the mean moisture value in each plant
def plant_Monitor (plantVCC,sensorArray):
    sampleSize = 50
    moistureData = []
    return_Array = []
    for _ in range (sampleSize): #As the mesurmement of soil is noizy I collect 50 moisture value per plant
        plant_moist_Value = read_Sensor_Average(sampleSize,sensorArray, plantVCC) # Collect moisture value
        moistureData.append(plant_moist_Value)
  
    for i in range(len(sensorArray)):
        moisture_Plant = outlier_Deleter([row[i] for row in moistureData]) # Take out the values associate with the plant and clean the array from outliers
        moisture = sum(moisture_Plant) / len(moisture_Plant) # Calculate the mean value of the clean array
        return_Array.append(moisture) # Append mosture level to retrun array [Mean_Moist_Level_Plant_1, Mean_Moist_Level_Plant_2,...]
    gc.collect()  # Delete nonsense data, Keep memory free!
    return return_Array


### ---------- Watering functions -------------------
# This function is used to measure how much water there is in the water tank
def water_Level_Reader(sample_Size):
    result_Array = []
    for i in range(sample_Size):
        trig_SoundSensor.value(0)
        time.sleep(0.005)
        trig_SoundSensor.value(1)
        time.sleep(0.00001)
        trig_SoundSensor.value(0)
        pulse_time = time_pulse_us(echo_SoundSensor, 1, 500*2*30) #Records the pulse time of the Ultrasonic Distance Sensor
        if not (pulse_time < 0): # If the pulse time is more than 0 (Remove noise) 
            result_Array.append(pulse_time)
        
    clean_result_Array = outlier_Deleter(result_Array) # Clean the pulse data from outliers 
    result_Array = None # Remove result array to save on memory
    average_pulse_time = sum(clean_result_Array)/len(clean_result_Array) # Calculate the average pulse time
    cms = (average_pulse_time / 2) / 29.1 # Convert pulse time to centimeters (Distance between sensor and water level)
    water_volume = -0.56 * cms + 9.4 # Convert centimerters to Water quant in DL (My tank is a slight cone shape therefor the need of a function) 
    gc.collect()  # Delete nonsense data, Keep memory free!
    return water_volume

# This function controls the water pump 
def water_distribution (plant):
    set_switch(plant) # Sets the switch so the water flows to the correct plant
    time.sleep(2) # Ensure switch has happen
    pump_relay.value(1)
    time.sleep (1) # Pump is on for 1s which is plenty of water
    pump_relay.value(0)
    time.sleep(2) # Ensure all water is through

# This function is used to control the servo which regulates to which plant the water flows
def set_switch(direction):
    # As I ran out of ADC pins i had to run the servo manually instead of the normal way, not ideal but it gets the work done
    hz = 50 # The Hz the server operates at
    puls_Period = 1/hz #  The puls period at 50Hz is 20ms(0.02s)
    if direction == "left":
        servo_pos = 20 # Not going to 0 as to make sure im not over-shooting and damaging the servo (I'm not sure of the precision of controlling the servo this way)
    else: # If the right plant is the one to be watered
        servo_pos = 160 # Not going to 180 as to make sure im not over-shooting and damaging the servo (I'm not sure of the precision of controlling the servo this way)
    pulse = 0.0005 + (servo_pos/180)*0.0019 # 0.5ms for 0 degree, 1.9ms + 0.5ms = 2.4ms for 180 degree
    for _ in range(hz): ## the servo operaters at 50Hz a second
        water_Switch_pin.value(1)
        time.sleep(pulse) 
        water_Switch_pin.value(0)
        time.sleep(puls_Period-pulse)
    gc.collect()  # Delete nonsense data, Keep memory free!
 
# This function is used to determine if the plants need watering and if so waters them. 
def watering_Of_Plants(plants):
    water_Level  = water_Level_Reader(50) # Determines current water level in water tank
    watering_Activity = []
    for plant_Info in plants: # Loops over all plants
        plant = plant_Info[0] # Retrives what plant (Left plant, right plant, etc) 
        plant_Moist_Level = plant_Info[1] # Retrives the measured moisture level of the plant
        threshold_Value = plant_Info[2] # Retrives moisture threshold value of said plant 
        safe_Water_Level = 1 # Running the pump without water is wasteful and dry running can damage the pump
        
        if plant_Moist_Level < threshold_Value: # If the plant needs to be watered
            if water_Level>safe_Water_Level: # Is there enough water in the tank?
                water_distribution(plant) # Water the plant
                watering_Activity.append("The " + plant + " plant was watered")
                water_Level  = water_Level_Reader(50) # Redetermine current water level in water tank
            else: 
                watering_Activity.append("Unable to water the " + plant + " plant, due to low water")
    gc.collect()  # Delete nonsense data, Keep memory free!
    return water_Level,watering_Activity

### ---------- Additional data functions -------------------
# This function is used to calculate the current light level
def light_Tracker(sample_Size):
    result_Array = []
    for i in range(sample_Size):
        result_Array.append(light_Reader.read_u16()) #Collects sample_Size light readings
    clean_result_Array = outlier_Deleter(result_Array) # Cleans the collected readings from outliers
    result_Array = None #Removes old array to save on memory
    curr_Val = sum(clean_result_Array)/len(clean_result_Array) # Calculate mean
    
    dark_Value  = 100 # The darkest value I have recorded in my room was 300
    sun_Value = 50000 # The brights value I have recorded in my room was 45000
    percent = (curr_Val - dark_Value) * (100) / (sun_Value - dark_Value) # Convert to a scale 0-100
    gc.collect()  # Delete nonsense data, Keep memory free!
    return round(percent,2)
# This function is used to calculate both the humidity and Tempature 
def humidity_Temp_Tracker(sample_Size):
    result_Temp_Array = []
    result_Humidity_Array = []
    for i in range(sample_Size):
        humidity_Sensor.measure() # The DTH11 collects both Tempature and Humidity data
        result_Temp_Array.append(humidity_Sensor.temperature())
        result_Humidity_Array.append(humidity_Sensor.humidity())
        
    clean_result_Temp_Array = outlier_Deleter(result_Temp_Array) # Cleans the collected readings from outliers
    clean_result_Humidity_Array = outlier_Deleter(result_Humidity_Array)# Cleans the collected readings from outliers
    result_Temp_Array = None #Removes old array to save on memory
    result_Humidity_Array = None #Removes old array to save on memory
    
    curr_Val_Temp = sum(clean_result_Temp_Array)/len(clean_result_Temp_Array) # Calculate mean
    curr_Val_Humidity = sum(clean_result_Humidity_Array)/len(clean_result_Humidity_Array) # Calculate mean
    gc.collect()  # Delete nonsense data, Keep memory free!
    return [round(curr_Val_Temp,2),round(curr_Val_Humidity,2)]
    
### ---------- Main function -------------------
def main():
    while True:
        alarm_Pin.value(0) # Sets alarm pin to off 
        moist = plant_Monitor (sensorVCC,[left_Soil_Sensor,right_Soil_Sensor]) # Calculate the moisture level of the plants
        plant_Left_Moist_Level = moist[0]
        plant_Right_Moist_Level = moist[1]
        plants =[
            ["left",plant_Right_Moist_Level,50],
            ["right",plant_Left_Moist_Level,50]
        ]
        water_Level, watering = watering_Of_Plants(plants) # Calculates the water level in the water tank and investigates if the plants need to be watered   
        humidity_Temp = humidity_Temp_Tracker(25) # Calculates both Tempature and Humidity data
        temperature = humidity_Temp[0]
        humidity_Level = humidity_Temp[1]
        sun_Light = light_Tracker(50) # Calculates the current light level
        print("Moisture level of the Left plant: ", plant_Left_Moist_Level, "\n",
              "Moisture level of the Right plant: ", plant_Right_Moist_Level, "\n",
              "Temperature: ", temperature, "\n",
              "Humidity: ", humidity_Level, "\n",
              "Light Level: ", sun_Light, "\n",
              "Water Level: ", water_Level, "\n",
              "Watering events: ", watering)
         
        connected, wlan = connect_To_Wifi() # Try to connect to Wifi
        if connected:
            #Send data to Adafruit
            send_To_Adafruit(plant_Left_Moist_Level, "moisture-plant-1")
            plant_Left_Moist_Level=None #Delete from memory
            send_To_Adafruit(plant_Right_Moist_Level, "moisture-plant-2")
            plant_Right_Moist_Level=None #Delete from memory
            send_To_Adafruit(water_Level, "water-tank")
            water_Level=None #Delete from memory
            send_To_Adafruit(temperature, "temperature")
            temperature=None #Delete from memory
            send_To_Adafruit(humidity_Level, "humidity")
            humidity_Level=None #Delete from memory
            send_To_Adafruit(sun_Light, "sun-light")
            sun_Light=None #Delete from memory
            if len(watering) != 0: # If a watering event has been recorded
                for i in watering:
                    send_To_Adafruit(i,"watering-event")
                watering=None #Delete from memory
            wlan.disconnect() # Disconnect from WIFI
            time.sleep(1)
            if wlan.isconnected(): #If unable to disconnect
                print ("Disconnect has failed :(, It left me no choice")
                machine.reset() # Hard reset, im not allowing the pico to keep wifi on under any circumstance
            else:
                print("Great success, we have disconnected!")
                
        else: # If unable to connect to Wifi
           print("Connection was never an option :(, Data not delivered") # Data do not get uploaded or stored (Main objective is to ensure plant safety not Dashbord uplink)
           alarm_Pin.value(1) # Turn on alarm pin to indicate error
               
        deepsleep(60*60*1000)#Puts the pico into deepsleep for 60min
        
main() # Runs main function and start the program :D

