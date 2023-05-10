# IoT-Smart-Waste-Segregation-System

The Smart Waste Segregation System is an IoT project that uses object detection and image classification to sort waste items into appropriate bins. This system detects waste items using a proximity sensor and captures an image of the item using the ESP-EYE camera. The captured image is then sent to the cloud, where an algorithm using the Faster RCNN technique classifies the item as either wet waste or dry waste. Once the waste item is classified, the system opens the appropriate bin for waste disposal using servo motors to control the bin lid. An LCD screen integrated with the system displays the waste category detected, providing real-time feedback to the user.

# Components
The system comprises several components that work together to achieve waste segregation. These components include:

- ESP32: Used as the main controller in the project, responsible for managing the inputs from various sensors and controlling the servo motor.
- ESP-EYE: Used to capture images of the trash that is being classified.
- Ultrasonic Sensor (Proximity Sensor): Used as a proximity sensor to detect the presence of trash in the vicinity.
- LCD Screen: Provides visual feedback to the user on the type of trash detected and the appropriate disposal method.
- Servo Motor: Used to control the opening and closing of the trash bin lid.
- Cloud Component: A backend code built using Flask and deployed on Azure.
- Faster RCNN Model: Used to classify trash based on its visual characteristics.

# Getting Started
To get started with the Smart Waste Segregation System, you will need to have the following components:

- ESP32
- ESP-EYE
- Ultrasonic Sensor (Proximity Sensor)
- LCD Screen
- Servo Motor
You will also need to clone this repository and follow the instructions in the "Installation" section to set up the project.

# Installation
To install the Smart Waste Segregation System, follow these steps:

1. Clone this repository to your local machine.
2. Set up the ESP32 and ESP-EYE.
3. Install the required Python packages by running pip install -r requirements.txt.
4. Start the Flask server by running python server.py.
5. Upload the main.ino sketch to your ESP32 board.
6. Connect the components.
7. Power on the system and start segregating waste!


# Conclusion
The Smart Waste Segregation System is an innovative solution for waste management that uses sensor networks, cloud computing, and object recognition techniques to detect the type of waste and optimize waste collection. The system promotes responsible waste disposal practices and encourages users to be more aware of the waste they generate. Future improvements could include adding sensors to track the level of waste in the bin and improving the object detection model to segregate other categories of waste.





