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
using System.Data.SQLite;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Windows.Forms;
using System.Linq;
using ZedGraph;

namespace Decoy
{
    public partial class FrmStatistics : Form
    {
        public FrmStatistics(FrmMain mainWnd)
        {
            InitializeComponent();
            for (int i = 0; i < clickbaitFeatures.Length; ++i)
            {
                clickbaitFeatures[i] = (i + 1).ToString() + ". " + clickbaitFeatures[i];
            }
            newDataset = new FrmNewDataset(mainWnd);
        }

        //from a run of only the clickbait challenge validation set without bags of anything
        private double[] AVG_CLICKBAIT_SCORES = { 8.913103448275862, 8.203793103448277, 11.766206896551724, 0.10344827586206896, 0.1279310344827586, 0.040344827586206895, 11.579310344827586, 0.8413793103448276, 1.5517241379310345, 0.028620689655172414, 0.029655172413793104, 1.4310344827586208, 0.846551724137931, 0.5172413793103449, 0.6727586206896552, 1.6293103448275863, 2.2751724137931033, 11.534281609195403, 53.540689655172415, 0.613103448275862, 0.38575980245807906, 0.1403448275862069, 0.15172413793103448, 1.2872413793103448, 0.1306896551724138, -0.6782758620689655, 0.24586206896551724, 8.536206896551723, 1.7841379310344827, 0.3368965517241379, 10.686206896551724, 211.10344827586206, 5.7924137931034485, 2.149655172413793, 1.7682758620689656, 0.36551724137931035, 0.7137931034482758, 0.10417638226747215 };
        private double[] AVG_NOT_CLICKBAIT_SCORES = { 12.138620689655172, 9.714827586206896, 14.68551724137931, 0.1703448275862069, 0.009655172413793104, 0.12103448275862069, 12.127586206896552, 0.843103448275862, 3.6241379310344826, 0.23482758620689656, 0.09448275862068965, 1.6310344827586207, 0.9868965517241379, 0.2986206896551724, 2.366206896551724, 1.9258620689655173, 3.2324137931034485, 18.896876026272587, 77.31103448275861, 0.2710344827586207, 0.28143231576852257, 0.12620689655172415, 0.2610344827586207, 1.803448275862069, 0.00896551724137931, 2.797586206896552, 0.7344827586206897, 10.060689655172414, 4.212068965517242, 0.5658620689655173, 19.729310344827585, 175.58620689655172, 17.796206896551723, 5.344137931034483, 4.310344827586207, 0.7103448275862069, 0.4996551724137931, 0.21919334644559002 };

        //from a run of our dataset
        private double[] AVG_SATIRE_SCORES = { 70.53336302049334, 49.20040627554768, 21.332956744945644, 201.69510764023823, 220.03358590018328, 219.78624191933096, 26.164302389955438, 28.96889543684623, 0.0, 211.20617726138425, 92.67010190268833, 4.2890214494190175, 0.6253269503603729, 1.4115916090366991, 0.5356246386538932, 0.0 };
        private double[] AVG_NOT_SATIRE_SCORES = { 94.99128045207216, 64.96627312053467, 30.025007331537502, 185.74279066977405, 225.8820817881384, 200.193224348379, 31.44596341155374, 31.99081107118283, 0.0, 211.71032078182446, 86.37133625975662, 2.3072740352432044, 0.8894542250499441, 3.0490297314312476, 3.595737910353116, 0.0 };

        //from a run of our dataset
        private double[] AVG_FALSIFICATION_SCORES = { 97.26666666666667, 11.011653103424036, 54.941977981140525, 109.3424811910611, 414.7253418196297, 18.04031969418325, 0.0, 2.972117545692954, 11.746823364612005, 0.1910825545341996, 17.85999955391857, 1.6766666666666665, 1.3211111111111111, 1.3607789807363118, 263.6 };
        private double[] AVG_LEGIT_SCORES = { 214.4, 11.715254971813241, 29.075697003216604, 134.15321785189903, 341.25002159001065, 20.106814777585328, 0.0, 2.677282396531567, 10.313342751134087, 0.1306445626320444, 21.204745754066558, 1.4444444444444444, 0.8777777777777778, 1.068371559806112, 463.3333333333333 };

