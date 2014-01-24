"""
    Copyright (C) 2014  Andrew MacDonald

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import argparse
import datetime
import json

from matplotlib import pyplot as plt
import numpy as np

class DieCounter(object):
    def __init__(self, savefile):
        self.savefile = savefile

        fig=plt.figure()
        self.ax1 = plt.subplot(2,1,1)
        self.ax2 = plt.subplot(2,2,3)
        self.ax3 = plt.subplot(2,2,4)

        self.ax1.set_xlim([2,13])
        self.ax2.set_xlim([1,7])
        self.ax3.set_xlim([1,7])

        plt.ion()
        plt.show()

    def get_ans(self):
        answer = raw_input().lower()
        if answer == 'quit':
            print 'You quit!'
            self.save()
            exit()
        elif answer == 'save':
            self.save()

        try:
            answer = int(answer)
        except:
            print "%s was not a number" % answer
            return self.get_ans()
        if answer in [1,2,3,4,5,6]:
            return answer
        else:
            print "%d not between 1 and 6" % answer
            return self.get_ans()

    def save(self):
        print 'Saving to %s...' % self.savefile
        json.dump({'d1': self.d1_list, 'd2': self.d2_list}, open(self.savefile, 'w'))
        print 'Saved.'

    def update_plot(self):
        bins = np.arange(2, 14, 1)
        sub_plot_bins = np.arange(1, 8, 1)
        self.ax1.cla()
        self.ax2.cla()
        self.ax3.cla()
        self.ax1.set_xlim([1.5,12.5])
        self.ax2.set_xlim([0.5,6.5])
        self.ax3.set_xlim([0.5,6.5])

        self.ax1.hist(np.array(self.d1_list) + np.array(self.d2_list), bins=bins, range=[1,13], facecolor='g', align='left')
        self.ax1.set_xticks(bins[:-1])

        self.ax2.hist(np.array(self.d1_list), bins=sub_plot_bins, range=[1,7], facecolor='g', align='left')
        self.ax2.set_xticks(sub_plot_bins[:-1])

        self.ax3.hist(np.array(self.d2_list), bins=sub_plot_bins, range=[1,7], facecolor='g', align='left')
        self.ax3.set_xticks(sub_plot_bins[:-1])

        plt.draw()

    def start(self):
        self.d1_list = []
        self.d2_list = []
        print "Die 1:"
        d1 = counter.get_ans()
        print "Die 2:"
        d2 = counter.get_ans()
        while(1):
            self.d1_list.append(d1)
            self.d2_list.append(d2)
            print "Last roll:", self.d1_list[-1], self.d2_list[-1]

            counter.update_plot()

            print "Die 1:"
            d1 = counter.get_ans()
            print "Die 2:"
            d2 = counter.get_ans()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Counts dice rolls.')
    parser.add_argument('savefile', metavar='FILE', type=str, nargs='?', default=datetime.datetime.now().strftime('%Y%m%d_%H%M_rolls.json'),
                       help='File to save results to when quitting. Default: YYYYMMDD_HHMM_rolls.json')

    args = parser.parse_args()
    counter = DieCounter(args.savefile)
    counter.start()
