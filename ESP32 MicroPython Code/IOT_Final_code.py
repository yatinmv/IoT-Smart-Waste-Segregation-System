import machine
import time
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
import network
from time import sleep
import urequests
import ubinascii
import ujson

# Configure your WiFi credentials
WIFI_SSID = "S20wifi"
WIFI_PASSWORD = "zkir7279"
download_url = "http://192.168.233.154/jpg"
upload_url = "https://iotgroup9webapp.azurewebsites.net/upload"

# Define servo pins
SERVO1_PIN = 27
SERVO2_PIN = 14

# Define sensor pins
SENSOR1_PIN = 32
SENSOR2_PIN = 33

TRIGER_PIN=16
ECHO_PIN=17

 # Echo pin connected to GPIO 17
# Define LCD pins
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

# intialize Grabage Detection
adc_1 = machine.ADC(machine.Pin(SENSOR1_PIN))
adc_2 = machine.ADC(machine.Pin(SENSOR2_PIN))

# Initialize servo objects
servo_pin1=machine.Pin(SERVO1_PIN)
pwm1=machine.PWM(servo_pin1)
pwm1.freq(50)
servo_pin2=machine.Pin(SERVO2_PIN)
pwm2=machine.PWM(servo_pin2)
pwm2.freq(50)

# Initialize sensor pins
sensor1 = Pin(SENSOR1_PIN, Pin.IN)
sensor2 = Pin(SENSOR2_PIN, Pin.IN)
# Initialize Proximity Sensor pins
Trig_pin = machine.Pin(TRIGER_PIN, Pin.OUT) # Trig pin connected to GPIO 16
echo_pin = machine.Pin(ECHO_PIN, Pin.IN)
# Set the distance threshold in centimeters
distance_threshold = 50

# TO calulate the distance from proximity sensor
def measure_distance():
    # Trigger a pulse on the ultrasonic sensor
    Trig_pin.value(0)
    time.sleep_us(2)
    Trig_pin.value(1)
    time.sleep_us(10)
    Trig_pin.value(0)
    # Measure the duration of the echo pulse
    pulse_duration = 0
    while echo_pin.value() == 0:
        pulse_start = time.ticks_us()
        pulse_duration = time.ticks_diff(time.ticks_us(), pulse_start)
        if pulse_duration > 23200:  # Exit the loop after 1.5 ms
            return -1
    while echo_pin.value() == 1:
        pulse_end = time.ticks_us()
        pulse_duration = time.ticks_diff(pulse_end, pulse_start)
        if pulse_duration > 23200:  # Exit the loop after 1.5 ms
            return -1

    # Calculate the distance in centimeters
    distance = pulse_duration / 58.0

    return distance


i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000) #I2C for ESP32
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

# Connect to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
# Wait until connected to the WiFi network
while not wifi.isconnected():
    pass
# Print the IP address assigned to the ESP32 by the router
print("Connected to WiFi")
print("IP address:", wifi.ifconfig()[0])

host = "192.168.70.154"  
port = 8080  # Port to listen on 

while True:
    print("In")
    lcd.putstr("On")
    sleep(1)
    lcd.clear
    distance = measure_distance()
    print("distance",distance)
    lcd.clear()
    lcd.putstr("SmartGarbage")
    
    
    
    if distance > 0 and distance < distance_threshold:
        print("Distance: ", distance, "cm")
        lcd.clear()
        lcd.putstr("Welcome")
        sleep(1)
        count=0
        while count < 3:
           
                lcd.clear()
                lcd.putstr("Calling API")
                print("MakeApiCAll")
                response = urequests.get(download_url)
                image_data = response.content

                # Save the image data to a file on the ESP32
                with open('image.jpg', 'wb') as f:
                    f.write(image_data)
                print("Image_Done")

                # Encode the image data as a Base64-encoded string
                encoded_image = ubinascii.b2a_base64(image_data).decode('utf-8')

                # Create a JSON object containing the encoded image data
                json_data = {"image": encoded_image}

                # Call the second API to upload the image in JSON format
                response_2 = urequests.post(upload_url, json=json_data)
                print(response_2.text)
            

                # Print the response from the API
                
                # code to get image and call api
                # code to make api call and get results
                result=response_2.text

                if(result=='2'):
                    print("Result: ", result)
                    lcd.clear()
                    lcd.putstr("Recycle Waste")
                    analog_signal = adc_1.read()
                    print("analog_signal:",analog_signal)
                    print("type",type(analog_signal))
                    sleep(1)
                    if analog_signal == 4095 :
                        print("Inside")
                        lcd.clear()
                        lcd.putstr("Recycle")
                        sleep(1) 
                        for duty_cycle in range(25, 90, 2):
                            pwm1.duty(duty_cycle)
                            time.sleep_ms(100)
                        sleep(5)
                    # Rotate from maximum to minimum angle
                        for duty_cycle in range(90, 25, -2):
                            pwm1.duty(duty_cycle)
                            time.sleep_ms(100)
                        lcd.clear()
                        lcd.putstr("Thank You")
                        sleep(1)
                        lcd.clear
                        break
                    else:
                        lcd.clear
                        lcd.putstr("Bin Full")
                        sleep(2)
                        lcd.clear()
                        break

                if (result == '3'):
                    lcd.clear()
                    lcd.putstr("General Waste")
                    analog_signal = adc_2.read()
                    print(analog_signal)
                    distance = (analog_signal - 200) * 25 / 800
                    garbage_level = 25 - distance
                    print("Garbage level: {} cm".format(garbage_level))
                    if analog_signal == 4095 or analog_signal != 4095 :
                        for duty_cycle in range(25, 90, 2):
                            pwm2.duty(duty_cycle)
                            time.sleep_ms(100)
                        sleep(5)
                        # Rotate from maximum to minimum angle
                        for duty_cycle in range(90, 25, -2):
                            pwm2.duty(duty_cycle)
                            time.sleep_ms(100)
                        lcd.clear()
                        lcd.putstr("Thank You")
                        sleep(2)
                        lcd.clear
                        break
                    else:
                        lcd.clear()
                        lcd.putstr("Bin Full")
                        sleep(2)
                        lcd.clear()
                        break
                
                if  (result == '1'):
                    lcd.clear()
                    lcd.putstr("Please Wait Processing")
                    if count:
                        count=count+1
            
                
                    

pwm1.deinit()
pwm2.deinit()




