# pylint: disable=too-many-instance-attributes

"""
    ECG window class is defined here
"""

import numpy as np

from .global_config import GlobalConfig as CONFIG


class Window:
    """
        Class for special interval of a processed signal
    """
    def __init__(self, name, r_peak_indexes):
        """
            Initialize object with interval (interval_size can differ)
        """
        self.name = name

        self.r_peaks = r_peak_indexes

        self.ratios = self.get_ratios()
        self.alphabet = self.code_ratios()

        self.median = np.median(self.ratios)
        self.mean = np.mean(self.ratios)
        self.variance = np.var(self.ratios)

    def get_ratios(self):
        """
            Output:
                get list of ratios
                ratio_i = 1 - y_i / y_{i-1}
                where y_i = len of i time interval
        """
        ratios = []
        prev_len = self.r_peaks[1] - self.r_peaks[0]
        for i in range(1, len(self.r_peaks) - 1):
            cur_len = self.r_peaks[i + 1] - self.r_peaks[i]
            if prev_len != 0:
                ratios.append(1 - cur_len / prev_len)
            prev_len = cur_len
        return np.array(ratios)


    def code_ratios(self):
        """
            Make from ratios list of coded letters:
            A - if abs(ratio) <  treshold
            B - if ratio > treshold
            C - if ratio < -1 * treshold
        """
        treshold = CONFIG.config('treshold')
        alphabet = []
        for ratio in self.ratios:
            if ratio > treshold:
                alphabet.append('B')
                continue
            if ratio < -treshold:
                alphabet.append('C')
                continue
            alphabet.append('A')

        return np.array(alphabet)

def create_window(name, r_peak_indexes):
    """
        create Window object
    """
    return Window(name, r_peak_indexes)
