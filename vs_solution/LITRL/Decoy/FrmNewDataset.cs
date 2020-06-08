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
using System.Data.SQLite;

namespace Decoy
{
    public partial class FrmNewDataset : Form
    {
        public FrmNewDataset(FrmMain mainWnd)
        {
            InitializeComponent();
            mainWndRef = mainWnd;
        }

        private FrmMain mainWndRef;

        private void BtnCreateDataset_Click(object sender, EventArgs e)
        {
            if (TxtDatasetName.Text != "")
            {

                string newDataset = ".\\datasets\\" + TxtDatasetName.Text + ".db";
                SQLiteConnection.CreateFile(newDataset);

                string tblClickbait = @"CREATE TABLE `clickbait` (
	                `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	                `url`	TEXT NOT NULL,
                    `caption`	TEXT NOT NULL,
                    `userNotClickbaitScore` REAL,
                    `userClickbaitScore` REAL,
                    `userAccInterpretation` TEXT,
	                `cbscore`	REAL,
	                `ncbscore`	REAL,
                    `getWordCount` REAL,
                    `getWord2GramsAvgLen` REAL,
                    `getWord3GramsAvgLen` REAL,
                    `getHashTagsAndRTs` REAL,
                    `getQuestionMarks` REAL,
                    `getAtMentions` REAL,
                    `getNumbersSum` REAL,
                    `minDistToNNP` REAL,
                    `maxDistToNNP` REAL,
                    `getNNPLOCCount` REAL,
                    `getNNPPERSCount` REAL,
                    `getSwearCount` REAL,
                    `getAdjpCount` REAL,
                    `getAdvpCount` REAL,
                    `getNNPCount` REAL,
                    `getVerbCount` REAL,
                    `getNPsCount` REAL,
                    `avgDistToNNP` REAL,
                    `getCharLength` REAL,
                    `getPronounCount` REAL,
                    `getEmotiveness` REAL,
                    `getTimeWordsCount` REAL,
                    `getAcademicWordsCount` REAL,
                    `getFirstNNPPos` REAL,
                    `startsWithNumber` REAL,
                    `maxDistFromNPToNNP` REAL,
                    `NNPCountOverNPCount` REAL,
                    `lenOfLongestWord` REAL,
                    `maxDistToQuote` REAL,
                    `containsOn` REAL,
                    `minDistToOn` REAL,
                    `containsTriggers` REAL,
                    `npsPlusNNPsOverNumbersSum` REAL,
                    `maxDistToHashTag` REAL,
                    `maxDistToAt` REAL,
                    `firstPartContainsColon` REAL,
                    `determiners` REAL,
                    `nounSimilarity` REAL,
                    `minWordCount` INTEGER,
                    `htmltags` TEXT,
	                `timestamp`	DATETIME,
                    `datestamp` DATETIME
                );";

                SQLiteConnection conn = new SQLiteConnection("Data Source=" + newDataset + ";Version=3");
                conn.Open();

                SQLiteCommand cmd = new SQLiteCommand(tblClickbait, conn);
                cmd.ExecuteNonQuery();

                //satire
                string tblSatire = @" CREATE TABLE `satire` (
	                `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	                `url`	TEXT NOT NULL,
                    `content` TEXT NOT NULL,
                    `userNotSatireScore` REAL,
                    `userSatireScore` REAL,
                    `userAccInterpretation` TEXT,
                    `satireScore` REAL, 
                    `notSatireScore` REAL,
                    `absurdity` REAL,
                    `pronouns` REAL,
                    `personalPronouns` REAL,
                    `impersonalPronouns` REAL,
                    `prepositions` REAL,
                    `verbs` REAL,
                    `conjunctions` REAL,
                    `adverbs` REAL,
                    `adjectives` REAL,
                    `negativeEmotions` REAL,
                    `periods` REAL,
                    `commas` REAL,
                    `colons` REAL,
                    `semicolons` REAL,
                    `questionMarks` REAL,
                    `exclamations` REAL,
                    `quotes` REAL,
                    `htmltags` TEXT,
                    `timestamp`	DATETIME,
                    `datestamp` DATETIME
                );";

                cmd = new SQLiteCommand(tblSatire, conn);
                cmd.ExecuteNonQuery();

                //falsifications
                string tblFalsification = @" CREATE TABLE `falsification` (
	                `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	                `url`	TEXT NOT NULL,
                    `content` TEXT NOT NULL,
                    `userLegitScore` REAL,
                    `userFalseScore` REAL,
                    `userAccInterpretation` TEXT,
                    `legitScore` REAL,
                    `falseScore` REAL,
                    `paragraphsPerStory` REAL,
                    `avgWordLen` REAL,
                    `avgSentsPerPara` REAL, 
                    `avgWordsPerSent` REAL, 
                    `avgWordsPerPara` REAL,
                    `pausality` REAL,
                    `verifiableFacts` REAL,
                    `emotiveness` REAL,
                    `pronounCount` REAL,
                    `informality` REAL,
                    `lexicalDiversity` REAL,
                    `affect` REAL,
                    `htmltags` TEXT,
                    `timestamp`	DATETIME,
                    `datestamp` DATETIME
                );";

                cmd = new SQLiteCommand(tblFalsification, conn);
                cmd.ExecuteNonQuery();

                //saves the contents of the textbox in analysis
                string tblNotes = @" CREATE TABLE `notes` (
	                `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	                `url`	TEXT NOT NULL,
                    `notes` TEXT NOT NULL,
                    `timestamp`	DATETIME,
                    `datestamp` DATETIME
                );";

                cmd = new SQLiteCommand(tblNotes, conn);
                cmd.ExecuteNonQuery();

                conn.Close();

                TxtDatasetName.Text = "";

                MessageBox.Show("Dataset created!");

                mainWndRef.LastSelectedDataset = -1;

                DialogResult = DialogResult.OK;
            }
        }
    }
}