        private void FillDatasetSelections()
        {
            CboDSBox1.Items.Clear();
            string[] datasets = Directory.GetFiles(".\\datasets");
            foreach (string fileName in datasets)
            {
                if (fileName.EndsWith(".db") == true)
                {
                    CboDSBox1.Items.Add(fileName);
                }
            }
        }

        private FrmNewDataset newDataset;
        private void BtnNewDS_Click(object sender, EventArgs e)
        {
            newDataset.ShowDialog();
            FillDatasetSelections();
        }

        private CultureInfo provider = CultureInfo.InvariantCulture;

        private FrmSelectWebsites websitesDs1 = new FrmSelectWebsites();

        private Random rand = new Random();

        private void UpdateTimelineGraphDataset()
        {
            zedGraphStats.GraphPane.Title.Text = "";
            zedGraphStats.GraphPane.CurveList.Clear();
            zedGraphStats.GraphPane.GraphObjList.Clear();

            if (RadClickbait.Checked == true)
            {
                zedGraphStats.GraphPane.Title.Text = "Clickbait";

                SQLiteConnection conn = new SQLiteConnection("Data Source=" + CboDSBox1.Items[CboDSBox1.SelectedIndex] + ";Version=3");

                conn.Open();

                if (ds1URLs.Count > 0)
                {
                    foreach (string url in ds1URLs)
                    {
                        if (RadDay.Checked == true)
                        {
                            GraphSelectedDatasetDay(conn, "select avg(cbscore), min(cbscore), max(cbscore), avg(ncbscore), min(ncbscore), max(ncbscore), datestamp from clickbait where url = '{0}' group by datestamp", url);
                        }
                        else
                        {
                            //todo
                        }
                    }
                }

                conn.Close();
            }
            else if (RadSatire.Checked == true)
            {
                zedGraphStats.GraphPane.Title.Text = "Satire";

                SQLiteConnection conn = new SQLiteConnection("Data Source=" + CboDSBox1.Items[CboDSBox1.SelectedIndex] + ";Version=3");

                conn.Open();

                if (ds1URLs.Count > 0)
                {
                    foreach (string url in ds1URLs)
                    {
                        if (RadDay.Checked == true)
                        {
                            GraphSelectedDatasetDay(conn, "select avg(notSatireScore), min(notSatireScore), max(notSatireScore), avg(satireScore), min(satireScore), max(satireScore), datestamp from satire where url = '{0}' group by datestamp", url);
                        }
                        else
                        {
                            //todo
                        }
                    }
                }

                conn.Close();
            }
            else if (RadFalsifications.Checked == true)
            {
                zedGraphStats.GraphPane.Title.Text = "Falsifications";

                SQLiteConnection conn = new SQLiteConnection("Data Source=" + CboDSBox1.Items[CboDSBox1.SelectedIndex] + ";Version=3");

                conn.Open();

                if (ds1URLs.Count > 0)
                {
                    foreach (string url in ds1URLs)
                    {
                        if (RadDay.Checked == true)
                        {
                            GraphSelectedDatasetDay(conn, "select avg(legitScore), min(legitScore), max(legitScore), avg(falseScore), min(falseScore), max(falseScore), datestamp from falsification where url = '{0}' group by datestamp", url);
                        }
                        else
                        {
                            //todo
                        }
                    }
                }

                conn.Close();
            }

            zedGraphStats.RestoreScale(zedGraphStats.GraphPane);
            zedGraphStats.AxisChange();
            zedGraphStats.Refresh();
        }

