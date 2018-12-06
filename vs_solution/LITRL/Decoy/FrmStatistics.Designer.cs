namespace Decoy
{
    partial class FrmStatistics
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
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FrmStatistics));
            this.panel3 = new System.Windows.Forms.Panel();
            this.TabStats = new System.Windows.Forms.TabControl();
            this.tabPage5 = new System.Windows.Forms.TabPage();
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            this.zedGraphStats = new ZedGraph.ZedGraphControl();
            this.panel2 = new System.Windows.Forms.Panel();
            this.label1 = new System.Windows.Forms.Label();
            this.RadDay = new System.Windows.Forms.RadioButton();
            this.RadMonth = new System.Windows.Forms.RadioButton();
            this.BtnNewDS = new System.Windows.Forms.Button();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.TxtDBOutput = new System.Windows.Forms.TextBox();
            this.GrpStatsFalsifications = new System.Windows.Forms.GroupBox();
            this.ChkFalseScore = new System.Windows.Forms.CheckBox();
            this.ChkTruthScore = new System.Windows.Forms.CheckBox();
            this.GrpStatsSatire = new System.Windows.Forms.GroupBox();
            this.ChkNotSatireScore = new System.Windows.Forms.CheckBox();
            this.ChkSatireScore = new System.Windows.Forms.CheckBox();
            this.GrpStatsClickbait = new System.Windows.Forms.GroupBox();
            this.ChkNcbScore = new System.Windows.Forms.CheckBox();
            this.ChkCbScore = new System.Windows.Forms.CheckBox();
            this.GrpBasicStats = new System.Windows.Forms.GroupBox();
            this.ChkMaximum = new System.Windows.Forms.CheckBox();
            this.ChkMinimum = new System.Windows.Forms.CheckBox();
            this.ChkMean = new System.Windows.Forms.CheckBox();
            this.GrpDB1 = new System.Windows.Forms.GroupBox();
            this.RadFalsifications = new System.Windows.Forms.RadioButton();
            this.RadSatire = new System.Windows.Forms.RadioButton();
            this.RadClickbait = new System.Windows.Forms.RadioButton();
            this.label4 = new System.Windows.Forms.Label();
            this.BtnSelectWebsitesDs1 = new System.Windows.Forms.Button();
            this.CboDSBox1 = new System.Windows.Forms.ComboBox();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.zedGraphClickbaitDetails = new ZedGraph.ZedGraphControl();
            this.tabControl1 = new System.Windows.Forms.TabControl();
            this.tabPage4 = new System.Windows.Forms.TabPage();
            this.dataGridViewClickbait = new System.Windows.Forms.DataGridView();
            this.Feature = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Value = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.tabPage6 = new System.Windows.Forms.TabPage();
            this.LstOtherClickbaitTexts = new System.Windows.Forms.ListBox();
            this.TxtClickbait = new System.Windows.Forms.TextBox();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            this.zedGraphSatireDetails = new ZedGraph.ZedGraphControl();
            this.dataGridViewSatire = new System.Windows.Forms.DataGridView();
            this.dataGridViewTextBoxColumn1 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn2 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.RtbSatireText = new System.Windows.Forms.RichTextBox();
            this.tabPage3 = new System.Windows.Forms.TabPage();
            this.zedGraphFalsificationDetails = new ZedGraph.ZedGraphControl();
            this.dataGridViewFalsification = new System.Windows.Forms.DataGridView();
            this.dataGridViewTextBoxColumn3 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn4 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.RtbFalsificationText = new System.Windows.Forms.RichTextBox();
            this.panel3.SuspendLayout();
            this.TabStats.SuspendLayout();
            this.tabPage5.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).BeginInit();
            this.splitContainer1.Panel1.SuspendLayout();
            this.splitContainer1.Panel2.SuspendLayout();
            this.splitContainer1.SuspendLayout();
            this.panel2.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.GrpStatsFalsifications.SuspendLayout();
            this.GrpStatsSatire.SuspendLayout();
            this.GrpStatsClickbait.SuspendLayout();
            this.GrpBasicStats.SuspendLayout();
            this.GrpDB1.SuspendLayout();
            this.tabPage1.SuspendLayout();
            this.tabControl1.SuspendLayout();
            this.tabPage4.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewClickbait)).BeginInit();
            this.tabPage6.SuspendLayout();
            this.tabPage2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewSatire)).BeginInit();
            this.tabPage3.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewFalsification)).BeginInit();
            this.SuspendLayout();
            // 
            // panel3
            // 
            this.panel3.Controls.Add(this.TabStats);
            this.panel3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panel3.Location = new System.Drawing.Point(0, 0);
            this.panel3.Margin = new System.Windows.Forms.Padding(4);
            this.panel3.Name = "panel3";
            this.panel3.Size = new System.Drawing.Size(1198, 739);
            this.panel3.TabIndex = 4;
            // 
            // TabStats
            // 
            this.TabStats.Controls.Add(this.tabPage5);
            this.TabStats.Controls.Add(this.tabPage1);
            this.TabStats.Controls.Add(this.tabPage2);
            this.TabStats.Controls.Add(this.tabPage3);
            this.TabStats.Dock = System.Windows.Forms.DockStyle.Fill;
            this.TabStats.Location = new System.Drawing.Point(0, 0);
            this.TabStats.Margin = new System.Windows.Forms.Padding(4);
            this.TabStats.Multiline = true;
            this.TabStats.Name = "TabStats";
            this.TabStats.SelectedIndex = 0;
            this.TabStats.Size = new System.Drawing.Size(1198, 739);
            this.TabStats.TabIndex = 3;
            // 
            // tabPage5
            // 
            this.tabPage5.Controls.Add(this.splitContainer1);
            this.tabPage5.Location = new System.Drawing.Point(4, 27);
            this.tabPage5.Margin = new System.Windows.Forms.Padding(4);
            this.tabPage5.Name = "tabPage5";
            this.tabPage5.Padding = new System.Windows.Forms.Padding(4);
            this.tabPage5.Size = new System.Drawing.Size(1190, 708);
            this.tabPage5.TabIndex = 1;
            this.tabPage5.Text = "Timeline View";
            this.tabPage5.UseVisualStyleBackColor = true;
            // 
            // splitContainer1
            // 
            this.splitContainer1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer1.Location = new System.Drawing.Point(4, 4);
            this.splitContainer1.Name = "splitContainer1";
            this.splitContainer1.Orientation = System.Windows.Forms.Orientation.Horizontal;
            // 
            // splitContainer1.Panel1
            // 
            this.splitContainer1.Panel1.Controls.Add(this.zedGraphStats);
            this.splitContainer1.Panel1.Controls.Add(this.panel2);
            // 
            // splitContainer1.Panel2
            // 
            this.splitContainer1.Panel2.Controls.Add(this.groupBox1);
            this.splitContainer1.Panel2.Controls.Add(this.GrpStatsFalsifications);
            this.splitContainer1.Panel2.Controls.Add(this.GrpStatsSatire);
            this.splitContainer1.Panel2.Controls.Add(this.GrpStatsClickbait);
            this.splitContainer1.Panel2.Controls.Add(this.GrpBasicStats);
            this.splitContainer1.Panel2.Controls.Add(this.GrpDB1);
            this.splitContainer1.Size = new System.Drawing.Size(1182, 700);
            this.splitContainer1.SplitterDistance = 435;
            this.splitContainer1.TabIndex = 8;
            // 
            // zedGraphStats
            // 
            this.zedGraphStats.BackColor = System.Drawing.Color.Transparent;
            this.zedGraphStats.Dock = System.Windows.Forms.DockStyle.Fill;
            this.zedGraphStats.ForeColor = System.Drawing.Color.White;
            this.zedGraphStats.IsShowCursorValues = true;
            this.zedGraphStats.IsShowPointValues = true;
            this.zedGraphStats.Location = new System.Drawing.Point(0, 52);
            this.zedGraphStats.Margin = new System.Windows.Forms.Padding(9, 8, 9, 8);
            this.zedGraphStats.Name = "zedGraphStats";
            this.zedGraphStats.ScrollGrace = 0D;
            this.zedGraphStats.ScrollMaxX = 0D;
            this.zedGraphStats.ScrollMaxY = 0D;
            this.zedGraphStats.ScrollMaxY2 = 0D;
            this.zedGraphStats.ScrollMinX = 0D;
            this.zedGraphStats.ScrollMinY = 0D;
            this.zedGraphStats.ScrollMinY2 = 0D;
            this.zedGraphStats.Size = new System.Drawing.Size(1182, 383);
            this.zedGraphStats.TabIndex = 8;
            this.zedGraphStats.UseExtendedPrintDialog = true;
            // 
            // panel2
            // 
            this.panel2.BackColor = System.Drawing.Color.Indigo;
            this.panel2.Controls.Add(this.label1);
            this.panel2.Controls.Add(this.RadDay);
            this.panel2.Controls.Add(this.RadMonth);
            this.panel2.Controls.Add(this.BtnNewDS);
            this.panel2.Dock = System.Windows.Forms.DockStyle.Top;
            this.panel2.Location = new System.Drawing.Point(0, 0);
            this.panel2.Margin = new System.Windows.Forms.Padding(4);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(1182, 52);
            this.panel2.TabIndex = 1;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.ForeColor = System.Drawing.Color.White;
            this.label1.Location = new System.Drawing.Point(162, 16);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(47, 18);
            this.label1.TabIndex = 12;
            this.label1.Text = "View:";
            // 
            // RadDay
            // 
            this.RadDay.AutoSize = true;
            this.RadDay.Checked = true;
            this.RadDay.ForeColor = System.Drawing.Color.White;
            this.RadDay.Location = new System.Drawing.Point(289, 14);
            this.RadDay.Name = "RadDay";
            this.RadDay.Size = new System.Drawing.Size(54, 22);
            this.RadDay.TabIndex = 9;
            this.RadDay.TabStop = true;
            this.RadDay.Text = "Day";
            this.RadDay.UseVisualStyleBackColor = true;
            this.RadDay.CheckedChanged += new System.EventHandler(this.RadDay_CheckedChanged);
            // 
            // RadMonth
            // 
            this.RadMonth.AutoSize = true;
            this.RadMonth.Enabled = false;
            this.RadMonth.ForeColor = System.Drawing.Color.White;
            this.RadMonth.Location = new System.Drawing.Point(215, 14);
            this.RadMonth.Name = "RadMonth";
            this.RadMonth.Size = new System.Drawing.Size(68, 22);
            this.RadMonth.TabIndex = 8;
            this.RadMonth.Text = "Month";
            this.RadMonth.UseVisualStyleBackColor = true;
            this.RadMonth.CheckedChanged += new System.EventHandler(this.RadMonth_CheckedChanged);
            // 
            // BtnNewDS
            // 
            this.BtnNewDS.BackColor = System.Drawing.Color.Indigo;
            this.BtnNewDS.Dock = System.Windows.Forms.DockStyle.Left;
            this.BtnNewDS.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.BtnNewDS.Font = new System.Drawing.Font("Arial", 11.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.BtnNewDS.ForeColor = System.Drawing.Color.White;
            this.BtnNewDS.Location = new System.Drawing.Point(0, 0);
            this.BtnNewDS.Margin = new System.Windows.Forms.Padding(4);
            this.BtnNewDS.Name = "BtnNewDS";
            this.BtnNewDS.Size = new System.Drawing.Size(155, 52);
            this.BtnNewDS.TabIndex = 0;
            this.BtnNewDS.Text = "NEW DATASET";
            this.BtnNewDS.UseVisualStyleBackColor = false;
            this.BtnNewDS.Click += new System.EventHandler(this.BtnNewDS_Click);
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.TxtDBOutput);
            this.groupBox1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.groupBox1.Location = new System.Drawing.Point(932, 79);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(250, 182);
            this.groupBox1.TabIndex = 15;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "DB OUTPUT";
            // 
            // TxtDBOutput
            // 
            this.TxtDBOutput.Dock = System.Windows.Forms.DockStyle.Fill;
            this.TxtDBOutput.Location = new System.Drawing.Point(3, 22);
            this.TxtDBOutput.Multiline = true;
            this.TxtDBOutput.Name = "TxtDBOutput";
            this.TxtDBOutput.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.TxtDBOutput.Size = new System.Drawing.Size(244, 157);
            this.TxtDBOutput.TabIndex = 0;
            // 
            // GrpStatsFalsifications
            // 
            this.GrpStatsFalsifications.Controls.Add(this.ChkFalseScore);
            this.GrpStatsFalsifications.Controls.Add(this.ChkTruthScore);
            this.GrpStatsFalsifications.Dock = System.Windows.Forms.DockStyle.Left;
            this.GrpStatsFalsifications.Enabled = false;
            this.GrpStatsFalsifications.Location = new System.Drawing.Point(752, 79);
            this.GrpStatsFalsifications.Name = "GrpStatsFalsifications";
            this.GrpStatsFalsifications.Size = new System.Drawing.Size(180, 182);
            this.GrpStatsFalsifications.TabIndex = 14;
            this.GrpStatsFalsifications.TabStop = false;
            this.GrpStatsFalsifications.Text = "FALSIFICATIONS";
            // 
            // ChkFalseScore
            // 
            this.ChkFalseScore.AutoSize = true;
            this.ChkFalseScore.Location = new System.Drawing.Point(18, 43);
            this.ChkFalseScore.Name = "ChkFalseScore";
            this.ChkFalseScore.Size = new System.Drawing.Size(133, 22);
            this.ChkFalseScore.TabIndex = 1;
            this.ChkFalseScore.Text = "Falsified Score";
            this.ChkFalseScore.UseVisualStyleBackColor = true;
            this.ChkFalseScore.CheckedChanged += new System.EventHandler(this.ChkFalseScore_CheckedChanged);
            // 
            // ChkTruthScore
            // 
            this.ChkTruthScore.AutoSize = true;
            this.ChkTruthScore.Location = new System.Drawing.Point(18, 81);
            this.ChkTruthScore.Name = "ChkTruthScore";
            this.ChkTruthScore.Size = new System.Drawing.Size(147, 22);
            this.ChkTruthScore.TabIndex = 0;
            this.ChkTruthScore.Text = "Legitimate Score";
            this.ChkTruthScore.UseVisualStyleBackColor = true;
            this.ChkTruthScore.CheckedChanged += new System.EventHandler(this.ChkTruthScore_CheckedChanged);
            // 
            // GrpStatsSatire
            // 
            this.GrpStatsSatire.BackColor = System.Drawing.Color.White;
            this.GrpStatsSatire.Controls.Add(this.ChkNotSatireScore);
            this.GrpStatsSatire.Controls.Add(this.ChkSatireScore);
            this.GrpStatsSatire.Dock = System.Windows.Forms.DockStyle.Left;
            this.GrpStatsSatire.Enabled = false;
            this.GrpStatsSatire.Location = new System.Drawing.Point(580, 79);
            this.GrpStatsSatire.Margin = new System.Windows.Forms.Padding(4);
            this.GrpStatsSatire.Name = "GrpStatsSatire";
            this.GrpStatsSatire.Padding = new System.Windows.Forms.Padding(4);
            this.GrpStatsSatire.Size = new System.Drawing.Size(172, 182);
            this.GrpStatsSatire.TabIndex = 13;
            this.GrpStatsSatire.TabStop = false;
            this.GrpStatsSatire.Text = "SATIRE";
            // 
            // ChkNotSatireScore
            // 
            this.ChkNotSatireScore.AutoSize = true;
            this.ChkNotSatireScore.Location = new System.Drawing.Point(18, 82);
            this.ChkNotSatireScore.Name = "ChkNotSatireScore";
            this.ChkNotSatireScore.Size = new System.Drawing.Size(143, 22);
            this.ChkNotSatireScore.TabIndex = 1;
            this.ChkNotSatireScore.Text = "Not Satire Score";
            this.ChkNotSatireScore.UseVisualStyleBackColor = true;
            this.ChkNotSatireScore.CheckedChanged += new System.EventHandler(this.ChkNotSatireScore_CheckedChanged);
            // 
            // ChkSatireScore
            // 
            this.ChkSatireScore.AutoSize = true;
            this.ChkSatireScore.Location = new System.Drawing.Point(18, 44);
            this.ChkSatireScore.Name = "ChkSatireScore";
            this.ChkSatireScore.Size = new System.Drawing.Size(115, 22);
            this.ChkSatireScore.TabIndex = 0;
            this.ChkSatireScore.Text = "Satire Score";
            this.ChkSatireScore.UseVisualStyleBackColor = true;
            this.ChkSatireScore.CheckedChanged += new System.EventHandler(this.ChkSatireScore_CheckedChanged);
            // 
            // GrpStatsClickbait
            // 
            this.GrpStatsClickbait.BackColor = System.Drawing.Color.White;
            this.GrpStatsClickbait.Controls.Add(this.ChkNcbScore);
            this.GrpStatsClickbait.Controls.Add(this.ChkCbScore);
            this.GrpStatsClickbait.Dock = System.Windows.Forms.DockStyle.Left;
            this.GrpStatsClickbait.Enabled = false;
            this.GrpStatsClickbait.Location = new System.Drawing.Point(393, 79);
            this.GrpStatsClickbait.Margin = new System.Windows.Forms.Padding(4);
            this.GrpStatsClickbait.Name = "GrpStatsClickbait";
            this.GrpStatsClickbait.Padding = new System.Windows.Forms.Padding(4);
            this.GrpStatsClickbait.Size = new System.Drawing.Size(187, 182);
            this.GrpStatsClickbait.TabIndex = 12;
            this.GrpStatsClickbait.TabStop = false;
            this.GrpStatsClickbait.Text = "CLICKBAIT";
            // 
            // ChkNcbScore
            // 
            this.ChkNcbScore.AutoSize = true;
            this.ChkNcbScore.Location = new System.Drawing.Point(16, 82);
            this.ChkNcbScore.Name = "ChkNcbScore";
            this.ChkNcbScore.Size = new System.Drawing.Size(162, 22);
            this.ChkNcbScore.TabIndex = 1;
            this.ChkNcbScore.Text = "Not Clickbait Score";
            this.ChkNcbScore.UseVisualStyleBackColor = true;
            this.ChkNcbScore.CheckedChanged += new System.EventHandler(this.ChkNcbScore_CheckedChanged);
            // 
            // ChkCbScore
            // 
            this.ChkCbScore.AutoSize = true;
            this.ChkCbScore.Location = new System.Drawing.Point(16, 44);
            this.ChkCbScore.Name = "ChkCbScore";
            this.ChkCbScore.Size = new System.Drawing.Size(134, 22);
            this.ChkCbScore.TabIndex = 0;
            this.ChkCbScore.Text = "Clickbait Score";
            this.ChkCbScore.UseVisualStyleBackColor = true;
            this.ChkCbScore.CheckedChanged += new System.EventHandler(this.ChkCbScore_CheckedChanged);
            // 
            // GrpBasicStats
            // 
            this.GrpBasicStats.Controls.Add(this.ChkMaximum);
            this.GrpBasicStats.Controls.Add(this.ChkMinimum);
            this.GrpBasicStats.Controls.Add(this.ChkMean);
            this.GrpBasicStats.Dock = System.Windows.Forms.DockStyle.Top;
            this.GrpBasicStats.Location = new System.Drawing.Point(393, 0);
            this.GrpBasicStats.Name = "GrpBasicStats";
            this.GrpBasicStats.Size = new System.Drawing.Size(789, 79);
            this.GrpBasicStats.TabIndex = 10;
            this.GrpBasicStats.TabStop = false;
            this.GrpBasicStats.Text = "BASIC STATS";
            // 
            // ChkMaximum
            // 
            this.ChkMaximum.AutoSize = true;
            this.ChkMaximum.Location = new System.Drawing.Point(202, 35);
            this.ChkMaximum.Name = "ChkMaximum";
            this.ChkMaximum.Size = new System.Drawing.Size(94, 22);
            this.ChkMaximum.TabIndex = 4;
            this.ChkMaximum.Text = "Maximum";
            this.ChkMaximum.UseVisualStyleBackColor = true;
            this.ChkMaximum.CheckedChanged += new System.EventHandler(this.ChkMaximum_CheckedChanged);
            // 
            // ChkMinimum
            // 
            this.ChkMinimum.AutoSize = true;
            this.ChkMinimum.Location = new System.Drawing.Point(16, 35);
            this.ChkMinimum.Name = "ChkMinimum";
            this.ChkMinimum.Size = new System.Drawing.Size(90, 22);
            this.ChkMinimum.TabIndex = 3;
            this.ChkMinimum.Text = "Minimum";
            this.ChkMinimum.UseVisualStyleBackColor = true;
            this.ChkMinimum.CheckedChanged += new System.EventHandler(this.ChkMinimum_CheckedChanged);
            // 
            // ChkMean
            // 
            this.ChkMean.AutoSize = true;
            this.ChkMean.Location = new System.Drawing.Point(121, 35);
            this.ChkMean.Name = "ChkMean";
            this.ChkMean.Size = new System.Drawing.Size(66, 22);
            this.ChkMean.TabIndex = 0;
            this.ChkMean.Text = "Mean";
            this.ChkMean.UseVisualStyleBackColor = true;
            this.ChkMean.CheckedChanged += new System.EventHandler(this.ChkMean_CheckedChanged);
            // 
            // GrpDB1
            // 
            this.GrpDB1.Controls.Add(this.RadFalsifications);
            this.GrpDB1.Controls.Add(this.RadSatire);
            this.GrpDB1.Controls.Add(this.RadClickbait);
            this.GrpDB1.Controls.Add(this.label4);
            this.GrpDB1.Controls.Add(this.BtnSelectWebsitesDs1);
            this.GrpDB1.Controls.Add(this.CboDSBox1);
            this.GrpDB1.Dock = System.Windows.Forms.DockStyle.Left;
            this.GrpDB1.Location = new System.Drawing.Point(0, 0);
            this.GrpDB1.Margin = new System.Windows.Forms.Padding(4);
            this.GrpDB1.Name = "GrpDB1";
            this.GrpDB1.Padding = new System.Windows.Forms.Padding(4);
            this.GrpDB1.Size = new System.Drawing.Size(393, 261);
            this.GrpDB1.TabIndex = 7;
            this.GrpDB1.TabStop = false;
            this.GrpDB1.Text = "DATASET";
            this.GrpDB1.UseCompatibleTextRendering = true;
            // 
            // RadFalsifications
            // 
            this.RadFalsifications.AutoSize = true;
            this.RadFalsifications.Location = new System.Drawing.Point(31, 196);
            this.RadFalsifications.Name = "RadFalsifications";
            this.RadFalsifications.Size = new System.Drawing.Size(118, 22);
            this.RadFalsifications.TabIndex = 9;
            this.RadFalsifications.TabStop = true;
            this.RadFalsifications.Text = "Falsifications";
            this.RadFalsifications.UseVisualStyleBackColor = true;
            this.RadFalsifications.CheckedChanged += new System.EventHandler(this.RadFalsifications_CheckedChanged);
            // 
            // RadSatire
            // 
            this.RadSatire.AutoSize = true;
            this.RadSatire.Location = new System.Drawing.Point(31, 159);
            this.RadSatire.Name = "RadSatire";
            this.RadSatire.Size = new System.Drawing.Size(68, 22);
            this.RadSatire.TabIndex = 8;
            this.RadSatire.TabStop = true;
            this.RadSatire.Text = "Satire";
            this.RadSatire.UseVisualStyleBackColor = true;
            this.RadSatire.CheckedChanged += new System.EventHandler(this.RadSatire_CheckedChanged);
            // 
            // RadClickbait
            // 
            this.RadClickbait.AutoSize = true;
            this.RadClickbait.Location = new System.Drawing.Point(31, 122);
            this.RadClickbait.Name = "RadClickbait";
            this.RadClickbait.Size = new System.Drawing.Size(87, 22);
            this.RadClickbait.TabIndex = 7;
            this.RadClickbait.TabStop = true;
            this.RadClickbait.Text = "Clickbait";
            this.RadClickbait.UseVisualStyleBackColor = true;
            this.RadClickbait.CheckedChanged += new System.EventHandler(this.RadClickbait_CheckedChanged);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(28, 39);
            this.label4.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(143, 18);
            this.label4.TabIndex = 6;
            this.label4.Text = "Available Datasets:";
            // 
            // BtnSelectWebsitesDs1
            // 
            this.BtnSelectWebsitesDs1.Location = new System.Drawing.Point(215, 172);
            this.BtnSelectWebsitesDs1.Margin = new System.Windows.Forms.Padding(4);
            this.BtnSelectWebsitesDs1.Name = "BtnSelectWebsitesDs1";
            this.BtnSelectWebsitesDs1.Size = new System.Drawing.Size(156, 46);
            this.BtnSelectWebsitesDs1.TabIndex = 5;
            this.BtnSelectWebsitesDs1.Text = "Select Websites";
            this.BtnSelectWebsitesDs1.UseVisualStyleBackColor = true;
            this.BtnSelectWebsitesDs1.Click += new System.EventHandler(this.BtnSelectWebsitesDs1_Click);
            // 
            // CboDSBox1
            // 
            this.CboDSBox1.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.CboDSBox1.FormattingEnabled = true;
            this.CboDSBox1.Location = new System.Drawing.Point(33, 65);
            this.CboDSBox1.Margin = new System.Windows.Forms.Padding(4);
            this.CboDSBox1.Name = "CboDSBox1";
            this.CboDSBox1.Size = new System.Drawing.Size(338, 26);
            this.CboDSBox1.TabIndex = 0;
            this.CboDSBox1.SelectedIndexChanged += new System.EventHandler(this.CboDSBox1_SelectedIndexChanged);
            // 
            // tabPage1
            // 
            this.tabPage1.Controls.Add(this.zedGraphClickbaitDetails);
            this.tabPage1.Controls.Add(this.tabControl1);
            this.tabPage1.Controls.Add(this.TxtClickbait);
            this.tabPage1.Location = new System.Drawing.Point(4, 27);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Size = new System.Drawing.Size(1190, 708);
            this.tabPage1.TabIndex = 2;
            this.tabPage1.Text = "Clickbait Explorer";
            this.tabPage1.UseVisualStyleBackColor = true;
            // 
            // zedGraphClickbaitDetails
            // 
            this.zedGraphClickbaitDetails.Dock = System.Windows.Forms.DockStyle.Fill;
            this.zedGraphClickbaitDetails.Location = new System.Drawing.Point(390, 75);
            this.zedGraphClickbaitDetails.Margin = new System.Windows.Forms.Padding(6);
            this.zedGraphClickbaitDetails.Name = "zedGraphClickbaitDetails";
            this.zedGraphClickbaitDetails.ScrollGrace = 0D;
            this.zedGraphClickbaitDetails.ScrollMaxX = 0D;
            this.zedGraphClickbaitDetails.ScrollMaxY = 0D;
            this.zedGraphClickbaitDetails.ScrollMaxY2 = 0D;
            this.zedGraphClickbaitDetails.ScrollMinX = 0D;
            this.zedGraphClickbaitDetails.ScrollMinY = 0D;
            this.zedGraphClickbaitDetails.ScrollMinY2 = 0D;
            this.zedGraphClickbaitDetails.Size = new System.Drawing.Size(800, 633);
            this.zedGraphClickbaitDetails.TabIndex = 8;
            this.zedGraphClickbaitDetails.UseExtendedPrintDialog = true;
            // 
            // tabControl1
            // 
            this.tabControl1.Controls.Add(this.tabPage4);
            this.tabControl1.Controls.Add(this.tabPage6);
            this.tabControl1.Dock = System.Windows.Forms.DockStyle.Left;
            this.tabControl1.Location = new System.Drawing.Point(0, 75);
            this.tabControl1.Name = "tabControl1";
            this.tabControl1.SelectedIndex = 0;
            this.tabControl1.Size = new System.Drawing.Size(390, 633);
            this.tabControl1.TabIndex = 7;
            // 
            // tabPage4
            // 
            this.tabPage4.Controls.Add(this.dataGridViewClickbait);
            this.tabPage4.Location = new System.Drawing.Point(4, 27);
            this.tabPage4.Name = "tabPage4";
            this.tabPage4.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage4.Size = new System.Drawing.Size(382, 602);
            this.tabPage4.TabIndex = 0;
            this.tabPage4.Text = "Feature Scores";
            this.tabPage4.UseVisualStyleBackColor = true;
            // 
            // dataGridViewClickbait
            // 
            this.dataGridViewClickbait.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewClickbait.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.Feature,
            this.Value});
            this.dataGridViewClickbait.Dock = System.Windows.Forms.DockStyle.Fill;
            this.dataGridViewClickbait.Location = new System.Drawing.Point(3, 3);
            this.dataGridViewClickbait.Margin = new System.Windows.Forms.Padding(2);
            this.dataGridViewClickbait.Name = "dataGridViewClickbait";
            this.dataGridViewClickbait.RowTemplate.Height = 24;
            this.dataGridViewClickbait.Size = new System.Drawing.Size(376, 596);
            this.dataGridViewClickbait.TabIndex = 5;
            // 
            // Feature
            // 
            this.Feature.HeaderText = "Feature";
            this.Feature.Name = "Feature";
            this.Feature.ReadOnly = true;
            this.Feature.Width = 250;
            // 
            // Value
            // 
            this.Value.HeaderText = "Value";
            this.Value.Name = "Value";
            this.Value.ReadOnly = true;
            this.Value.Width = 250;
            // 
            // tabPage6
            // 
            this.tabPage6.Controls.Add(this.LstOtherClickbaitTexts);
            this.tabPage6.Location = new System.Drawing.Point(4, 27);
            this.tabPage6.Name = "tabPage6";
            this.tabPage6.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage6.Size = new System.Drawing.Size(382, 630);
            this.tabPage6.TabIndex = 1;
            this.tabPage6.Text = "Compare";
            this.tabPage6.UseVisualStyleBackColor = true;
            // 
            // LstOtherClickbaitTexts
            // 
            this.LstOtherClickbaitTexts.Dock = System.Windows.Forms.DockStyle.Fill;
            this.LstOtherClickbaitTexts.FormattingEnabled = true;
            this.LstOtherClickbaitTexts.HorizontalScrollbar = true;
            this.LstOtherClickbaitTexts.ItemHeight = 18;
            this.LstOtherClickbaitTexts.Location = new System.Drawing.Point(3, 3);
            this.LstOtherClickbaitTexts.Name = "LstOtherClickbaitTexts";
            this.LstOtherClickbaitTexts.ScrollAlwaysVisible = true;
            this.LstOtherClickbaitTexts.Size = new System.Drawing.Size(376, 624);
            this.LstOtherClickbaitTexts.TabIndex = 0;
            this.LstOtherClickbaitTexts.SelectedIndexChanged += new System.EventHandler(this.LstOtherTexts_SelectedIndexChanged);
            // 
            // TxtClickbait
            // 
            this.TxtClickbait.Dock = System.Windows.Forms.DockStyle.Top;
            this.TxtClickbait.Font = new System.Drawing.Font("Microsoft Sans Serif", 18F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.TxtClickbait.Location = new System.Drawing.Point(0, 0);
            this.TxtClickbait.Margin = new System.Windows.Forms.Padding(2);
            this.TxtClickbait.Multiline = true;
            this.TxtClickbait.Name = "TxtClickbait";
            this.TxtClickbait.ReadOnly = true;
            this.TxtClickbait.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.TxtClickbait.Size = new System.Drawing.Size(1190, 75);
            this.TxtClickbait.TabIndex = 3;
            // 
            // tabPage2
            // 
            this.tabPage2.Controls.Add(this.zedGraphSatireDetails);
            this.tabPage2.Controls.Add(this.dataGridViewSatire);
            this.tabPage2.Controls.Add(this.RtbSatireText);
            this.tabPage2.Location = new System.Drawing.Point(4, 27);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Size = new System.Drawing.Size(1190, 708);
            this.tabPage2.TabIndex = 3;
            this.tabPage2.Text = "Satire Explorer";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // zedGraphSatireDetails
            // 
            this.zedGraphSatireDetails.Dock = System.Windows.Forms.DockStyle.Fill;
            this.zedGraphSatireDetails.Location = new System.Drawing.Point(434, 164);
            this.zedGraphSatireDetails.Margin = new System.Windows.Forms.Padding(9, 8, 9, 8);
            this.zedGraphSatireDetails.Name = "zedGraphSatireDetails";
            this.zedGraphSatireDetails.ScrollGrace = 0D;
            this.zedGraphSatireDetails.ScrollMaxX = 0D;
            this.zedGraphSatireDetails.ScrollMaxY = 0D;
            this.zedGraphSatireDetails.ScrollMaxY2 = 0D;
            this.zedGraphSatireDetails.ScrollMinX = 0D;
            this.zedGraphSatireDetails.ScrollMinY = 0D;
            this.zedGraphSatireDetails.ScrollMinY2 = 0D;
            this.zedGraphSatireDetails.Size = new System.Drawing.Size(756, 544);
            this.zedGraphSatireDetails.TabIndex = 11;
            this.zedGraphSatireDetails.UseExtendedPrintDialog = true;
            // 
            // dataGridViewSatire
            // 
            this.dataGridViewSatire.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewSatire.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.dataGridViewTextBoxColumn1,
            this.dataGridViewTextBoxColumn2});
            this.dataGridViewSatire.Dock = System.Windows.Forms.DockStyle.Left;
            this.dataGridViewSatire.Location = new System.Drawing.Point(0, 164);
            this.dataGridViewSatire.Margin = new System.Windows.Forms.Padding(2);
            this.dataGridViewSatire.Name = "dataGridViewSatire";
            this.dataGridViewSatire.RowTemplate.Height = 24;
            this.dataGridViewSatire.Size = new System.Drawing.Size(434, 544);
            this.dataGridViewSatire.TabIndex = 10;
            // 
            // dataGridViewTextBoxColumn1
            // 
            this.dataGridViewTextBoxColumn1.HeaderText = "Feature";
            this.dataGridViewTextBoxColumn1.Name = "dataGridViewTextBoxColumn1";
            this.dataGridViewTextBoxColumn1.ReadOnly = true;
            this.dataGridViewTextBoxColumn1.Width = 250;
            // 
            // dataGridViewTextBoxColumn2
            // 
            this.dataGridViewTextBoxColumn2.HeaderText = "Value";
            this.dataGridViewTextBoxColumn2.Name = "dataGridViewTextBoxColumn2";
            this.dataGridViewTextBoxColumn2.ReadOnly = true;
            this.dataGridViewTextBoxColumn2.Width = 250;
            // 
            // RtbSatireText
            // 
            this.RtbSatireText.Dock = System.Windows.Forms.DockStyle.Top;
            this.RtbSatireText.Location = new System.Drawing.Point(0, 0);
            this.RtbSatireText.Name = "RtbSatireText";
            this.RtbSatireText.Size = new System.Drawing.Size(1190, 164);
            this.RtbSatireText.TabIndex = 0;
            this.RtbSatireText.Text = "";
            // 
            // tabPage3
            // 
            this.tabPage3.Controls.Add(this.zedGraphFalsificationDetails);
            this.tabPage3.Controls.Add(this.dataGridViewFalsification);
            this.tabPage3.Controls.Add(this.RtbFalsificationText);
            this.tabPage3.Location = new System.Drawing.Point(4, 27);
            this.tabPage3.Name = "tabPage3";
            this.tabPage3.Size = new System.Drawing.Size(1190, 708);
            this.tabPage3.TabIndex = 4;
            this.tabPage3.Text = "Falsification (WIP) Explorer";
            this.tabPage3.UseVisualStyleBackColor = true;
            // 
            // zedGraphFalsificationDetails
            // 
            this.zedGraphFalsificationDetails.Dock = System.Windows.Forms.DockStyle.Fill;
            this.zedGraphFalsificationDetails.Location = new System.Drawing.Point(434, 164);
            this.zedGraphFalsificationDetails.Margin = new System.Windows.Forms.Padding(14, 11, 14, 11);
            this.zedGraphFalsificationDetails.Name = "zedGraphFalsificationDetails";
            this.zedGraphFalsificationDetails.ScrollGrace = 0D;
            this.zedGraphFalsificationDetails.ScrollMaxX = 0D;
            this.zedGraphFalsificationDetails.ScrollMaxY = 0D;
            this.zedGraphFalsificationDetails.ScrollMaxY2 = 0D;
            this.zedGraphFalsificationDetails.ScrollMinX = 0D;
            this.zedGraphFalsificationDetails.ScrollMinY = 0D;
            this.zedGraphFalsificationDetails.ScrollMinY2 = 0D;
            this.zedGraphFalsificationDetails.Size = new System.Drawing.Size(756, 544);
            this.zedGraphFalsificationDetails.TabIndex = 14;
            this.zedGraphFalsificationDetails.UseExtendedPrintDialog = true;
            // 
            // dataGridViewFalsification
            // 
            this.dataGridViewFalsification.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewFalsification.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.dataGridViewTextBoxColumn3,
            this.dataGridViewTextBoxColumn4});
            this.dataGridViewFalsification.Dock = System.Windows.Forms.DockStyle.Left;
            this.dataGridViewFalsification.Location = new System.Drawing.Point(0, 164);
            this.dataGridViewFalsification.Margin = new System.Windows.Forms.Padding(2);
            this.dataGridViewFalsification.Name = "dataGridViewFalsification";
            this.dataGridViewFalsification.RowTemplate.Height = 24;
            this.dataGridViewFalsification.Size = new System.Drawing.Size(434, 544);
            this.dataGridViewFalsification.TabIndex = 13;
            // 
            // dataGridViewTextBoxColumn3
            // 
            this.dataGridViewTextBoxColumn3.HeaderText = "Feature";
            this.dataGridViewTextBoxColumn3.Name = "dataGridViewTextBoxColumn3";
            this.dataGridViewTextBoxColumn3.ReadOnly = true;
            this.dataGridViewTextBoxColumn3.Width = 250;
            // 
            // dataGridViewTextBoxColumn4
            // 
            this.dataGridViewTextBoxColumn4.HeaderText = "Value";
            this.dataGridViewTextBoxColumn4.Name = "dataGridViewTextBoxColumn4";
            this.dataGridViewTextBoxColumn4.ReadOnly = true;
            this.dataGridViewTextBoxColumn4.Width = 250;
            // 
            // RtbFalsificationText
            // 
            this.RtbFalsificationText.Dock = System.Windows.Forms.DockStyle.Top;
            this.RtbFalsificationText.Location = new System.Drawing.Point(0, 0);
            this.RtbFalsificationText.Name = "RtbFalsificationText";
            this.RtbFalsificationText.Size = new System.Drawing.Size(1190, 164);
            this.RtbFalsificationText.TabIndex = 12;
            this.RtbFalsificationText.Text = "";
            // 
            // FrmStatistics
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 18F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Control;
            this.ClientSize = new System.Drawing.Size(1198, 739);
            this.Controls.Add(this.panel3);
            this.Font = new System.Drawing.Font("Arial", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.ForeColor = System.Drawing.Color.Black;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(4);
            this.Name = "FrmStatistics";
            this.Text = "Litrl Browser - News Verification Suite - Statistics";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.FrmStatistics_FormClosing);
            this.Load += new System.EventHandler(this.FrmStatistics_Load);
            this.panel3.ResumeLayout(false);
            this.TabStats.ResumeLayout(false);
            this.tabPage5.ResumeLayout(false);
            this.splitContainer1.Panel1.ResumeLayout(false);
            this.splitContainer1.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).EndInit();
            this.splitContainer1.ResumeLayout(false);
            this.panel2.ResumeLayout(false);
            this.panel2.PerformLayout();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.GrpStatsFalsifications.ResumeLayout(false);
            this.GrpStatsFalsifications.PerformLayout();
            this.GrpStatsSatire.ResumeLayout(false);
            this.GrpStatsSatire.PerformLayout();
            this.GrpStatsClickbait.ResumeLayout(false);
            this.GrpStatsClickbait.PerformLayout();
            this.GrpBasicStats.ResumeLayout(false);
            this.GrpBasicStats.PerformLayout();
            this.GrpDB1.ResumeLayout(false);
            this.GrpDB1.PerformLayout();
            this.tabPage1.ResumeLayout(false);
            this.tabPage1.PerformLayout();
            this.tabControl1.ResumeLayout(false);
            this.tabPage4.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewClickbait)).EndInit();
            this.tabPage6.ResumeLayout(false);
            this.tabPage2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewSatire)).EndInit();
            this.tabPage3.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewFalsification)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Panel panel3;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.Button BtnNewDS;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.RadioButton RadDay;
        private System.Windows.Forms.RadioButton RadMonth;
        private System.Windows.Forms.TabControl TabStats;
        private System.Windows.Forms.TabPage tabPage5;
        private System.Windows.Forms.SplitContainer splitContainer1;
        private System.Windows.Forms.GroupBox GrpDB1;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button BtnSelectWebsitesDs1;
        private System.Windows.Forms.ComboBox CboDSBox1;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.TabPage tabPage2;
        private System.Windows.Forms.TabPage tabPage3;
        private System.Windows.Forms.DataGridView dataGridViewClickbait;
        private System.Windows.Forms.DataGridViewTextBoxColumn Feature;
        private System.Windows.Forms.DataGridViewTextBoxColumn Value;
        private System.Windows.Forms.TextBox TxtClickbait;
        private System.Windows.Forms.RadioButton RadFalsifications;
        private System.Windows.Forms.RadioButton RadSatire;
        private System.Windows.Forms.RadioButton RadClickbait;
        private System.Windows.Forms.GroupBox GrpStatsSatire;
        private System.Windows.Forms.GroupBox GrpStatsClickbait;
        private System.Windows.Forms.GroupBox GrpBasicStats;
        private System.Windows.Forms.CheckBox ChkMaximum;
        private System.Windows.Forms.CheckBox ChkMinimum;
        private System.Windows.Forms.CheckBox ChkMean;
        private System.Windows.Forms.GroupBox GrpStatsFalsifications;
        private System.Windows.Forms.CheckBox ChkNotSatireScore;
        private System.Windows.Forms.CheckBox ChkSatireScore;
        private System.Windows.Forms.CheckBox ChkNcbScore;
        private System.Windows.Forms.CheckBox ChkCbScore;
        private System.Windows.Forms.CheckBox ChkFalseScore;
        private System.Windows.Forms.CheckBox ChkTruthScore;
        private ZedGraph.ZedGraphControl zedGraphSatireDetails;
        private System.Windows.Forms.DataGridView dataGridViewSatire;
        private System.Windows.Forms.DataGridViewTextBoxColumn dataGridViewTextBoxColumn1;
        private System.Windows.Forms.DataGridViewTextBoxColumn dataGridViewTextBoxColumn2;
        private System.Windows.Forms.RichTextBox RtbSatireText;
        private ZedGraph.ZedGraphControl zedGraphClickbaitDetails;
        private System.Windows.Forms.TabControl tabControl1;
        private System.Windows.Forms.TabPage tabPage4;
        private System.Windows.Forms.TabPage tabPage6;
        private System.Windows.Forms.ListBox LstOtherClickbaitTexts;
        private ZedGraph.ZedGraphControl zedGraphFalsificationDetails;
        private System.Windows.Forms.DataGridView dataGridViewFalsification;
        private System.Windows.Forms.DataGridViewTextBoxColumn dataGridViewTextBoxColumn3;
        private System.Windows.Forms.DataGridViewTextBoxColumn dataGridViewTextBoxColumn4;
        private System.Windows.Forms.RichTextBox RtbFalsificationText;
        private ZedGraph.ZedGraphControl zedGraphStats;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.TextBox TxtDBOutput;
    }
}