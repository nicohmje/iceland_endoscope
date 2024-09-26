from pydualsense import *
from dynamixel_sdk import *
import time
import os
import logging


logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger('RHU_ICELAND')

# Control table address
ADDR_PRO_TORQUE_ENABLE      = 24               # Control table address is different in each Dynamixel model
ADDR_PRO_LED_RED            = 25 
ADDR_PRO_GOAL_POSITION      = 30
ADDR_PRO_PRESENT_POSITION   = 36
ADDR_PRO_GOAL_VELOCITY      = 32

# Data Byte Length
LEN_PRO_LED_RED             = 1
LEN_PRO_GOAL_POSITION       = 2
LEN_PRO_PRESENT_POSITION    = 2

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL1_ID                     = 1                # Dynamixel#1 ID : 1
DXL2_ID                     = 2                # Dynamixel#1 ID : 2
BAUDRATE                    = 57600            # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'   # Check which port is being used on your controller
                                               # something like Windows: "COM1"   Linux: "/dev/ttyUSB0" macOS                                     : "/dev/tty.usbserial-*"


#DYNAMIXEL SETUP
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)


#DUALSENSE SETUP
dualsense = pydualsense()
dualsense.init()

#Open port to U2D2
if portHandler.openPort():
   logger.info("Succeeded to open the U2D2 port")
else:
   logger.error("Failed to open the U2D2 port")
   quit()

#Set the baudrate
if portHandler.setBaudRate(BAUDRATE):
   logger.info("Succeeded to change the baudrate")
else:
   logger.error("Failed to change the baudrate")
   quit()


os.system("clear")

print("------------ RHU ICELAND INTERNSHIP -------------")
print("|                                               |")
print("|                                               |")
print("|           Created by Nicolas Hammje           |")
print("|                                               |")
print("|                                               |")
print("|             www.nicolashammje.com             |")
print("|                                               |")
print("|              me@nicolashammje.com             |")
print("|                                               |")
print("|                                               |")
print("-------------------------------------------------")
print(" ")
print(" ")
print("Press X (cross) to start")
print("Use the right joystick to control the endoscope")
print("To exit, press O (circle)")


while True:
   if dualsense.state.circle:
      quit()
   if dualsense.state.cross:
      break
   time.sleep(0.1)


#LED on
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_LED_RED, 1)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_LED_RED, 1)

#Torque on
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_TORQUE_ENABLE, 1)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_TORQUE_ENABLE, 1)

while not dualsense.state.circle:
   try:
    R_jstck = [dualsense.last_states.RX,dualsense.last_states.RY]

    if abs(R_jstck[0]) < 10:
       R_jstck[0] = 0
    if abs(R_jstck[1]) < 10:
       R_jstck[1] = 0

    if R_jstck[0] < 0: #CW is [1024, 2047], CCW is [0, 1023]
       R_jstck[0] = 1024 + (-1 * R_jstck[0])
    if R_jstck[1] < 0:
       R_jstck[1] = 1024 + (-1 * R_jstck[1])

    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_GOAL_VELOCITY, R_jstck[0])
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_GOAL_VELOCITY, R_jstck[1])

   except:
       pass

   time.sleep(0.1)

#LED off
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_LED_RED, 0)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_LED_RED, 0)

#Torque off
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_TORQUE_ENABLE, 0)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_TORQUE_ENABLE, 0)

dualsense.close()