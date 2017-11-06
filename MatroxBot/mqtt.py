# mqtt.py
# Interface to the MQTT functionality
# Requires pip install paho-mqtt
import paho.mqtt.client as mqtt
import secrets
from singleton import Singleton
from utility import Utility

@Singleton
class ColorManager:

    @staticmethod
    def changeColor(targetColor):
        client = mqtt.Client("matroxbot")
        client.connect(secrets.MQTT_BROKER_ADDRESS)
        client.publish(secrets.MQTT_COLOR_TOPIC, targetColor)

    @staticmethod
    def changeColorHex(targetHex):
        value = targetHex.lstrip('#')
        util = Utility()
        hex = util.hex_to_rgb(value)
        strHex = str(hex[0]) + "," + str(hex[1]) + "," + str(hex[2])
        client = mqtt.Client("matroxbot")
        client.connect(secrets.MQTT_BROKER_ADDRESS)
        client.publish(secrets.MQTT_COLOR_TOPIC, strHex)

    @staticmethod
    def help():
        return "Use !colorchange to set the mood. Specify either a CSS3 color name of hex value after the command and watch the magic. !colorchange red || !colorchange #Ff0000"
