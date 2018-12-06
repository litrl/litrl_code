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

namespace Decoy
{
    public partial class FrmSelectHtmlTags : Form
    {
        public FrmSelectHtmlTags(string[] initialTags)
        {
            InitializeComponent();

            //set the initial tag selections in the list box
            for (int i = 0; i < LstHtmlTags.Items.Count; ++i)
            {
                for (int j = 0; j < initialTags.Length; ++j)
                {
                    if (LstHtmlTags.Items[i].ToString() == initialTags[j])
                    {
                        LstHtmlTags.SetSelected(i, true);
                    }
                }
            }
        }

        public string GetXPathTags()
        {
            string xpathTags = "";
            for (int i = 0; i < LstHtmlTags.SelectedItems.Count; ++i)
            {
                if (xpathTags == "")
                {
                    xpathTags = "//" + LstHtmlTags.SelectedItems[i];
                }
                else
                {
                    xpathTags += " | //" + LstHtmlTags.SelectedItems[i];
                }
            }
            return xpathTags;
        }

        public string GetJSTags(string JSstart, string JSend)
        {
            string JStags = "";
            for (int i = 0; i < LstHtmlTags.SelectedItems.Count; ++i)
            {
                JStags += JSstart + LstHtmlTags.SelectedItems[i] + JSend + Environment.NewLine;
            }
            return JStags;
        }

        private void BtnOK_Click(object sender, EventArgs e)
        {
            FrmMain.SATIRE_TAG_TEXT_MIN_CHAR_LENGTH = Convert.ToInt32(numSatireLength.Value);
            FrmMain.FALSIFICATION_TAG_TEXT_MIN_CHAR_LENGTH = Convert.ToInt32(numFalsificationLength.Value);
            GrpFals.Hide();
            GrpSatire.Hide();
            DialogResult = DialogResult.OK;
        }

        private void FrmSelectHtmlTags_Load(object sender, EventArgs e)
        {
            numSatireLength.Value = Convert.ToDecimal(FrmMain.SATIRE_TAG_TEXT_MIN_CHAR_LENGTH);
            numFalsificationLength.Value = Convert.ToDecimal(FrmMain.FALSIFICATION_TAG_TEXT_MIN_CHAR_LENGTH);
        }

        public void ShowSatireCharLength()
        {
            GrpSatire.Show();
        }

        public void ShowFalsCharLength()
        {
            GrpFals.Show();
        }
    }
}
