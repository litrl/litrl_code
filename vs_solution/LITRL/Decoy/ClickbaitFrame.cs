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
using System.Collections.Generic;
using System.Linq;
using System.Drawing;
using System.Windows.Forms;

namespace Decoy
{
    public partial class ClickbaitFrame : UserControl
    {
        public ClickbaitFrame()
        {
            InitializeComponent();
            LstViewClickbait.Sorting = SortOrder.Ascending;
        }

        private int itemNum = 0;

        private Dictionary<int, List<string>> clickbaitResults = new Dictionary<int, List<string>>();

        //this is kind of a crappy way to store the user scores; it was an after thought so it was basically worked into
        //the existing code; the result is messy but again, it works
        private Dictionary<int, List<string>> clickbaitUserScoreResults = new Dictionary<int, List<string>>();
        public Dictionary<int, List<string>> ClickbaitUserScoreResults { get => clickbaitUserScoreResults; set => clickbaitUserScoreResults = value; }

        public void AddClickbaitToListViewAndDict(string clickbaitDetectorLine)
        {
            //split the input line from the detector
            char[] seps = { ',' };
            string[] items = clickbaitDetectorLine.Split(seps, 41);

            //create a list to store in the dictionary
            List<string> clickbaitScores = items.ToList<string>();

            //default values for user scores
            List<string> clickbaitUserScores = new List<string>();
            clickbaitUserScores.Add("0");
            clickbaitUserScores.Add("0");
            clickbaitUserScores.Add("No opinion");

            //set the clickbait scores for this text
            clickbaitResults[itemNum] = clickbaitScores;
            clickbaitUserScoreResults[itemNum] = clickbaitUserScores;

            string[] formattedItems = new string[3];
            formattedItems[0] = (Math.Round(Convert.ToDouble(items[0]), 2) * 100).ToString();
            formattedItems[1] = (Math.Round(Convert.ToDouble(items[1]), 2) * 100).ToString();
            formattedItems[2] = items[items.Length - 1];

            ListViewItem clickbaitItem = new ListViewItem(itemNum.ToString());
            clickbaitItem.UseItemStyleForSubItems = false;
            clickbaitItem.SubItems.Add("", Color.Black, GetColor(items[0]), this.Font);
            clickbaitItem.SubItems.Add(formattedItems[0]);
            clickbaitItem.SubItems.Add(formattedItems[1]);
            clickbaitItem.SubItems.Add(formattedItems[2]);

            LstViewClickbait.Items.Add(clickbaitItem);
            itemNum++;
        }

        public Color GetColor(string percentage)
        {
            double cbScore = Convert.ToDouble(percentage);

            if (cbScore >= FrmMain.CLICKBAIT_HEAVY_THRESHOLD)
            {
                return FrmColorSettings.GetColorFromString(FrmMain.CLICKBAIT_HEAVY_COLOR);
            }
            else if (cbScore >= FrmMain.CLICKBAIT_MODERATE_THRESHOLD)
            {
                return FrmColorSettings.GetColorFromString(FrmMain.CLICKBAIT_MODERATE_COLOR);
            }
            else if (cbScore >= FrmMain.CLICKBAIT_SLIGHT_THRESHOLD)
            {
                return FrmColorSettings.GetColorFromString(FrmMain.CLICKBAIT_SLIGHT_COLOR);
            }
            else if (cbScore > 0)
            {
                return FrmColorSettings.GetColorFromString(FrmMain.CLICKBAIT_LOW_COLOR);
            }
            return FrmColorSettings.GetColorFromString(FrmMain.CLICKBAIT_HEAVY_COLOR);
        }

        //potential refactor; leads to messy code
        public List<string> GetEntry(int count)
        {
            return clickbaitResults[count];
        }

        public Dictionary<int, List<string>> GetEntries()
        {
            return clickbaitResults;
        }

        public Dictionary<int, List<string>> GetUserScoreEntries()
        {
            return clickbaitUserScoreResults;
        }

        public void Reset()
        {
            itemNum = 0;
            clickbaitResults = new Dictionary<int, List<string>>();
            clickbaitUserScoreResults = new Dictionary<int, List<string>>();
            LstViewClickbait.Items.Clear();
        }

        private void LstViewClickbait_ColumnClick(object sender, ColumnClickEventArgs e)
        {
            if (LstViewClickbait.Columns[e.Column].Text == "Clickbait %" || LstViewClickbait.Columns[e.Column].Text == "Not %")
                this.LstViewClickbait.ListViewItemSorter = new ListViewItemComparer(e.Column);
        }
    }
}