        private void GraphSelectedDatasetDay(SQLiteConnection conn, string sqlString, string whereUrlEq = "")
        {
            TxtDBOutput.Clear();
            SQLiteCommand cmd = new SQLiteCommand(String.Format(sqlString, whereUrlEq), conn);
            SQLiteDataReader reader = cmd.ExecuteReader();

            double min = 1;
            double max = 1;

            List<string> xLabels = new List<string>();
            List<string> xVals = new List<string>();
            List<string> yVals = new List<string>();

            Dictionary<int, string> labels = new Dictionary<int, string>();
            labels.Add(0, "Min Deceptive (CB/Satire/Fals.)");
            labels.Add(1, "Min Not Deceptive (Not CB/Not Satire/Legit)");
            labels.Add(2, "Avg Deceptive (CB/Satire/Fals.)");
            labels.Add(3, "Avg Not Deceptive (Not CB/Not Satire/Legit)");
            labels.Add(4, "Max Deceptive (CB/Satire/Fals.)");
            labels.Add(5, "Max Not Deceptive (Not CB/Not Satire/Legit)");

            Dictionary<string, Color> barColors = new Dictionary<string, Color>();
            barColors.Add("Min Deceptive (CB/Satire/Fals.)", Color.Green);
            barColors.Add("Min Not Deceptive (Not CB/Not Satire/Legit)", Color.LightGreen);
            barColors.Add("Avg Deceptive (CB/Satire/Fals.)", Color.Blue);
            barColors.Add("Avg Not Deceptive (Not CB/Not Satire/Legit)", Color.LightBlue);
            barColors.Add("Max Deceptive (CB/Satire/Fals.)", Color.DarkMagenta);
            barColors.Add("Max Not Deceptive (Not CB/Not Satire/Legit)", Color.Magenta);

            while (reader.Read())
            {
                string avgFirst = reader.GetDouble(0).ToString();
                string minFirst = reader.GetDouble(1).ToString();
                string maxFirst = reader.GetDouble(2).ToString();
                string avgSecond = reader.GetDouble(3).ToString();
                string minSecond = reader.GetDouble(4).ToString();
                string maxSecond = reader.GetDouble(5).ToString();
                string timestamp = reader.GetString(6);
                DateTime datestampParsed = DateTime.Parse(timestamp, provider);

                int keyFromTimestamp = -1;
                if (RadDay.Checked == true)
                {
                    keyFromTimestamp = datestampParsed.DayOfYear;
                    xLabels.Add(datestampParsed.ToShortDateString());
                }
                else if (RadMonth.Checked == true)
                {
                    keyFromTimestamp = datestampParsed.Month;
                    //todo: add format for month here
                }

                #region "Bad code that makes the timeline work for now"

                //NOTE: I am really not happy with the following messy copy+paste fix to get the graph working - it needs cleaned up - but it works

                if (ChkMinimum.Checked == true)
                {
                    if (ActiveGroupShowGoodValue())
                    {
                        xVals.Add(keyFromTimestamp.ToString());
                        yVals.Add(minFirst);
                    }
                    else
                    {
                        xVals.Add(keyFromTimestamp.ToString());
                        yVals.Add("0");
                    }
                    if (ActiveGroupShowBadValue())
                    {
                        xVals.Add(keyFromTimestamp.ToString());
                        yVals.Add(minSecond);
                    }
                    else
                    {
                        xVals.Add(keyFromTimestamp.ToString());
                        yVals.Add("0");
                    }
                }
                else
                {
                    xVals.Add(keyFromTimestamp.ToString());
                    yVals.Add("0");
                    xVals.Add(keyFromTimestamp.ToString());
                    yVals.Add("0");
                }

                if (ChkMean.Checked == true)
                {
                    if (ActiveGroupShowGoodValue())
                    {
                        xVals.Add(keyFromTimestamp.ToString());
                        yVals.Add(avgFirst);
                    }
                    else
                    {
                        xVals.Add(keyFromTimestamp.ToString());
                        yVals.Add("0");
                    }
                    if (ActiveGroupShowBadValue())
                    {
                        xVals.Add(keyFromTimestamp.ToString());
                        yVals.Add(avgSecond);
                    }
                    else
                    {
                        xVals.Add(keyFromTimestamp.ToString());
                        yVals.Add("0");
                    }
                }
                else
                {
                    xVals.Add(keyFromTimestamp.ToString());
                    yVals.Add("0");
                    xVals.Add(keyFromTimestamp.ToString());
                    yVals.Add("0");
                }

                if (ChkMaximum.Checked == true)
                {
                    if (ActiveGroupShowGoodValue())
                    {
                        xVals.Add(keyFromTimestamp.ToString());
                        yVals.Add(maxFirst);
                    }
                    else
                    {
                        xVals.Add(keyFromTimestamp.ToString());
                        yVals.Add("0");
                    }
                    if (ActiveGroupShowBadValue())
                    {
                        xVals.Add(keyFromTimestamp.ToString());
                        yVals.Add(maxSecond);
                    }
                    else
                    {
                        xVals.Add(keyFromTimestamp.ToString());
                        yVals.Add("0");
                    }
                }
                else
                {
                    xVals.Add(keyFromTimestamp.ToString());
                    yVals.Add("0");
                    xVals.Add(keyFromTimestamp.ToString());
                    yVals.Add("0");
                }

                #endregion
            }

            max = xVals.Count;

            Dictionary<string, PointPairList> allVals = new Dictionary<string, PointPairList>();

            for (int i = 0; i < xVals.Count; ++i)
            {
                if (allVals.ContainsKey(labels[i % labels.Count]) == false)
                {
                    allVals[labels[i % labels.Count]] = new PointPairList();
                }

                allVals[labels[i % labels.Count]].Add(new PointPair(Convert.ToDouble(xVals[i]), Convert.ToDouble(yVals[i])));
            }

            foreach (KeyValuePair<string, PointPairList> kv in allVals)
            {
                BarItem scatterPlot = zedGraphStats.GraphPane.AddBar(kv.Key, kv.Value, barColors[kv.Key]);
                scatterPlot.Bar.Fill.RangeMin = min;
                scatterPlot.Bar.Fill.RangeMax = max;
            }

            string[] dateLabels = xLabels.Distinct().ToArray();
            zedGraphStats.GraphPane.XAxis.Title = new AxisLabel("Timestamp", "Consolas", 12, Color.Black, true, false, false);
            zedGraphStats.GraphPane.XAxis.Type = AxisType.Text;
            zedGraphStats.GraphPane.XAxis.Scale.TextLabels = dateLabels;

            //write sql output
            for(int i = 0; i < dateLabels.Length; ++i)
            {
                TxtDBOutput.Text += dateLabels[i] + Environment.NewLine;
                foreach (KeyValuePair<string, PointPairList> kv in allVals)
                {
                    TxtDBOutput.Text += kv.Key + ": " + kv.Value[i] + Environment.NewLine;
                }
            }
        }

