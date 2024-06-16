# python3.8

import random
from paho.mqtt import client as mqtt_client
import os

callsign = "BI3AGV" #本人呼号，统一使用大写否则别人叫不到你
freq = "152650000"  #寻呼机频率，单位Hz
rate = "1200"  #数据速率，512/1200/2400
function = "3"  #默认功能位
addr = "0027741" #寻呼机地址
pocsagPath = "sudo /root/rpitx/pocsag" #指定rpitx/pocsag程序路径

charString = ""

broker = 'broker.emqx.io'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = '**********'

rpitxBusyFlag = False
def convertSpecialChar(c):
    # print(c)
    global charString
    if c in [0x22, 0x5c, 0x60, 0x24]:  # operate with " \ ` $ ,just add a "\"
        charString += chr(0x5c)
    elif c in [0x25]:  # operate with "%" eg. Error:"%Jar" Right:"%%Jar"
        charString += chr(0x25)
    elif len(charString) > 0:
        if charString[-1] == "\\":  # handle situation like "\\ar",the right should be "\\\ar"
            charString += chr(0x5c)


def sendPocsag(addr, message):
    global rpitxBusyFlag
    rpitxBusyFlag = True
    function = "1"
    if message == "":
        function = "0"
    rawString = list(message.encode('gb2312'))  # decode string with gb2312
    global charString
    charString = ""  # a string to storge converted bytes
    charset = 'gb2312'  # a status flag to determin when to convert chinese and ascii characters
    for c in rawString:

        if c >= 128:  # the MSB of a byte is 1 means the char is chinese
            if charset != 'gb2312':
                charString += "\x0e"
                charset = 'gb2312'
            convertSpecialChar(c & 0b01111111)
            charString += chr(c & 0b01111111)
            function = "3"
        else:
            if charset != 'ascii':
                charString += "\x0f"
                charset = 'ascii'
            convertSpecialChar(c)
            charString += chr(c)
    cmd = f"printf \"{addr}:{charString}\" | {pocsagPath} -f {freq} -r {rate} -b {function}"
    os.system(cmd)
    rpitxBusyFlag = False
    # print(cmd)

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.tls_set(ca_certs='./server-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global rpitxBusyFlag
        if not rpitxBusyFlag:
            sendPocsag(addr, msg.payload.decode())
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(f"CRACBP@{callsign}")
    client.subscribe(f"CRACBP@CQCALLING")
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
