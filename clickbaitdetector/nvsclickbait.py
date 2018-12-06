'''
    Copyright Victoria L. Rubin 2017-2018.

    This file is part of Litrl Browser.

    Litrl Browser is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Litrl Browser is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Litrl Browser.  If not, see <https://www.gnu.org/licenses/>.
'''

#-------------------------------------------------------------------------------
# Name:        nvsclickbait
# Purpose:     news verification suite clickbait entry point
#              run this from the browser, not clickbait.py
#              if you DO NOT have a serialized clickbait detector, please run
#              clickbait.py first with training sets to obtain this
#
# Created:     09/09/2017
#
# Language and Information Technology Research Lab
# Faculty of Information and Media Studies (FIMS)
# University of Western Ontario, London, Canada
#-------------------------------------------------------------------------------

import sys
import dill

from clickbaitml import clickbaitDetector

def main():
    detectorDUMP = open('pickles/clickbait_detector.dill', 'rb')
    detector = dill.load(detectorDUMP)

    while True:
        headline = raw_input()
        headline = unicode(headline, errors='ignore')
        print detector.predict(headline, verbose=False)
        sys.stdout.flush() #so the nvs browser gets the output... windows buffering won't print stuff without this line

if __name__ == '__main__':
    main()
