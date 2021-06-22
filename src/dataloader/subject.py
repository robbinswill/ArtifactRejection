import sys
import mne
from pathlib import Path
sys.path.append('../src')

from src.config import config


class Subject:
    """
    Subject class for reading EEG data and performing pre-processing
    """

    def __init__(self, name):
        self.subject_name = name

    def read_data(self):
        """
        Reads in raw .set (and .fdi) files to generate a Raw mne object
        :return:
        """
        raw_path = config.PATH_DATA_RAW