        private void GraphSelectedDatasetMonth()
        {
            throw new NotImplementedException();
        }

        private void CboDSBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
        }

        private void FrmStatistics_Load(object sender, EventArgs e)
        {
            FillDatasetSelections();
        }

        private void BtnSaveTimeline_Click(object sender, EventArgs e)
        {
            zedGraphStats.SaveAs();
        }

        private void RadDay_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
        }

        private void RadMonth_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
        }

        private List<string> ds1URLs = new List<string>();

        private void BtnSelectWebsitesDs1_Click(object sender, EventArgs e)
        {
            if (CboDSBox1.SelectedIndex == -1)
            {
                MessageBox.Show("No dataset has been selected.");
                return;
            }

            SQLiteConnection conn = new SQLiteConnection("Data Source=" + CboDSBox1.Items[CboDSBox1.SelectedIndex] + ";Version=3");
            conn.Open();

            SQLiteCommand cmd = new SQLiteCommand("select distinct url from clickbait", conn);
            SQLiteDataReader reader = cmd.ExecuteReader();

            websitesDs1.LstWebsites.Items.Clear();

            while (reader.Read())
            {
                websitesDs1.LstWebsites.Items.Add(reader.GetString(0));
            }

            websitesDs1.ShowDialog();

            List<string> urls = new List<string>();

            foreach (string url in websitesDs1.LstWebsites.SelectedItems)
            {
                urls.Add(url.Replace("'", "''"));
            }

            ds1URLs = urls;

            UpdateTimelineGraphDataset();
        }

        private void ResetChkBoxes()
        {
            ChkCbScore.Checked = false;
            ChkNcbScore.Checked = false;
            ChkSatireScore.Checked = false;
            ChkNotSatireScore.Checked = false;
            ChkTruthScore.Checked = false;
            ChkFalseScore.Checked = false;
        }

        private void RadClickbait_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
            ResetChkBoxes();
            GrpStatsClickbait.Enabled = true;
            GrpStatsSatire.Enabled = false;
            GrpStatsFalsifications.Enabled = false;
        }

        private void RadSatire_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
            ResetChkBoxes();
            GrpStatsClickbait.Enabled = false;
            GrpStatsSatire.Enabled = true;
            GrpStatsFalsifications.Enabled = false;
        }

        private void RadFalsifications_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
            ResetChkBoxes();
            GrpStatsClickbait.Enabled = false;
            GrpStatsSatire.Enabled = false;
            GrpStatsFalsifications.Enabled = true;
        }

        private bool ActiveGroupShowGoodValue()
        {
            if (GrpStatsClickbait.Enabled == true)
            {
                return ChkCbScore.Checked;
            }
            else if (GrpStatsSatire.Enabled == true)
            {
                return ChkSatireScore.Checked;
            }
            else
            {
                return ChkTruthScore.Checked;
            }
        }

        private bool ActiveGroupShowBadValue()
        {
            if (GrpStatsClickbait.Enabled == true)
            {
                return ChkNcbScore.Checked;
            }
            else if (GrpStatsSatire.Enabled == true)
            {
                return ChkNotSatireScore.Checked;
            }
            else
            {
                return ChkFalseScore.Checked;
            }
        }

        private void ChkMean_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
        }

        private void ChkMinimum_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
        }

        private void ChkMaximum_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
        }

        private void ChkCbScore_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
        }

        private void ChkNcbScore_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
        }

        private void ChkSatireScore_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
        }

        private void ChkNotSatireScore_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
        }

        private void ChkTruthScore_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
        }

        private void ChkFalseScore_CheckedChanged(object sender, EventArgs e)
        {
            UpdateTimelineGraphDataset();
        }

        private void FrmStatistics_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (e.CloseReason == CloseReason.UserClosing)
            {
                e.Cancel = true;
                Hide();
            }
        }

        string[] clickbaitFeatures = { "getWordCount", "getWord2GramsAvgLen", "getWord3GramsAvgLen", "getHashTagsAndRTs", "getQuestionMarks", "getAtMentions", "getNumbersSum", "minDistToNNP", "maxDistToNNP", "getNNPLOCCount", "getNNPPERSCount", "getSwearCount", "getAdjpCount", "getAdvpCount", "getNNPCount", "getVerbCount", "getNPsCount", "avgDistToNNP", "getCharLength", "getPronounCount", "getEmotiveness", "getTimeWordsCount", "getAcademicWordsCount", "getFirstNNPPos", "startsWithNumber", "maxDistFromNPToNNP", "NNPCountOverNPCount", "lenOfLongestWord", "maxDistToQuote", "containsOn", "minDistToOn", "containsTriggers", "npsPlusNNPsOverNumbersSum", "maxDistToHashTag", "maxDistToAt", "firstPartContainsColon", "determiners", "nounSimilarity"};

        public void ShowClickbaitDetails(List<string> cbResult)
        {
            TabStats.SelectTab(1);
            dataGridViewClickbait.Rows.Clear();
            zedGraphClickbaitDetails.GraphPane.CurveList.Clear();
            zedGraphClickbaitDetails.GraphPane.GraphObjList.Clear();

            List<double> featureVals = new List<double>();
            double clickbaitScore = 0;

            //this for loop is a mess. Had to remove the 3 features listed above because the numbers make the graph look weird
            int j = 0;
            for (int i = 0; i < cbResult.Count; ++i)
            {
                if (i == cbResult.Count - 1)
                {
                    TxtClickbait.Text = cbResult[i];
                    break;
                }

                if (i == 0)
                {
                    clickbaitScore = Convert.ToDouble(cbResult[i]);
                }
                else if (i == 1)
                {
                    continue;
                }
                else
                {
                    dataGridViewClickbait.Rows.Add(clickbaitFeatures[j], cbResult[i]);
                    ++j;
                    featureVals.Add(Convert.ToDouble(cbResult[i]));
                }
            }

            zedGraphClickbaitDetails.GraphPane.BarSettings.Base = BarBase.Y;

            zedGraphClickbaitDetails.GraphPane.YAxis.Scale.TextLabels = clickbaitFeatures;
            zedGraphClickbaitDetails.GraphPane.YAxis.Type = AxisType.Text;
            zedGraphClickbaitDetails.GraphPane.Title.Text = "Text on page (colored by clickbait level)";
            zedGraphClickbaitDetails.GraphPane.XAxis.Title = new AxisLabel("Feature Score", "Consolas", 12, Color.Black, true, false, false);
            zedGraphClickbaitDetails.GraphPane.YAxis.Title = new AxisLabel("Feature Name", "Consolas", 12, Color.Black, true, false, false);

            zedGraphClickbaitDetails.GraphPane.YAxis.Scale.FontSpec.Size = 7.0f;
            zedGraphClickbaitDetails.GraphPane.YAxis.Scale.FontSpec.Angle = 90;

            Color clickbaitColor = GetClickbaitScoreColor(clickbaitScore);

            zedGraphClickbaitDetails.GraphPane.AddCurve("AVG. Clickbait Score", AVG_CLICKBAIT_SCORES, null, Color.Red);
            zedGraphClickbaitDetails.GraphPane.AddCurve("AVG. Not Clickbait Score", AVG_NOT_CLICKBAIT_SCORES, null, Color.Green);
            zedGraphClickbaitDetails.GraphPane.AddBar(TxtClickbait.Text, featureVals.ToArray(), null, clickbaitColor);
            zedGraphClickbaitDetails.AxisChange();
            zedGraphClickbaitDetails.Refresh();
        }

        public Color GetClickbaitScoreColor(double clickbaitScore)
        {
            if (clickbaitScore >= FrmMain.CLICKBAIT_HEAVY_THRESHOLD)
            {
                return FrmColorSettings.GetColorFromString(FrmMain.CLICKBAIT_HEAVY_COLOR);
            }
            else if (clickbaitScore >= FrmMain.CLICKBAIT_MODERATE_THRESHOLD)
            {
                return FrmColorSettings.GetColorFromString(FrmMain.CLICKBAIT_MODERATE_COLOR);
            }
            else if (clickbaitScore >= FrmMain.CLICKBAIT_SLIGHT_THRESHOLD)
            {
                return FrmColorSettings.GetColorFromString(FrmMain.CLICKBAIT_SLIGHT_COLOR);
            }
            else if (clickbaitScore > 0)
            {
                return FrmColorSettings.GetColorFromString(FrmMain.CLICKBAIT_LOW_COLOR);
            }
            return FrmColorSettings.GetColorFromString(FrmMain.CLICKBAIT_HEAVY_COLOR);
        }

        //FIXMEUP: sort of works OK, not implemented for satire or falsifications
        public void CompareClickbaitDetails(int index)
        {
            List<double> featureVals = new List<double>();
            double clickbaitScore = Convert.ToDouble(otherClickbaitDetails[index][0]); //clickbait score is the first item in this list
            string text = "";

            for (int i = 2; i < otherClickbaitDetails[index].Count - 1; ++i)
            {
                if (i == otherClickbaitDetails[index].Count - 1)
                {
                    text = otherClickbaitDetails[index][i];
                    break;
                }

                featureVals.Add(Convert.ToDouble(otherClickbaitDetails[index][i]));
            }

            zedGraphClickbaitDetails.GraphPane.AddBar(otherClickbaitDetails[index][otherClickbaitDetails[index].Count - 1], featureVals.ToArray(), null, GetClickbaitScoreColor(clickbaitScore));
            zedGraphClickbaitDetails.AxisChange();
            zedGraphClickbaitDetails.Refresh();
        }

        private Dictionary<int, List<string>> otherClickbaitDetails = new Dictionary<int, List<string>>();

        public void ShowOtherClickbaitDetails(Dictionary<int, List<string>> entries)
        {
            this.otherClickbaitDetails = entries;
            LstOtherClickbaitTexts.Items.Clear();
            for (int i = 0; i < entries.Count; ++i)
            {
                string clickbaitScore = "";
                string notClickbaitScore = "";
                for (int j = 0; j < entries[i].Count; ++j)
                {
                    if (j == 0)
                    {
                        clickbaitScore = entries[i][j];
                    }
                    else if (j == 1)
                    {
                        notClickbaitScore = entries[i][j];
                    }
                    else if (j == entries[i].Count - 1)
                    {
                        LstOtherClickbaitTexts.Items.Add(entries[i][j] + "," + clickbaitScore + "," + notClickbaitScore);
                    }
                }
            }
        }

        private void LstOtherTexts_SelectedIndexChanged(object sender, EventArgs e)
        {
            foreach (int index in LstOtherClickbaitTexts.SelectedIndices)
            {
                CompareClickbaitDetails(index);
            }
        }

        string[] satireFeatures = { "Pronouns", "Personal Pronouns ", "Impersonal Pronouns", "Prepositions", "Verbs", "Conjunctions", "Adverbs", "Adjectives", "Negative Emotions", "Periods", "Commas", "Colons", "Semicolons", "Question Marks", "Exclamations", "Quotes" };

        public void ShowSatireDetails(List<string> satResult, string textProcessed)
        {
            TabStats.SelectTab(2);
            dataGridViewSatire.Rows.Clear();
            zedGraphSatireDetails.GraphPane.CurveList.Clear();
            zedGraphSatireDetails.GraphPane.GraphObjList.Clear();
            RtbSatireText.Text = textProcessed;

            List<double> featureVals = new List<double>();
            double satireScore = 0;

            int j = 0;
            for (int i = 0; i < satResult.Count; ++i)
            {
                if (i == 0)
                {
                    satireScore = Convert.ToDouble(satResult[i]);
                }
                else if (i == 1 || i == 2 || i == 3)
                {
                    continue;
                }
                else
                {
                    dataGridViewSatire.Rows.Add(satireFeatures[j], satResult[i]);
                    ++j;
                    featureVals.Add(Convert.ToDouble(satResult[i]));
                }
            }

            zedGraphSatireDetails.GraphPane.BarSettings.Base = BarBase.Y;

            zedGraphSatireDetails.GraphPane.YAxis.Scale.TextLabels = satireFeatures;
            zedGraphSatireDetails.GraphPane.YAxis.Type = AxisType.Text;
            zedGraphSatireDetails.GraphPane.Title.Text = "Text on page (colored by satire level)";
            zedGraphSatireDetails.GraphPane.XAxis.Title = new AxisLabel("Feature Score", "Consolas", 12, Color.Black, true, false, false);
            zedGraphSatireDetails.GraphPane.YAxis.Title = new AxisLabel("Feature Name", "Consolas", 12, Color.Black, true, false, false);

            zedGraphSatireDetails.GraphPane.YAxis.Scale.FontSpec.Size = 7.0f;
            zedGraphSatireDetails.GraphPane.YAxis.Scale.FontSpec.Angle = 90;

            Color satireColor = GetClickbaitScoreColor(satireScore); //fix me

            zedGraphSatireDetails.GraphPane.AddCurve("AVG. Satire Score", AVG_SATIRE_SCORES, null, Color.Red);
            zedGraphSatireDetails.GraphPane.AddCurve("AVG. Not Satire Score", AVG_NOT_SATIRE_SCORES, null, Color.Green);
            zedGraphSatireDetails.GraphPane.AddBar("Selected Text", featureVals.ToArray(), null, satireColor);
            zedGraphSatireDetails.AxisChange();
            zedGraphSatireDetails.Refresh();
        }

        string[] FalsificationFeatures = { "Paragraphs Per Story", "Avg Word Len", "Avg Num of Sents/Paragraph", "Avg Num of Words/Sent", "Avg Num of Words Per Para", "Pausality", "Verifiable Facts", "Emotiveness", "Pronoun Count", "Informality", "Lexical Diversity", "Affect", "Ambiguity", "Interrogative Pronouns", "Forward Referencing" };

        public void ShowFalsificationDetails(List<string> falsResult, string textProcessed)
        {
            TabStats.SelectTab(3);
            dataGridViewFalsification.Rows.Clear();
            zedGraphFalsificationDetails.GraphPane.CurveList.Clear();
            zedGraphFalsificationDetails.GraphPane.GraphObjList.Clear();
            RtbFalsificationText.Text = textProcessed;

            List<double> featureVals = new List<double>();
            double FalsificationScore = 0;

            int j = 0;
            for (int i = 0; i < falsResult.Count; ++i)
            {
                if (i == 0)
                {
                    FalsificationScore = Convert.ToDouble(falsResult[i]);
                }
                else if (i == 1)
                {
                    continue;
                }
                else
                {
                    dataGridViewFalsification.Rows.Add(FalsificationFeatures[j], falsResult[i]);
                    ++j;
                    featureVals.Add(Convert.ToDouble(falsResult[i]));
                }
            }

            zedGraphFalsificationDetails.GraphPane.BarSettings.Base = BarBase.Y;

            zedGraphFalsificationDetails.GraphPane.YAxis.Scale.TextLabels = FalsificationFeatures;
            zedGraphFalsificationDetails.GraphPane.YAxis.Type = AxisType.Text;
            zedGraphFalsificationDetails.GraphPane.Title.Text = "Text on page (colored by Falsification level)";
            zedGraphFalsificationDetails.GraphPane.XAxis.Title = new AxisLabel("Feature Score", "Consolas", 12, Color.Black, true, false, false);
            zedGraphFalsificationDetails.GraphPane.YAxis.Title = new AxisLabel("Feature Name", "Consolas", 12, Color.Black, true, false, false);

            zedGraphFalsificationDetails.GraphPane.YAxis.Scale.FontSpec.Size = 7.0f;
            zedGraphFalsificationDetails.GraphPane.YAxis.Scale.FontSpec.Angle = 90;

            Color FalsificationColor = GetClickbaitScoreColor(FalsificationScore); //fix me

            zedGraphFalsificationDetails.GraphPane.AddCurve("AVG. Falsification Score", AVG_FALSIFICATION_SCORES, null, Color.Red);
            zedGraphFalsificationDetails.GraphPane.AddCurve("AVG. Legitimate Score", AVG_LEGIT_SCORES, null, Color.Green);
            zedGraphFalsificationDetails.GraphPane.AddBar("Selected Text", featureVals.ToArray(), null, FalsificationColor);
            zedGraphFalsificationDetails.AxisChange();
            zedGraphFalsificationDetails.Refresh();
        }
    }
}
