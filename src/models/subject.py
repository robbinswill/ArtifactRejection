import sys

sys.path.append('../src')
from src.config.config import get_cfg_defaults, get_channel_mapping
import mne
import numpy as np


class Subject:
    """
    Subject class for reading EEG data and performing pre-processing
    """

    def __init__(self, name, path1, path2, events_fname, list1, list2):
        self.MNE_Raw = None
        self.MNE_Raw_filt = None
        self.raw_files = []
        self.events = None
        self.event_dict = None
        self.name = name
        self.list1 = list1
        self.list2 = list2
        self.paths = [path1, path2]
        self.events_fname = events_fname

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
        self.events, self.event_dict = mne.events_from_annotations(self.MNE_Raw)

        # Perform extra step to correct for wrong codes
        cfg = get_cfg_defaults()
        if self.list1 == 'a1l2':
            codes2replace_idx = np.where(self.events[:, 2] < 3)
            self.events[codes2replace_idx, 2] = cfg['EXPERIMENT']['CODES_A1L2']
        if self.list2 == 'a2l2':
            codes2replace_idx = np.where((self.events[:, 2] > 2) and (self.events[:, 2] < 5))
            self.events[codes2replace_idx, 2] = cfg['EXPERIMENT']['CODES_A2L2']

        mne.write_events(self.events_fname, self.events)
