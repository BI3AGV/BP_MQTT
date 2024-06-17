import os
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import paho.mqtt.client as mqtt
import random

# MQTT Broker settings
broker = 'broker.emqx.io'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = '**********'


def publish_message(topic, message):
    client = mqtt.Client(client_id)
    client.username_pw_set(username, password)
    client.connect(broker, port)
    client.loop_start()

    result = client.publish(topic, message)
    status = result[0]

    if status == 0:
        print(f"消息发送到 {topic} 成功")
    else:
        print(f"消息发送到 {topic} 失败")

    client.loop_stop()
    client.disconnect()


def main(Call_index):
    if Call_index == '1' or Call_index == '2':
        if Call_index == '1':
            topic = "CRACBP@CQCALLING"
        if Call_index == '2':
            Call_sign = input("请输入呼叫呼号：")
            topic = f'CRACBP@{Call_sign}'
        message = input("请输入呼叫内容：")
        publish_message(topic, message)
    else:
        exit(1)


if __name__ == '__main__':
    while True:
        Call_index = input("请输入呼叫类型：\n1. CQ呼叫\n2. 对点呼叫\n3. 取消\n")
        main(Call_index)
