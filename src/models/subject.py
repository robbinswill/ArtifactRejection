import sys

sys.path.append('../src')
from src.config.config import get_cfg_defaults, get_channel_mapping
import mne


class Subject:
    """
    Subject class for reading EEG data and performing pre-processing
    """

    def __init__(self, name, path1, path2, list1, list2):
        self.MNE_Raw = None
        self.raw_files = []
        self.name = name
        self.list1 = list1
        self.list2 = list2
        self.paths = [path1, path2]

    def read_MNE_raw(self):
        cfg = get_cfg_defaults()
        eog_inds = cfg['PARAMS']['EOG_INDS']
        self.raw_files = [mne.io.read_raw_eeglab(f, eog=eog_inds, preload=False)
                          for f in self.paths]
        self.MNE_Raw = mne.concatenate_raws(self.raw_files, preload=True)

        # Check for incorrect channels
        if self.MNE_Raw.ch_names[1] == 'Fpz':
            channel_mapping = get_channel_mapping()
            mne.rename_channels(self.MNE_Raw.info, channel_mapping)
        self.MNE_Raw.set_montage(cfg['PARAMS']['MONTAGE_FNAME'])
