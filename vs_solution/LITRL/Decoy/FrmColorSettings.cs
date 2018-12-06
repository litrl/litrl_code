/*

Copyright Victoria L. Rubin 2017-2018.

This file is part of Litrl Browser.

Litrl Browser is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Litrl Browser is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Litrl Browser.If not, see<https://www.gnu.org/licenses/>. 

*/

using System;
using System.Data.SQLite;
using System.Drawing;
using System.Windows.Forms;

namespace Decoy
{
    public partial class FrmColorSettings : Form
    {
        public FrmColorSettings()
        {
            InitializeComponent();
        }

        private ColorDialog colorDialog = new ColorDialog();

        private void BtnSetNotCB_Click(object sender, EventArgs e)
        {
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                panNotCB.BackColor = colorDialog.Color;
            }
        }

        private void panSetModerateCB_Click(object sender, EventArgs e)
        {
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                panModerateCB.BackColor = colorDialog.Color;
            }
        }

        private void BtnSetSlightCB_Click(object sender, EventArgs e)
        {
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                panSlightCB.BackColor = colorDialog.Color;
            }
        }

        private void BtnSetHeavyCB_Click(object sender, EventArgs e)
        {
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                panHeavyCB.BackColor = colorDialog.Color;
            }
        }

        private void BtnSetNotSatire_Click(object sender, EventArgs e)
        {
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                panNotSatire.BackColor = colorDialog.Color;
            }
        }

        private void panSetSatire_Click(object sender, EventArgs e)
        {
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                panSatire.BackColor = colorDialog.Color;
            }
        }

        private void BtnSetNotFals_Click(object sender, EventArgs e)
        {
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                panNotFals.BackColor = colorDialog.Color;
            }
        }

        private void BtnSetFals_Click(object sender, EventArgs e)
        {
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                panFals.BackColor = colorDialog.Color;
            }
        }

        private void FrmColorSettings_Load(object sender, EventArgs e)
        {
            panNotCB.BackColor = GetColorFromString(FrmMain.CLICKBAIT_LOW_COLOR);
            panSlightCB.BackColor = GetColorFromString(FrmMain.CLICKBAIT_SLIGHT_COLOR);
            panModerateCB.BackColor = GetColorFromString(FrmMain.CLICKBAIT_MODERATE_COLOR);
            panHeavyCB.BackColor = GetColorFromString(FrmMain.CLICKBAIT_HEAVY_COLOR);
            panSatire.BackColor = GetColorFromString(FrmMain.SATIRE_TEXT_COLOR);
            panNotSatire.BackColor = GetColorFromString(FrmMain.NOT_SATIRE_TEXT_COLOR);
            panFals.BackColor = GetColorFromString(FrmMain.FALSIFICATION_TEXT_COLOR);
            panNotFals.BackColor = GetColorFromString(FrmMain.NOT_FALSIFICATION_TEXT_COLOR);

            numHeavy.Value = Convert.ToInt32(FrmMain.CLICKBAIT_HEAVY_THRESHOLD * 100);
            numModerate.Value = Convert.ToInt32(FrmMain.CLICKBAIT_MODERATE_THRESHOLD * 100);
            numSlight.Value = Convert.ToInt32(FrmMain.CLICKBAIT_SLIGHT_THRESHOLD * 100);
        }

        public static Color GetColorFromString(string col)
        {
            string[] rgb = col.Split(',');
            Color newCol = Color.FromArgb(Convert.ToInt32(rgb[0]), Convert.ToInt32(rgb[1]), Convert.ToInt32(rgb[2]));
            return newCol;
        }

        public static string GetStringFromColor(Color col)
        {
            string r = col.R.ToString();
            string g = col.G.ToString();
            string b = col.B.ToString();
            return r + "," + g + "," + b;
        }

        private void BtnSave_Click(object sender, EventArgs e)
        {
            SQLiteConnection conn = new SQLiteConnection("Data Source=bookmarks.db;Version=3");
            conn.Open();

            string updateClickbaitColors = String.Format("update colors_clickbait set cb_heavy = '{0}', cb_moderate = '{1}', cb_slight = '{2}', cb_none = '{3}';", 
                GetStringFromColor(panHeavyCB.BackColor), GetStringFromColor(panModerateCB.BackColor), GetStringFromColor(panSlightCB.BackColor), GetStringFromColor(panNotCB.BackColor));

            SQLiteCommand cmd = new SQLiteCommand(updateClickbaitColors, conn);
            cmd.ExecuteNonQuery();

            string updateSatireColors = String.Format("update colors_satire set satirical = '{0}', notsatirical = '{1}';",
                GetStringFromColor(panSatire.BackColor), GetStringFromColor(panNotSatire.BackColor));

            cmd = new SQLiteCommand(updateSatireColors, conn);
            cmd.ExecuteNonQuery();

            string updateFalsColors = String.Format("update colors_falsifications set falsification = '{0}', notfalsification = '{1}';",
                GetStringFromColor(panFals.BackColor), GetStringFromColor(panNotFals.BackColor));

            cmd = new SQLiteCommand(updateFalsColors, conn);
            cmd.ExecuteNonQuery();

            conn.Close();

            FrmMain.CLICKBAIT_HEAVY_THRESHOLD = Convert.ToDouble(numHeavy.Value / 100);
            FrmMain.CLICKBAIT_MODERATE_THRESHOLD = Convert.ToDouble(numModerate.Value / 100);
            FrmMain.CLICKBAIT_SLIGHT_THRESHOLD = Convert.ToDouble(numSlight.Value / 100);

            MessageBox.Show("Settings will take effect for the next page.");

            this.Close();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void numHeavy_ValueChanged(object sender, EventArgs e)
        {

        }

        private void numModerate_ValueChanged(object sender, EventArgs e)
        {

        }

        private void numSlight_ValueChanged(object sender, EventArgs e)
        {

        }

        private void numLowNone_ValueChanged(object sender, EventArgs e)
        {

        }
    }
}
