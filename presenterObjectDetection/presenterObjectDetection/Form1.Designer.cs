namespace presenterObjectDetection
{
    partial class Form1
    {
        /// <summary>
        /// 필수 디자이너 변수입니다.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 사용 중인 모든 리소스를 정리합니다.
        /// </summary>
        /// <param name="disposing">관리되는 리소스를 삭제해야 하면 true이고, 그렇지 않으면 false입니다.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form 디자이너에서 생성한 코드

        /// <summary>
        /// 디자이너 지원에 필요한 메서드입니다. 
        /// 이 메서드의 내용을 코드 편집기로 수정하지 마세요.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.gbList = new System.Windows.Forms.GroupBox();
            this.price6 = new System.Windows.Forms.Label();
            this.quantity6 = new System.Windows.Forms.Label();
            this.object6 = new System.Windows.Forms.Label();
            this.priceTotal = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.price5 = new System.Windows.Forms.Label();
            this.price4 = new System.Windows.Forms.Label();
            this.price3 = new System.Windows.Forms.Label();
            this.price2 = new System.Windows.Forms.Label();
            this.price1 = new System.Windows.Forms.Label();
            this.quantity5 = new System.Windows.Forms.Label();
            this.quantity4 = new System.Windows.Forms.Label();
            this.quantity3 = new System.Windows.Forms.Label();
            this.quantity2 = new System.Windows.Forms.Label();
            this.quantity1 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.object5 = new System.Windows.Forms.Label();
            this.object4 = new System.Windows.Forms.Label();
            this.object3 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.object2 = new System.Windows.Forms.Label();
            this.object1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.gbUse = new System.Windows.Forms.GroupBox();
            this.useTime = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.timer_clock = new System.Windows.Forms.Timer(this.components);
            this.pbi1 = new OpenCvSharp.UserInterface.PictureBoxIpl();
            this.pbi2 = new OpenCvSharp.UserInterface.PictureBoxIpl();
            this.btReset = new System.Windows.Forms.Button();
            this.gbList.SuspendLayout();
            this.gbUse.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pbi1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pbi2)).BeginInit();
            this.SuspendLayout();
            // 
            // gbList
            // 
            this.gbList.Controls.Add(this.price6);
            this.gbList.Controls.Add(this.quantity6);
            this.gbList.Controls.Add(this.object6);
            this.gbList.Controls.Add(this.priceTotal);
            this.gbList.Controls.Add(this.label4);
            this.gbList.Controls.Add(this.price5);
            this.gbList.Controls.Add(this.price4);
            this.gbList.Controls.Add(this.price3);
            this.gbList.Controls.Add(this.price2);
            this.gbList.Controls.Add(this.price1);
            this.gbList.Controls.Add(this.quantity5);
            this.gbList.Controls.Add(this.quantity4);
            this.gbList.Controls.Add(this.quantity3);
            this.gbList.Controls.Add(this.quantity2);
            this.gbList.Controls.Add(this.quantity1);
            this.gbList.Controls.Add(this.label3);
            this.gbList.Controls.Add(this.object5);
            this.gbList.Controls.Add(this.object4);
            this.gbList.Controls.Add(this.object3);
            this.gbList.Controls.Add(this.label5);
            this.gbList.Controls.Add(this.object2);
            this.gbList.Controls.Add(this.object1);
            this.gbList.Controls.Add(this.label2);
            this.gbList.Controls.Add(this.label1);
            this.gbList.Font = new System.Drawing.Font("나눔고딕 ExtraBold", 15F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.gbList.ForeColor = System.Drawing.Color.White;
            this.gbList.Location = new System.Drawing.Point(660, 329);
            this.gbList.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.gbList.Name = "gbList";
            this.gbList.Padding = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.gbList.Size = new System.Drawing.Size(480, 339);
            this.gbList.TabIndex = 2;
            this.gbList.TabStop = false;
            this.gbList.Text = "구입 목록";
            // 
            // price6
            // 
            this.price6.AccessibleName = "";
            this.price6.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.price6.Location = new System.Drawing.Point(355, 256);
            this.price6.Name = "price6";
            this.price6.Size = new System.Drawing.Size(77, 25);
            this.price6.TabIndex = 23;
            this.price6.Text = "0";
            this.price6.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // quantity6
            // 
            this.quantity6.AccessibleName = "";
            this.quantity6.AutoSize = true;
            this.quantity6.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.quantity6.Location = new System.Drawing.Point(259, 256);
            this.quantity6.Name = "quantity6";
            this.quantity6.Size = new System.Drawing.Size(25, 25);
            this.quantity6.TabIndex = 22;
            this.quantity6.Text = "0";
            // 
            // object6
            // 
            this.object6.AccessibleName = "";
            this.object6.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.object6.Location = new System.Drawing.Point(7, 256);
            this.object6.Name = "object6";
            this.object6.Size = new System.Drawing.Size(166, 25);
            this.object6.TabIndex = 21;
            this.object6.Text = "버터쿠키";
            this.object6.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // priceTotal
            // 
            this.priceTotal.AccessibleName = "";
            this.priceTotal.Font = new System.Drawing.Font("나눔고딕", 13.2F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.priceTotal.Location = new System.Drawing.Point(336, 290);
            this.priceTotal.Name = "priceTotal";
            this.priceTotal.Size = new System.Drawing.Size(83, 25);
            this.priceTotal.TabIndex = 20;
            this.priceTotal.Text = "0";
            this.priceTotal.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("나눔고딕 ExtraBold", 13.2F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.label4.Location = new System.Drawing.Point(425, 290);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(33, 25);
            this.label4.TabIndex = 19;
            this.label4.Text = "원";
            // 
            // price5
            // 
            this.price5.AccessibleName = "";
            this.price5.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.price5.Location = new System.Drawing.Point(355, 222);
            this.price5.Name = "price5";
            this.price5.Size = new System.Drawing.Size(77, 25);
            this.price5.TabIndex = 18;
            this.price5.Text = "0";
            this.price5.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // price4
            // 
            this.price4.AccessibleName = "";
            this.price4.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.price4.Location = new System.Drawing.Point(355, 188);
            this.price4.Name = "price4";
            this.price4.Size = new System.Drawing.Size(77, 25);
            this.price4.TabIndex = 17;
            this.price4.Text = "0";
            this.price4.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // price3
            // 
            this.price3.AccessibleName = "";
            this.price3.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.price3.Location = new System.Drawing.Point(355, 154);
            this.price3.Name = "price3";
            this.price3.Size = new System.Drawing.Size(77, 25);
            this.price3.TabIndex = 16;
            this.price3.Text = "0";
            this.price3.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // price2
            // 
            this.price2.AccessibleName = "";
            this.price2.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.price2.Location = new System.Drawing.Point(355, 120);
            this.price2.Name = "price2";
            this.price2.Size = new System.Drawing.Size(77, 25);
            this.price2.TabIndex = 15;
            this.price2.Text = "0";
            this.price2.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // price1
            // 
            this.price1.AccessibleName = "";
            this.price1.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.price1.Location = new System.Drawing.Point(355, 86);
            this.price1.Name = "price1";
            this.price1.RightToLeft = System.Windows.Forms.RightToLeft.No;
            this.price1.Size = new System.Drawing.Size(77, 25);
            this.price1.TabIndex = 14;
            this.price1.Text = "0";
            this.price1.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // quantity5
            // 
            this.quantity5.AccessibleName = "";
            this.quantity5.AutoSize = true;
            this.quantity5.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.quantity5.Location = new System.Drawing.Point(259, 222);
            this.quantity5.Name = "quantity5";
            this.quantity5.Size = new System.Drawing.Size(25, 25);
            this.quantity5.TabIndex = 13;
            this.quantity5.Text = "0";
            // 
            // quantity4
            // 
            this.quantity4.AccessibleName = "";
            this.quantity4.AutoSize = true;
            this.quantity4.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.quantity4.Location = new System.Drawing.Point(259, 188);
            this.quantity4.Name = "quantity4";
            this.quantity4.Size = new System.Drawing.Size(25, 25);
            this.quantity4.TabIndex = 12;
            this.quantity4.Text = "0";
            // 
            // quantity3
            // 
            this.quantity3.AccessibleName = "";
            this.quantity3.AutoSize = true;
            this.quantity3.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.quantity3.Location = new System.Drawing.Point(259, 154);
            this.quantity3.Name = "quantity3";
            this.quantity3.Size = new System.Drawing.Size(25, 25);
            this.quantity3.TabIndex = 11;
            this.quantity3.Text = "0";
            // 
            // quantity2
            // 
            this.quantity2.AccessibleName = "";
            this.quantity2.AutoSize = true;
            this.quantity2.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.quantity2.Location = new System.Drawing.Point(259, 120);
            this.quantity2.Name = "quantity2";
            this.quantity2.Size = new System.Drawing.Size(25, 25);
            this.quantity2.TabIndex = 10;
            this.quantity2.Text = "0";
            // 
            // quantity1
            // 
            this.quantity1.AccessibleName = "";
            this.quantity1.AutoSize = true;
            this.quantity1.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.quantity1.Location = new System.Drawing.Point(259, 86);
            this.quantity1.Name = "quantity1";
            this.quantity1.Size = new System.Drawing.Size(25, 25);
            this.quantity1.TabIndex = 9;
            this.quantity1.Text = "0";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("나눔고딕", 15F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.label3.Location = new System.Drawing.Point(235, 290);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(68, 29);
            this.label3.TabIndex = 8;
            this.label3.Text = "총 액";
            // 
            // object5
            // 
            this.object5.AccessibleName = "";
            this.object5.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.object5.Location = new System.Drawing.Point(7, 222);
            this.object5.Name = "object5";
            this.object5.Size = new System.Drawing.Size(166, 25);
            this.object5.TabIndex = 7;
            this.object5.Text = "버터쿠키";
            this.object5.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // object4
            // 
            this.object4.AccessibleName = "";
            this.object4.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.object4.Location = new System.Drawing.Point(7, 188);
            this.object4.Name = "object4";
            this.object4.Size = new System.Drawing.Size(166, 25);
            this.object4.TabIndex = 6;
            this.object4.Text = "버터쿠키";
            this.object4.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // object3
            // 
            this.object3.AccessibleName = "";
            this.object3.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.object3.Location = new System.Drawing.Point(7, 154);
            this.object3.Name = "object3";
            this.object3.Size = new System.Drawing.Size(166, 25);
            this.object3.TabIndex = 5;
            this.object3.Text = "버터쿠키";
            this.object3.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("나눔고딕", 15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.label5.Location = new System.Drawing.Point(75, 43);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(85, 29);
            this.label5.TabIndex = 4;
            this.label5.Text = "상품명";
            // 
            // object2
            // 
            this.object2.AccessibleName = "lb1";
            this.object2.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.object2.Location = new System.Drawing.Point(7, 120);
            this.object2.Name = "object2";
            this.object2.Size = new System.Drawing.Size(166, 25);
            this.object2.TabIndex = 3;
            this.object2.Text = "버터쿠키";
            this.object2.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // object1
            // 
            this.object1.AccessibleName = "";
            this.object1.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.object1.Location = new System.Drawing.Point(7, 86);
            this.object1.Name = "object1";
            this.object1.Size = new System.Drawing.Size(166, 25);
            this.object1.TabIndex = 2;
            this.object1.Text = "버터쿠키";
            this.object1.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("나눔고딕", 15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.label2.Location = new System.Drawing.Point(235, 43);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(68, 29);
            this.label2.TabIndex = 1;
            this.label2.Text = "수 량";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("나눔고딕", 15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.label1.Location = new System.Drawing.Point(373, 43);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(68, 29);
            this.label1.TabIndex = 0;
            this.label1.Text = "가 격";
            // 
            // gbUse
            // 
            this.gbUse.Controls.Add(this.btReset);
            this.gbUse.Controls.Add(this.useTime);
            this.gbUse.Controls.Add(this.label7);
            this.gbUse.Controls.Add(this.label6);
            this.gbUse.Controls.Add(this.label8);
            this.gbUse.Font = new System.Drawing.Font("나눔고딕 ExtraBold", 15F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.gbUse.ForeColor = System.Drawing.Color.White;
            this.gbUse.Location = new System.Drawing.Point(13, 12);
            this.gbUse.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.gbUse.Name = "gbUse";
            this.gbUse.Padding = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.gbUse.Size = new System.Drawing.Size(640, 170);
            this.gbUse.TabIndex = 3;
            this.gbUse.TabStop = false;
            this.gbUse.Text = "사용 정보";
            // 
            // useTime
            // 
            this.useTime.AccessibleName = "";
            this.useTime.AutoSize = true;
            this.useTime.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.useTime.Location = new System.Drawing.Point(299, 94);
            this.useTime.Name = "useTime";
            this.useTime.Size = new System.Drawing.Size(25, 25);
            this.useTime.TabIndex = 23;
            this.useTime.Text = "0";
            this.useTime.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // label7
            // 
            this.label7.AccessibleName = "";
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("나눔고딕", 13F);
            this.label7.Location = new System.Drawing.Point(207, 49);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(428, 25);
            this.label7.TabIndex = 21;
            this.label7.Text = "T77829-2287987Q (롯데마트 포항 지곡점)";
            this.label7.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("나눔고딕", 15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.label6.Location = new System.Drawing.Point(31, 91);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(109, 29);
            this.label6.TabIndex = 22;
            this.label6.Text = "사용시간";
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Font = new System.Drawing.Font("나눔고딕", 15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.label8.Location = new System.Drawing.Point(31, 45);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(85, 29);
            this.label8.TabIndex = 21;
            this.label8.Text = "카트ID";
            // 
            // timer_clock
            // 
            this.timer_clock.Interval = 1000;
            this.timer_clock.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // pbi1
            // 
            this.pbi1.Location = new System.Drawing.Point(13, 188);
            this.pbi1.Name = "pbi1";
            this.pbi1.Size = new System.Drawing.Size(640, 480);
            this.pbi1.TabIndex = 4;
            this.pbi1.TabStop = false;
            // 
            // pbi2
            // 
            this.pbi2.Location = new System.Drawing.Point(660, 23);
            this.pbi2.Name = "pbi2";
            this.pbi2.Size = new System.Drawing.Size(480, 300);
            this.pbi2.TabIndex = 5;
            this.pbi2.TabStop = false;
            // 
            // btReset
            // 
            this.btReset.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.btReset.Font = new System.Drawing.Font("나눔고딕 Light", 10.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.btReset.Location = new System.Drawing.Point(558, 126);
            this.btReset.Name = "btReset";
            this.btReset.Size = new System.Drawing.Size(75, 38);
            this.btReset.TabIndex = 24;
            this.btReset.Text = "RST";
            this.btReset.UseVisualStyleBackColor = true;
            this.btReset.Click += new System.EventHandler(this.btReset_Click);
            // 
            // Form1
            // 
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.None;
            this.AutoSize = true;
            this.BackColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.ClientSize = new System.Drawing.Size(1152, 687);
            this.Controls.Add(this.pbi2);
            this.Controls.Add(this.pbi1);
            this.Controls.Add(this.gbUse);
            this.Controls.Add(this.gbList);
            this.Font = new System.Drawing.Font("휴먼둥근헤드라인", 15F);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
            this.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.Name = "Form1";
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Hide;
            this.Text = "ASCAR 계산기";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.gbList.ResumeLayout(false);
            this.gbList.PerformLayout();
            this.gbUse.ResumeLayout(false);
            this.gbUse.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pbi1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pbi2)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion
        private System.Windows.Forms.GroupBox gbList;
        private System.Windows.Forms.GroupBox gbUse;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label object2;
        private System.Windows.Forms.Label object1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label object5;
        private System.Windows.Forms.Label object4;
        private System.Windows.Forms.Label object3;
        public System.Windows.Forms.Label price5;
        public System.Windows.Forms.Label price4;
        public System.Windows.Forms.Label price3;
        public System.Windows.Forms.Label price2;
        public System.Windows.Forms.Label price1;
        public System.Windows.Forms.Label quantity5;
        public System.Windows.Forms.Label quantity4;
        public System.Windows.Forms.Label quantity3;
        public System.Windows.Forms.Label quantity2;
        public System.Windows.Forms.Label quantity1;
        private System.Windows.Forms.Label label3;
        public System.Windows.Forms.Label priceTotal;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label useTime;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Timer timer_clock;
        public OpenCvSharp.UserInterface.PictureBoxIpl pbi1;
        public OpenCvSharp.UserInterface.PictureBoxIpl pbi2;
        public System.Windows.Forms.Label price6;
        public System.Windows.Forms.Label quantity6;
        private System.Windows.Forms.Label object6;
        private System.Windows.Forms.Button btReset;
    }
}

