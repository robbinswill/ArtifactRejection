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
        self.MNE_Raw_filt = None
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

    def bandpass_raw(self):
        cfg = get_cfg_defaults()
        cfg_params = cfg['PARAMS']
        l_freq = cfg_params['L_FREQ']
        h_freq = cfg_params['H_FREQ']
        l_trans_bandwidth = cfg_params['L_TRANS_BANDWIDTH']
        h_trans_bandwidth = cfg_params['H_TRANS_BANDWIDTH']
        filter_length = cfg_params['FILTER_LENGTH']
        method = cfg_params['METHOD']
        n_jobs = cfg_params['N_JOBS']
        self.MNE_Raw_filt = self.MNE_Raw.copy().filter(l_freq, h_freq,
                                                       l_trans_bandwidth=l_trans_bandwidth,
                                                       h_trans_bandwidth=h_trans_bandwidth,
                                                       filter_length=filter_length,
                                                       method=method,
                                                       picks=mne.pick_types(self.MNE_Raw.info, eeg=True, eog=True),
                                                       n_jobs=n_jobs)

    def process_events(self):
        pass
