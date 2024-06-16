using System;
using System.Text.Json;
using System.Windows.Forms;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
namespace 远程寻呼发射台
{

    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            comboBox2.SelectedIndex = comboBox2.Items.IndexOf("对点呼叫");
        }

        private void button1_Click(object sender, EventArgs e)
        {
            MessageBody message = new MessageBody();
            message.callsign = textBox1.Text.ToUpper();
            message.message = richTextBox1.Text;
            button1.Text = "正在连接";
            MQTT_Client client = new MQTT_Client();
            bool isConnected = client.ConnectMQTT("broker.emqx.io", 1883, Guid.NewGuid().ToString(), "emqx", "public");
            if (isConnected)
            {
                button1.Text = "正在发送";
                if (comboBox2.SelectedItem.ToString() == "CQ呼叫")
                {
                    client.Publish("CRACBP@CQCALLING", message.message);
                }
                else
                {
                    client.Publish($"CRACBP@{message.callsign}", message.message);
                }
                button1.Text = "发送信息";
                MessageBox.Show("发送完成", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);

            }
            else
            {
                button1.Text = "发送信息";
                MessageBox.Show("连接失败", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void comboBox2_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (comboBox2.SelectedItem.ToString() == "CQ呼叫")
            {
                textBox1.Enabled = false;
            }
            else
            {
                textBox1.Enabled= true;
            }
        }
    }
    public class MessageBody
    {
        public string message { get; set; }
        public string callsign { get; set; }
    }
    public class MQTT_Client
    {
        MqttClient client;
        public bool ConnectMQTT(string broker, int port, string clientId, string username, string password)
        {
            client = new MqttClient(broker, port, false, MqttSslProtocols.None, null, null);
            client.Connect(clientId, username, password);
            if (client.IsConnected)
            {
                return true;
            }
            else
            {
                return false;
            }
            
        }

        public void Publish(string topic, string msg)
        {
            client.Publish(topic, System.Text.Encoding.UTF8.GetBytes(msg));
            Console.WriteLine("Send `{0}` to topic `{1}`", msg, topic);
        }

        public void Subscribe(string topic)
        {
            client.MqttMsgPublishReceived += client_MqttMsgPublishReceived;
            client.Subscribe(new string[] { topic }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_MOST_ONCE });
        }
        public void client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            string payload = System.Text.Encoding.Default.GetString(e.Message);
            Console.WriteLine("Received `{0}` from `{1}` topic", payload, e.Topic.ToString());
        }
    }
}
