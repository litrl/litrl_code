namespace Decoy
{
    partial class ClickbaitFrame
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

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.LstViewClickbait = new System.Windows.Forms.ListView();
            this.colId = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.colClickbaitScore = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.colNotClickbaitScore = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.colText = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.colTypeColor = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.SuspendLayout();
            // 
            // LstViewClickbait
            // 
            this.LstViewClickbait.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.colId,
            this.colTypeColor,
            this.colClickbaitScore,
            this.colNotClickbaitScore,
            this.colText});
            this.LstViewClickbait.Dock = System.Windows.Forms.DockStyle.Fill;
            this.LstViewClickbait.Font = new System.Drawing.Font("Arial", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.LstViewClickbait.FullRowSelect = true;
            this.LstViewClickbait.GridLines = true;
            this.LstViewClickbait.Location = new System.Drawing.Point(0, 0);
            this.LstViewClickbait.Name = "LstViewClickbait";
            this.LstViewClickbait.Size = new System.Drawing.Size(705, 251);
            this.LstViewClickbait.TabIndex = 0;
            this.LstViewClickbait.UseCompatibleStateImageBehavior = false;
            this.LstViewClickbait.View = System.Windows.Forms.View.Details;
            this.LstViewClickbait.ColumnClick += new System.Windows.Forms.ColumnClickEventHandler(this.LstViewClickbait_ColumnClick);
            // 
            // colId
            // 
            this.colId.Text = "ID";
            this.colId.Width = 41;
            // 
            // colClickbaitScore
            // 
            this.colClickbaitScore.Text = "Clickbait %";
            this.colClickbaitScore.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.colClickbaitScore.Width = 105;
            // 
            // colNotClickbaitScore
            // 
            this.colNotClickbaitScore.Text = "Not %";
            this.colNotClickbaitScore.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.colNotClickbaitScore.Width = 72;
            // 
            // colText
            // 
            this.colText.Text = "Text";
            this.colText.Width = 379;
            // 
            // colTypeColor
            // 
            this.colTypeColor.Text = "";
            this.colTypeColor.Width = 21;
            // 
            // ClickbaitFrame
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.LstViewClickbait);
            this.Name = "ClickbaitFrame";
            this.Size = new System.Drawing.Size(705, 251);
            this.ResumeLayout(false);

        }

        #endregion

        public System.Windows.Forms.ListView LstViewClickbait;
        private System.Windows.Forms.ColumnHeader colClickbaitScore;
        private System.Windows.Forms.ColumnHeader colNotClickbaitScore;
        private System.Windows.Forms.ColumnHeader colText;
        private System.Windows.Forms.ColumnHeader colId;
        private System.Windows.Forms.ColumnHeader colTypeColor;
    }
}
