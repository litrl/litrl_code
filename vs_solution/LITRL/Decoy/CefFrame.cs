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
using CefSharp;
using CefSharp.WinForms;

namespace Decoy
{
    public partial class CefFrame : UserControl
    {
        public CefFrame(string path = "", bool editor = false)
        {
            InitializeComponent();
            editMode = editor;

            CefSharpSettings.SubprocessExitIfParentProcessClosed = true;

            browser = new ChromiumWebBrowser(path)
            {
                Dock = DockStyle.Fill
            };
            this.Controls.Add(browser);
        }

        private bool editMode = false;

        ChromiumWebBrowser browser;

        public ChromiumWebBrowser Browser { get => browser; set => browser = value; }

        private void CefFrame_Load(object sender, EventArgs e)
        {
            if (editMode)
            {
                browser.LoadHtml("<html><body contentEditable='true'></body></html>", "http://yourinputdoc");
            }
        }
    }
}
