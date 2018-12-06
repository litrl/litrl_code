namespace Decoy
{
    partial class FrmSelectWebsites
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
            this.LstWebsites = new System.Windows.Forms.ListBox();
            this.BtnOK = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // LstWebsites
            // 
            this.LstWebsites.FormattingEnabled = true;
            this.LstWebsites.ItemHeight = 16;
            this.LstWebsites.Location = new System.Drawing.Point(14, 15);
            this.LstWebsites.Margin = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.LstWebsites.Name = "LstWebsites";
            this.LstWebsites.ScrollAlwaysVisible = true;
            this.LstWebsites.Size = new System.Drawing.Size(556, 484);
            this.LstWebsites.Sorted = true;
            this.LstWebsites.TabIndex = 0;
            // 
            // BtnOK
            // 
            this.BtnOK.Location = new System.Drawing.Point(483, 507);
            this.BtnOK.Margin = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.BtnOK.Name = "BtnOK";
            this.BtnOK.Size = new System.Drawing.Size(87, 41);
            this.BtnOK.TabIndex = 1;
            this.BtnOK.Text = "OK";
            this.BtnOK.UseVisualStyleBackColor = true;
            this.BtnOK.Click += new System.EventHandler(this.BtnOK_Click);
            // 
            // FrmSelectWebsites
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(583, 562);
            this.ControlBox = false;
            this.Controls.Add(this.BtnOK);
            this.Controls.Add(this.LstWebsites);
            this.Font = new System.Drawing.Font("Arial", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
            this.Margin = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.Name = "FrmSelectWebsites";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Select Websites";
            this.ResumeLayout(false);

        }

        #endregion
        private System.Windows.Forms.Button BtnOK;
        public System.Windows.Forms.ListBox LstWebsites;
    }
}