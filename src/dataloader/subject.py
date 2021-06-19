import sys
sys.path.append('../src')

from src.config import config


class Subject:
    """
    Subject class for reading EEG data and performing pre-processing
    """

    def __init__(self, name):
        self.subject_name = name

    def read_data(self):
        pass
