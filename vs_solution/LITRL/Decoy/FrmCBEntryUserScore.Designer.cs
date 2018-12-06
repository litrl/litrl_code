namespace Decoy
{
    partial class FrmCBEntryUserScore
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.TxtCbCaption = new System.Windows.Forms.TextBox();
            this.PanelUserScores = new System.Windows.Forms.Panel();
            this.label8 = new System.Windows.Forms.Label();
            this.cboClickbaitDetectorAcc = new System.Windows.Forms.ComboBox();
            this.label12 = new System.Windows.Forms.Label();
            this.LblDetectorClickbait = new System.Windows.Forms.Label();
            this.LblDetectorNotClickbait = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.numObservedClickbait = new System.Windows.Forms.NumericUpDown();
            this.label6 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.numObservedNotClickbait = new System.Windows.Forms.NumericUpDown();
            this.BtnOK = new System.Windows.Forms.Button();
            this.PanelUserScores.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numObservedClickbait)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numObservedNotClickbait)).BeginInit();
            this.SuspendLayout();
            // 
            // TxtCbCaption
            // 
            this.TxtCbCaption.Dock = System.Windows.Forms.DockStyle.Top;
            this.TxtCbCaption.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.TxtCbCaption.Location = new System.Drawing.Point(0, 0);
            this.TxtCbCaption.Multiline = true;
            this.TxtCbCaption.Name = "TxtCbCaption";
            this.TxtCbCaption.ReadOnly = true;
            this.TxtCbCaption.Size = new System.Drawing.Size(574, 65);
            this.TxtCbCaption.TabIndex = 0;
            this.TxtCbCaption.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // PanelUserScores
            // 
            this.PanelUserScores.Controls.Add(this.label8);
            this.PanelUserScores.Controls.Add(this.cboClickbaitDetectorAcc);
            this.PanelUserScores.Controls.Add(this.label12);
            this.PanelUserScores.Controls.Add(this.LblDetectorClickbait);
            this.PanelUserScores.Controls.Add(this.LblDetectorNotClickbait);
            this.PanelUserScores.Controls.Add(this.label7);
            this.PanelUserScores.Controls.Add(this.numObservedClickbait);
            this.PanelUserScores.Controls.Add(this.label6);
            this.PanelUserScores.Controls.Add(this.label5);
            this.PanelUserScores.Controls.Add(this.numObservedNotClickbait);
            this.PanelUserScores.Dock = System.Windows.Forms.DockStyle.Top;
            this.PanelUserScores.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.PanelUserScores.Location = new System.Drawing.Point(0, 65);
            this.PanelUserScores.Name = "PanelUserScores";
            this.PanelUserScores.Size = new System.Drawing.Size(574, 108);
            this.PanelUserScores.TabIndex = 11;
            // 
            // label8
            // 
            this.label8.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.label8.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.label8.Font = new System.Drawing.Font("Arial", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label8.Location = new System.Drawing.Point(437, 35);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(111, 17);
            this.label8.TabIndex = 9;
            this.label8.Text = "Detector Accuracy";
            this.label8.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            // 
            // cboClickbaitDetectorAcc
            // 
            this.cboClickbaitDetectorAcc.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.cboClickbaitDetectorAcc.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cboClickbaitDetectorAcc.FormattingEnabled = true;
            this.cboClickbaitDetectorAcc.Items.AddRange(new object[] {
            "No opinion",
            "Very High",
            "High",
            "Moderate",
            "Low",
            "Poor"});
            this.cboClickbaitDetectorAcc.Location = new System.Drawing.Point(437, 55);
            this.cboClickbaitDetectorAcc.Name = "cboClickbaitDetectorAcc";
            this.cboClickbaitDetectorAcc.Size = new System.Drawing.Size(111, 28);
            this.cboClickbaitDetectorAcc.TabIndex = 8;
            // 
            // label12
            // 
            this.label12.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.label12.AutoSize = true;
            this.label12.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label12.Location = new System.Drawing.Point(276, 12);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(144, 20);
            this.label12.TabIndex = 7;
            this.label12.Text = "Detector prediction";
            // 
            // LblDetectorClickbait
            // 
            this.LblDetectorClickbait.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.LblDetectorClickbait.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.LblDetectorClickbait.Font = new System.Drawing.Font("Arial", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.LblDetectorClickbait.ForeColor = System.Drawing.Color.Red;
            this.LblDetectorClickbait.Location = new System.Drawing.Point(280, 67);
            this.LblDetectorClickbait.Name = "LblDetectorClickbait";
            this.LblDetectorClickbait.Size = new System.Drawing.Size(152, 26);
            this.LblDetectorClickbait.TabIndex = 6;
            this.LblDetectorClickbait.Text = "Processing...";
            this.LblDetectorClickbait.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // LblDetectorNotClickbait
            // 
            this.LblDetectorNotClickbait.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.LblDetectorNotClickbait.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.LblDetectorNotClickbait.Font = new System.Drawing.Font("Arial", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.LblDetectorNotClickbait.ForeColor = System.Drawing.Color.Blue;
            this.LblDetectorNotClickbait.Location = new System.Drawing.Point(280, 35);
            this.LblDetectorNotClickbait.Name = "LblDetectorNotClickbait";
            this.LblDetectorNotClickbait.Size = new System.Drawing.Size(152, 26);
            this.LblDetectorNotClickbait.TabIndex = 5;
            this.LblDetectorNotClickbait.Text = "Processing...";
            this.LblDetectorNotClickbait.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label7
            // 
            this.label7.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.Location = new System.Drawing.Point(150, 12);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(73, 20);
            this.label7.TabIndex = 4;
            this.label7.Text = "Observer";
            // 
            // numObservedClickbait
            // 
            this.numObservedClickbait.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.numObservedClickbait.Font = new System.Drawing.Font("Arial", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.numObservedClickbait.Location = new System.Drawing.Point(154, 67);
            this.numObservedClickbait.Name = "numObservedClickbait";
            this.numObservedClickbait.Size = new System.Drawing.Size(120, 26);
            this.numObservedClickbait.TabIndex = 3;
            this.numObservedClickbait.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // label6
            // 
            this.label6.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(5, 70);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(114, 20);
            this.label6.TabIndex = 2;
            this.label6.Text = "Clickbait Score";
            // 
            // label5
            // 
            this.label5.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(5, 38);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(143, 20);
            this.label5.TabIndex = 1;
            this.label5.Text = "Not Clickbait Score";
            // 
            // numObservedNotClickbait
            // 
            this.numObservedNotClickbait.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.numObservedNotClickbait.Font = new System.Drawing.Font("Arial", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.numObservedNotClickbait.Location = new System.Drawing.Point(154, 35);
            this.numObservedNotClickbait.Name = "numObservedNotClickbait";
            this.numObservedNotClickbait.Size = new System.Drawing.Size(120, 26);
            this.numObservedNotClickbait.TabIndex = 0;
            this.numObservedNotClickbait.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // BtnOK
            // 
            this.BtnOK.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.BtnOK.Location = new System.Drawing.Point(437, 179);
            this.BtnOK.Name = "BtnOK";
            this.BtnOK.Size = new System.Drawing.Size(133, 28);
            this.BtnOK.TabIndex = 12;
            this.BtnOK.Text = "OK";
            this.BtnOK.UseVisualStyleBackColor = true;
            this.BtnOK.Click += new System.EventHandler(this.BtnOK_Click);
            // 
            // FrmCBEntryUserScore
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.White;
            this.ClientSize = new System.Drawing.Size(574, 210);
            this.Controls.Add(this.BtnOK);
            this.Controls.Add(this.PanelUserScores);
            this.Controls.Add(this.TxtCbCaption);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "FrmCBEntryUserScore";
            this.Text = "Clickbait User Score";
            this.PanelUserScores.ResumeLayout(false);
            this.PanelUserScores.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numObservedClickbait)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numObservedNotClickbait)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        public System.Windows.Forms.TextBox TxtCbCaption;
        private System.Windows.Forms.Panel PanelUserScores;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.ComboBox cboClickbaitDetectorAcc;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.Label LblDetectorClickbait;
        private System.Windows.Forms.Label LblDetectorNotClickbait;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.NumericUpDown numObservedClickbait;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.NumericUpDown numObservedNotClickbait;
        private System.Windows.Forms.Button BtnOK;
    }
}