import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import paho.mqtt.client as mqtt
import random

# MQTT Broker settings
broker = 'broker.emqx.io'
port = 1883
topic2 = "CRACBP@CQCALLING"
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = '**********'


class PagingTransmitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("寻呼发射台")
        self.create_widgets()

    def create_widgets(self):
        self.label_call_type = ttk.Label(self.root, text="呼叫类型选择")
        self.label_call_type.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.combo_call_type = ttk.Combobox(self.root, values=["CQ呼叫", "对点呼叫"], width=23)
        self.combo_call_type.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        self.combo_call_type.current(0)

        self.label_call_sign = ttk.Label(self.root, text="对方呼号")
        self.label_call_sign.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.entry_call_sign = ttk.Entry(self.root, width=25)
        self.entry_call_sign.grid(row=1, column=1, padx=10, pady=5, sticky="e")

        self.label_message_content = ttk.Label(self.root, text="消息内容")
        self.label_message_content.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.text_message_content = ttk.Text(self.root, wrap="word", height=10, width=25)
        self.text_message_content.grid(row=2, column=1, padx=10, pady=5, sticky="e")

        self.button_send = ttk.Button(self.root, text="发送消息", command=self.send_message)
        self.button_send.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def send_message(self):
        call_type = self.combo_call_type.get()
        call_sign = self.entry_call_sign.get()
        message_content = self.text_message_content.get("1.0", tk.END).strip()

        if call_type == "对点呼叫" and not call_sign:
            messagebox.showwarning("输入错误", "请填写对方呼号")
            return

        topic = f'CRACBP@{self.entry_call_sign.get()}' if call_type == "对点呼叫" else topic2
        self.publish_message(topic, message_content)

    def publish_message(self, topic, message):
        client = mqtt.Client(client_id)
        client.username_pw_set(username, password)
        client.connect(broker, port)
        client.loop_start()

        result = client.publish(topic, message)
        status = result[0]

        if status == 0:
            messagebox.showinfo("发送成功", f"消息发送到 {topic}")
        else:
            messagebox.showerror("发送失败", f"消息发送到 {topic} 失败")

        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    root = ttk.Window()
    app = PagingTransmitterApp(root)
    root.mainloop()
