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
using System.Windows.Forms;
using System.Collections.Generic;

namespace Decoy
{
    public partial class FrmCBEntryUserScore : Form
    {
        public FrmCBEntryUserScore(string id, string caption, string cbScore, string ncbScore, string userCbScore, string userNcbScore, string detectorAcc)
        {
            InitializeComponent();
            TxtCbCaption.Text = caption;
            LblDetectorClickbait.Text = (Math.Round(Convert.ToDouble(cbScore) * 100)).ToString();
            LblDetectorNotClickbait.Text = (Math.Round(Convert.ToDouble(ncbScore) * 100)).ToString();
            cboClickbaitDetectorAcc.Text = detectorAcc;
            numObservedClickbait.Value = Convert.ToInt32(userCbScore);
            numObservedNotClickbait.Value = Convert.ToInt32(userNcbScore);
        }

        public List<string> GetUserScores()
        {
            this.ShowDialog();
            List<string> userScores = new List<string>();
            userScores.Add(numObservedClickbait.Value.ToString());
            userScores.Add(numObservedNotClickbait.Value.ToString());
            userScores.Add(cboClickbaitDetectorAcc.Text);
            return userScores;
        }

        private void BtnOK_Click(object sender, EventArgs e)
        {
            DialogResult = DialogResult.OK;
        }
    }
}
