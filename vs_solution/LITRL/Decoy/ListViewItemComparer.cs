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
using System.Collections;

namespace Decoy
{
    class ListViewItemComparer : IComparer
    {
        private int col;
        public ListViewItemComparer(int column)
        {
            col = column;
        }
        public int Compare(object x, object y)
        {
            int l = Convert.ToInt32(((ListViewItem)x).SubItems[col].Text);
            int r = Convert.ToInt32(((ListViewItem)y).SubItems[col].Text);

            if (l < r)
            {
                return -1;
            }
            else if (l == r)
            {
                return 0;
            }
            else
                return 1;
        }
    }
}
