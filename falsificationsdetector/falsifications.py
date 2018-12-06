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
# Name:        falsifications
# Purpose:     main program for falsifications
#              can run this if you are working on the falsifications detector to test
#              additionally you need to run this module to generate the detector
#              .dill pickle file (in ./pickles) , which is used by the browser for falsifications detection
#
# Created:     05/01/2018
#
# Language and Information Technology Research Lab
# Faculty of Information and Media Studies (FIMS)
# University of Western Ontario, London, Canada
#-------------------------------------------------------------------------------

import dill
import cProfile, pstats, StringIO
from falsificationsml import falsificationDetector

def main():

    pr = cProfile.Profile()
    pr.enable()

    detector = falsificationDetector()
    detector.train()

    #dump (serialize) the detector object so we don't have to retrain every time
    #use a dump of the detector that has the highest observed accuracy
    detectorDUMP = open('pickles/falsification_detector.dill', 'wb')
    dill.dump(detector, detectorDUMP)
    detectorDUMP.close()
    pr.disable()

    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(30)
    print s.getvalue()

if __name__ == '__main__':
    main()
