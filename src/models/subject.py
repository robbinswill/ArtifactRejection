import sys

sys.path.append('../src')
from src.config.config import get_cfg_defaults, get_channel_mapping
import mne
import numpy as np


class Subject:
    """
    Subject class for reading EEG data and performing pre-processing
    """
    def __init__(self, name, paths):
        self.MNE_Raw = None
        self.MNE_Raw_filt = None
        self.raw_files = []
        self.events = None
        self.event_dict = None
        self.name = name
        self.list1 = paths.list1
        self.list2 = paths.list2
        self.raw_paths = [paths.path1, paths.path2]
        self.events_fname = paths.events_fname
        self.epochs_fname = paths.epochs_fname
        self.evoked_fname = paths.evoked_fname
        self.covariance_fname = paths.covariance_fname
        self.trans_fname = paths.trans_fname
        self.forward_fname = paths.forward_fname
        self.inverse_fname = paths.inverse_fname

    def read_MNE_raw(self):
        cfg = get_cfg_defaults()
        eog_inds = cfg['PARAMS']['EOG_INDS']
        self.raw_files = [mne.io.read_raw_eeglab(f, eog=eog_inds, preload=False)
                          for f in self.raw_paths]
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

    def read_behavioural_log(self):
        pass
