namespace Decoy
{
    partial class FrmNewDataset
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
            this.label1 = new System.Windows.Forms.Label();
            this.BtnCreateDataset = new System.Windows.Forms.Button();
            this.TxtDatasetName = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(12, 9);
            this.label1.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(539, 44);
            this.label1.TabIndex = 0;
            this.label1.Text = "Enter name of dataset below:";
            // 
            // BtnCreateDataset
            // 
            this.BtnCreateDataset.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.BtnCreateDataset.Location = new System.Drawing.Point(13, 75);
            this.BtnCreateDataset.Margin = new System.Windows.Forms.Padding(4);
            this.BtnCreateDataset.Name = "BtnCreateDataset";
            this.BtnCreateDataset.Size = new System.Drawing.Size(530, 29);
            this.BtnCreateDataset.TabIndex = 1;
            this.BtnCreateDataset.Text = "Create Dataset";
            this.BtnCreateDataset.UseVisualStyleBackColor = true;
            this.BtnCreateDataset.Click += new System.EventHandler(this.BtnCreateDataset_Click);
            // 
            // TxtDatasetName
            // 
            this.TxtDatasetName.Location = new System.Drawing.Point(13, 41);
            this.TxtDatasetName.Margin = new System.Windows.Forms.Padding(4);
            this.TxtDatasetName.Name = "TxtDatasetName";
            this.TxtDatasetName.Size = new System.Drawing.Size(529, 26);
            this.TxtDatasetName.TabIndex = 2;
            // 
            // label2
            // 
            this.label2.Location = new System.Drawing.Point(13, 108);
            this.label2.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(530, 49);
            this.label2.TabIndex = 3;
            this.label2.Text = "(Note: This creates a new Sqlite Database which you can query outside of the News" +
    " Verification Suite)";
            // 
            // FrmNewDataset
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 18F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.Indigo;
            this.ClientSize = new System.Drawing.Size(554, 159);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.TxtDatasetName);
            this.Controls.Add(this.BtnCreateDataset);
            this.Controls.Add(this.label1);
            this.Font = new System.Drawing.Font("Arial", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.ForeColor = System.Drawing.Color.White;
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
            this.Margin = new System.Windows.Forms.Padding(4);
            this.Name = "FrmNewDataset";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Create New Dataset";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button BtnCreateDataset;
        private System.Windows.Forms.TextBox TxtDatasetName;
        private System.Windows.Forms.Label label2;
    }
}