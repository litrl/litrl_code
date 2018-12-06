namespace Decoy
{
    partial class FrmSelectHtmlTags
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
            this.BtnOK = new System.Windows.Forms.Button();
            this.LstHtmlTags = new System.Windows.Forms.ListBox();
            this.label1 = new System.Windows.Forms.Label();
            this.numSatireLength = new System.Windows.Forms.NumericUpDown();
            this.label3 = new System.Windows.Forms.Label();
            this.numFalsificationLength = new System.Windows.Forms.NumericUpDown();
            this.GrpFals = new System.Windows.Forms.GroupBox();
            this.GrpSatire = new System.Windows.Forms.GroupBox();
            this.label5 = new System.Windows.Forms.Label();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.TxtHTMLID = new System.Windows.Forms.TextBox();
            this.TxtHTMLClass = new System.Windows.Forms.TextBox();
            ((System.ComponentModel.ISupportInitialize)(this.numSatireLength)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numFalsificationLength)).BeginInit();
            this.GrpFals.SuspendLayout();
            this.GrpSatire.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.SuspendLayout();
            // 
            // BtnOK
            // 
            this.BtnOK.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.BtnOK.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.BtnOK.Location = new System.Drawing.Point(455, 316);
            this.BtnOK.Margin = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.BtnOK.Name = "BtnOK";
            this.BtnOK.Size = new System.Drawing.Size(108, 34);
            this.BtnOK.TabIndex = 3;
            this.BtnOK.Text = "OK";
            this.BtnOK.UseVisualStyleBackColor = true;
            this.BtnOK.Click += new System.EventHandler(this.BtnOK_Click);
            // 
            // LstHtmlTags
            // 
            this.LstHtmlTags.Font = new System.Drawing.Font("Arial", 18F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.LstHtmlTags.FormattingEnabled = true;
            this.LstHtmlTags.ItemHeight = 27;
            this.LstHtmlTags.Items.AddRange(new object[] {
            "a",
            "div",
            "em",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "header",
            "i",
            "li",
            "ol",
            "p",
            "pre",
            "span",
            "strong",
            "time",
            "title",
            "track",
            "u",
            "ul"});
            this.LstHtmlTags.Location = new System.Drawing.Point(12, 37);
            this.LstHtmlTags.Margin = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.LstHtmlTags.Name = "LstHtmlTags";
            this.LstHtmlTags.ScrollAlwaysVisible = true;
            this.LstHtmlTags.SelectionMode = System.Windows.Forms.SelectionMode.MultiSimple;
            this.LstHtmlTags.Size = new System.Drawing.Size(193, 274);
            this.LstHtmlTags.Sorted = true;
            this.LstHtmlTags.TabIndex = 2;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(12, 9);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(510, 24);
            this.label1.TabIndex = 4;
            this.label1.Text = "Select the HTML tags to pull text content from (per detector):";
            // 
            // numSatireLength
            // 
            this.numSatireLength.Font = new System.Drawing.Font("Arial", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.numSatireLength.Location = new System.Drawing.Point(104, 36);
            this.numSatireLength.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.numSatireLength.Name = "numSatireLength";
            this.numSatireLength.Size = new System.Drawing.Size(127, 26);
            this.numSatireLength.TabIndex = 5;
            this.numSatireLength.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(6, 35);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(75, 20);
            this.label3.TabIndex = 8;
            this.label3.Text = "0 - ignore";
            // 
            // numFalsificationLength
            // 
            this.numFalsificationLength.Font = new System.Drawing.Font("Arial", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.numFalsificationLength.Location = new System.Drawing.Point(104, 34);
            this.numFalsificationLength.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.numFalsificationLength.Name = "numFalsificationLength";
            this.numFalsificationLength.Size = new System.Drawing.Size(127, 26);
            this.numFalsificationLength.TabIndex = 7;
            this.numFalsificationLength.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // GrpFals
            // 
            this.GrpFals.Controls.Add(this.numFalsificationLength);
            this.GrpFals.Controls.Add(this.label3);
            this.GrpFals.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.GrpFals.ForeColor = System.Drawing.Color.White;
            this.GrpFals.Location = new System.Drawing.Point(231, 211);
            this.GrpFals.Name = "GrpFals";
            this.GrpFals.Size = new System.Drawing.Size(334, 92);
            this.GrpFals.TabIndex = 10;
            this.GrpFals.TabStop = false;
            this.GrpFals.Text = "Falsification tag text content character length";
            this.GrpFals.Visible = false;
            // 
            // GrpSatire
            // 
            this.GrpSatire.Controls.Add(this.label5);
            this.GrpSatire.Controls.Add(this.numSatireLength);
            this.GrpSatire.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.GrpSatire.ForeColor = System.Drawing.Color.White;
            this.GrpSatire.Location = new System.Drawing.Point(231, 217);
            this.GrpSatire.Name = "GrpSatire";
            this.GrpSatire.Size = new System.Drawing.Size(332, 92);
            this.GrpSatire.TabIndex = 11;
            this.GrpSatire.TabStop = false;
            this.GrpSatire.Text = "Satire tag text content character length";
            this.GrpSatire.Visible = false;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(6, 37);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(75, 20);
            this.label5.TabIndex = 8;
            this.label5.Text = "0 - ignore";
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.TxtHTMLID);
            this.groupBox2.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBox2.ForeColor = System.Drawing.Color.White;
            this.groupBox2.Location = new System.Drawing.Point(231, 51);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(332, 77);
            this.groupBox2.TabIndex = 12;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "By ID #";
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.TxtHTMLClass);
            this.groupBox3.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBox3.ForeColor = System.Drawing.Color.White;
            this.groupBox3.Location = new System.Drawing.Point(231, 134);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(332, 77);
            this.groupBox3.TabIndex = 13;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "By Class .";
            // 
            // TxtHTMLID
            // 
            this.TxtHTMLID.Location = new System.Drawing.Point(6, 28);
            this.TxtHTMLID.Name = "TxtHTMLID";
            this.TxtHTMLID.Size = new System.Drawing.Size(320, 29);
            this.TxtHTMLID.TabIndex = 0;
            // 
            // TxtHTMLClass
            // 
            this.TxtHTMLClass.Location = new System.Drawing.Point(6, 28);
            this.TxtHTMLClass.Name = "TxtHTMLClass";
            this.TxtHTMLClass.Size = new System.Drawing.Size(320, 29);
            this.TxtHTMLClass.TabIndex = 1;
            // 
            // FrmSelectHtmlTags
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.Indigo;
            this.ClientSize = new System.Drawing.Size(577, 358);
            this.Controls.Add(this.groupBox3);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.GrpFals);
            this.Controls.Add(this.GrpSatire);
            this.Controls.Add(this.BtnOK);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.LstHtmlTags);
            this.ForeColor = System.Drawing.Color.White;
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
            this.Name = "FrmSelectHtmlTags";
            this.Text = "Selection Tags";
            this.Load += new System.EventHandler(this.FrmSelectHtmlTags_Load);
            ((System.ComponentModel.ISupportInitialize)(this.numSatireLength)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numFalsificationLength)).EndInit();
            this.GrpFals.ResumeLayout(false);
            this.GrpFals.PerformLayout();
            this.GrpSatire.ResumeLayout(false);
            this.GrpSatire.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button BtnOK;
        public System.Windows.Forms.ListBox LstHtmlTags;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.NumericUpDown numSatireLength;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown numFalsificationLength;
        private System.Windows.Forms.GroupBox GrpFals;
        private System.Windows.Forms.GroupBox GrpSatire;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.GroupBox groupBox2;
        public System.Windows.Forms.TextBox TxtHTMLID;
        private System.Windows.Forms.GroupBox groupBox3;
        public System.Windows.Forms.TextBox TxtHTMLClass;
    }
}