import sys
sys.path.append('../src')
import mne


class Subject:
    """
    Subject class for reading EEG data and performing pre-processing
    """
    def __init__(self, name, path1, path2, list1, list2):
        self.name = name
        self.list1 = list1
        self.list2 = list2
        self.path1 = path1
        self.path2 = path2


    def read_MNE_raw(self):
        pass
