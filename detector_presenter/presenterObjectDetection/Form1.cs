using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using OpenCvSharp;
using System.Net.Sockets;
using System.IO.Ports;
using System.IO;
using System.Net;
using System.Threading;
using System.Runtime.Serialization.Formatters.Binary;
using OpenCvSharp.CPlusPlus;
using Size = System.Drawing.Size;

namespace presenterObjectDetection
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            init_system();

        }

        DateTime start_time;

        Label[] lbObj = new Label[6];
        Label[] lbPrice = new Label[6];
        Label[] lbQuantity = new Label[6];



        void init_system()
        {
            lbObj[0] = object1;
            lbObj[1] = object2;
            lbObj[2] = object3;
            lbObj[3] = object4;
            lbObj[4] = object5;
            lbObj[5] = object6;

            lbPrice[0] = price1;
            lbPrice[1] = price2;
            lbPrice[2] = price3;
            lbPrice[3] = price4;
            lbPrice[4] = price5;
            lbPrice[5] = price6;

            lbQuantity[0] = quantity1;
            lbQuantity[1] = quantity2;
            lbQuantity[2] = quantity3;
            lbQuantity[3] = quantity4;
            lbQuantity[4] = quantity5;
            lbQuantity[5] = quantity6;

            Console.WriteLine("start");
            timer_clock.Interval = 1000;
            timer_clock.Enabled = true;
            timer_clock.Start();

            start_time = DateTime.Now;
        }


        private void timer1_Tick(object sender, EventArgs e)
        {
            var use_time = (DateTime.Now - start_time).ToString(@"\.h\:mm\:ss");

            HandleInvoke(() =>
            {
                useTime.Text = use_time;
            });

        }

        void HandleInvoke(Action action)
        {
            if (InvokeRequired)
            {
                Invoke(action);
            }
            else
            {
                action();
            }
        }

        VideoCapture video;
        public Mat frame = new Mat();
        TcpListener Server;
        TcpClient Client;
        StreamReader Reader;
        StreamWriter Writer;
        NetworkStream stream;
        Thread ReceiveThread;
        bool Connected;

        private void Form1_Load(object sd, EventArgs e)
        {
            String IP = "141.223.140.53"; // 접속 할 서버 아이피를 입력
            //String IP = "127.0.0.1"; // 접속 할 서버 아이피를 입력
            int port = 8888; // 포트
            Client = new TcpClient();
            Client.Connect(IP, port);
            stream = Client.GetStream();
            Connected = true;
            Reader = new StreamReader(stream);
            Writer = new StreamWriter(stream);
            Writer.Write("4;MONITOR");
            Writer.Flush();
            ReceiveThread = new Thread(new ThreadStart(Receive));
            ReceiveThread.Start();

            object1.Text = "";
            object2.Text = "";
            object3.Text = "";
            object4.Text = "";
            object5.Text = "";
            object6.Text = "";

            quantity1.Text = "";
            quantity2.Text = "";
            quantity3.Text = "";
            quantity4.Text = "";
            quantity5.Text = "";
            quantity6.Text = "";

            price1.Text = "";
            price2.Text = "";
            price3.Text = "";
            price4.Text = "";
            price5.Text = "";
            price6.Text = "";

            priceTotal.Text = "0";



            try
            {
                //video = new VideoCapture(1);
                //video.FrameWidth = 800;
                //video.FrameHeight = 600;
            }
            catch
            {
            }
        }

        byte[] buff = new byte[100000];
        byte[] buff2 = new byte[100];



        BinaryFormatter formatter;
        int max_num_labels = 0;


        //{
        //        {"buttercookie", "버터쿠키", 2980, 1},
        //        {"sinlamyeon", "신라면", 950, 1},
        //        {"orangejuice", "미닛메이드 망고주스", 1880, 1},
        //        {"jjapageti", "짜파게티", 950, 1},
        //        {"oreooz", "오레오오즈", 7880, 1},
        //        {"montes_alpha_wine", "몬테스 알파 샤도네이", 40000, 1}
        //}

        public class product_info
        {
            public string name;
            public int price;
            public int quantity;
        }

        string[] label_list =
        {
            "buttercookie",
            "sinlamyeon",
            "orangejuice",
            "jjapageti",
            "oreooz",
            "montes_alpha_wine"
        };

        string[] name_list =
        {
            "버터쿠키",
            "신라면",
            "미닛메이드 망고주스",
            "짜파게티",
            "오레오오즈",
            "몬테스 알파 샤도네이"
        };

        int[] price_list =
        {
            2980,
            950,
            1880,
            950,
            7880,
            40000
        };

        int[] quantity_list =
        {
            1,
            1,
            1,
            1,
            1,
            1
        };

        private void Receive() // 서버로 부터 값 받아오기
        {
            formatter = new BinaryFormatter();
            BinaryWriter binWriter = new BinaryWriter(stream);
            BinaryReader binReader =
            new BinaryReader(binWriter.BaseStream);

            Dictionary<string, product_info> dic = new Dictionary<string, product_info>();

            product_info[] prod;
            prod = new product_info[6];

            for (int i = 0; i < 6; i++)
            {
                prod[i] = new product_info();
            }

            for (int i = 0; i < 6; i++)
            {
                prod[i].name = name_list[i];
                prod[i].price = price_list[i];
                prod[i].quantity = quantity_list[i];

                dic.Add(label_list[i], prod[i]);
            }

            while (Connected)
            {
                //Thread.Sleep(1);
                if (stream.CanRead)
                {
                    try
                    {
                        Array.Clear(buff, 0, buff.Length);
                        int tempInt = stream.Read(buff, 0, 100000);

                        Writer.Write('A');
                        Writer.Flush();

                        Console.WriteLine(tempInt.ToString());

                        Image x = (Bitmap)((new ImageConverter()).ConvertFrom(buff));

                        Array.Clear(buff2, 0, buff2.Length);
                        int tempInt2 = stream.Read(buff2, 0, 100);

                        Writer.Write('B');
                        Writer.Flush();

                        //if (tempInt > 0)
                        //{
                        Console.WriteLine(tempInt2.ToString());





                        //var myMat = convertToMat(buff);
                        ////byte[] byte_array = Encoding.GetEncoding("UTF-8").GetBytes(buff);
                        HandleInvoke(() =>
                        {
                            pbi1.Image = (Bitmap)x.Clone();

                            string recv_label_string = ByteToString(buff2);
                            Console.WriteLine(recv_label_string);
                            //recv_label_string = recv_label_string.Remove(0, 1);
                            string[] check_label_string = recv_label_string.Split(']');

                            string[] recv_labels = check_label_string[0].Split(',');



                            int num_labels = recv_labels.Length;

                            if (recv_labels[0].Length != 1)
                            {
                                try
                                {
                                    for (int i = 0; i < num_labels; i++)
                                    {

                                        recv_labels[i] = recv_labels[i].Remove(0, 2);
                                        recv_labels[i] = recv_labels[i].Remove(recv_labels[i].Length - 1, 1);
                                        Console.WriteLine(recv_labels[i]);
                                    }

                                    if (num_labels >= max_num_labels)
                                    {
                                        max_num_labels = num_labels;
                                        Size resize = new Size(480, 300);
                                        Bitmap resizeImage = new Bitmap(pbi1.Image, resize);
                                        pbi2.Image = resizeImage;

                                        try
                                        {
                                            int totalPrice_int = 0;
                                            for (int i = 0; i < num_labels; i++)
                                            {
                                                lbObj[i].Text = dic[recv_labels[i]].name;
                                                lbQuantity[i].Text = dic[recv_labels[i]].quantity.ToString();
                                                lbPrice[i].Text = dic[recv_labels[i]].price.ToString();

                                                totalPrice_int += dic[recv_labels[i]].quantity * dic[recv_labels[i]].price;
                                            }

                                            priceTotal.Text = totalPrice_int.ToString();
                                        }
                                        catch
                                        {

                                        }
                                    }
                                }
                                catch
                                {

                                }
                                
                            }
                        });
                    }
                    catch
                    {

                    }
                    

                }

            }

        }

        private string ByteToString(byte[] strByte)
        {
            string str = Encoding.Default.GetString(strByte);
            return str;
        }

        private void btReset_Click(object sender, EventArgs e)
        {
            start_time = DateTime.Now;
            if (pbi1.Image != null)
            {
                pbi1.Image.Dispose();
                pbi1.Image = null;
            }

            if (pbi2.Image != null)
            {
                pbi2.Image.Dispose();
                pbi2.Image = null;
            }

            max_num_labels = 0;

            object1.Text = "";
            object2.Text = "";
            object3.Text = "";
            object4.Text = "";
            object5.Text = "";
            object6.Text = "";

            quantity1.Text = "";
            quantity2.Text = "";
            quantity3.Text = "";
            quantity4.Text = "";
            quantity5.Text = "";
            quantity6.Text = "";

            price1.Text = "";
            price2.Text = "";
            price3.Text = "";
            price4.Text = "";
            price5.Text = "";
            price6.Text = "";

            priceTotal.Text = "0";

        }
    }
}