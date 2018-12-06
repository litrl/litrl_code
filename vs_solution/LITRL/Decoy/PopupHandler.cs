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

namespace Decoy
{
    public class PopupHandler : ILifeSpanHandler
    {
        public String lastURL;

        public PopupHandler(String lasturl)
        {
            lastURL = lasturl;
        }

        public bool DoClose(IWebBrowser browserControl, IBrowser browser)
        {
            return false;
        }

        public void OnAfterCreated(IWebBrowser browserControl, IBrowser browser)
        {
            return;
        }

        public void OnBeforeClose(IWebBrowser browserControl, IBrowser browser)
        {
            return;
        }

        bool ILifeSpanHandler.OnBeforePopup(IWebBrowser browserControl, IBrowser browser, IFrame frame, string targetUrl, string targetFrameName, WindowOpenDisposition targetDisposition, bool userGesture, IPopupFeatures popupFeatures, IWindowInfo windowInfo, IBrowserSettings browserSettings, ref bool noJavascriptAccess, out IWebBrowser newBrowser)
        {
            newBrowser = null;

            DialogResult res = MessageBox.Show("A popup is attempting to open from the address: " + Environment.NewLine + targetUrl +
                Environment.NewLine + Environment.NewLine + 
                "Would you like to open it in the main browser window? (this will close the current page)",
                "Litrl Browser Popup", MessageBoxButtons.YesNo, MessageBoxIcon.Question);

            if (res == DialogResult.Yes)
            {
                lastURL = "";
                browserControl.Load(targetUrl);
            }

            //return true closes the popup, false opens it
            return true;
        }
    }
}