# BP_MQTT
基于rpitx和互联网MQTT通信的无线网络寻呼项目
* 如果对源码不感兴趣，请直接转到[Release](https://github.com/BI3AGV/BP_MQTT/Releases)页面
* bilibili: [@BI3AGV](https://space.bilibili.com/351393380)
# 使用方法
## 树莓派端
先修改7-12行的配置文件，根据自己实际情况填写
```Python
callsign = "BI3AGV" #本人呼号，统一使用大写否则别人叫不到你
freq = "152650000"  #寻呼机频率，单位Hz
rate = "1200"  #数据速率，512/1200/2400
function = "3"  #默认功能位
addr = "0027741" #寻呼机地址
pocsagPath = "sudo /root/rpitx/pocsag" #指定rpitx/pocsag程序路径
```
然后直接在终端执行脚本即可。
```shell
python main.py
```
也可注册为systemd服务实现开机自启动
```shell
sudo nano /etc/systemd/system/rpitx.service 
```
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
```shell
systemctl enable rpitx
systemctl restart rpitx
```
## Windows端
转到[Release](https://github.com/BI3AGV/BP_MQTT/Releases)页面下载Windows可执行程序或下载源码自行编译（作者使用环境是Visual Studio 2022）
提供了两种呼叫模式
### 对点模式
需要指定被叫方呼号，统一使用大写，并要求被叫方树莓派已运行python脚本
### CQ呼叫模式
注意！！！
该模式无需指定呼号，在该模式下发送的信息可被全网所有部署脚本的设备接收，为了维护良好环境，请勿使用此功能交流业余无线电以外的话题！
### 使用方法
选择呼叫模式，填写呼号（如果使用对点模式），填写消息内容，点击发送即可！
* 如果填写空消息，对方会收到单音呼叫
* 如果发送纯ASCII字符，会自动将功能位置0b01,开启四行显示模式
  [实现显示自动切换功能需要对传呼机进行编程，功能位设置为"TANI"]

# 写在最后
## 希望大家共同维护好公网环境，文明用语，否则，我们的通联活动可能被取缔！
