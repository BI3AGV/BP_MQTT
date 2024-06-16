# BP_MQTT
基于rpitx和互联网MQTT通信的无线网络寻呼项目
* 如果对源码不感兴趣，请直接转到[Release](https://github.com/BI3AGV/BP_MQTT/Releases)页面
* bilibili: [@BI3AGV](https://space.bilibili.com/351393380)
# 使用方法
## 树莓派端
先修改7-11行的配置文件，根据自己实际情况填写
```Python
callsign = "BI3AGV" #本人呼号，统一使用大写否则别人叫不到你
freq = "152650000"  #寻呼机频率，单位Hz
rate = "1200"  #数据速率，512/1200/2400
function = "3"  #默认功能位
addr = "0027741" #寻呼机地址
```
直接在终端执行脚本即可。
```shell
python main.py
```
也可注册为systemd服务实现开机自启动
```shell
[Unit]
Description=rpitx
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
WorkingDirectory=/home/rpi
ExecStart=/usr/bin/python /your script path/main.py

[Install]
WantedBy=multi-user.target
```

