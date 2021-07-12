import sys

sys.path.append('../src')
from src.config.config import get_cfg_defaults, get_channel_mapping, get_event_id
import mne
from autoreject import Ransac
from autoreject.utils import interpolate_bads
import numpy as np
import pandas as pd
from pathlib import Path


class Subject:
    """
    Subject class for reading EEG data and performing pre-processing
    """

    def __init__(self, name, paths):
        self.epochs_clean = None
        self.epochs = None
        self.picks_eeg = None
        self.event_id = None
        self.event_id_actual = None
        self.actual_codes = None
        self.err_indices = None
        self.events_target = None
        self.target_codes_idx = None
        self.acc_data = None
        self.MNE_Raw = None
        self.MNE_Raw_filt = None
        self.raw_files = None
        self.events = None
        self.event_dict = None
        self.name = name
        self.processed_path = paths.processed_path
        self.list_names = [paths.list1, paths.list2]
        self.raw_paths = [paths.eeg1, paths.eeg2]
        self.events_fname = paths.events_fname
        self.epochs_fname = paths.epochs_fname
        self.evoked_fname = paths.evoked_fname
        self.covariance_fname = paths.covariance_fname
        self.trans_fname = paths.trans_fname
        self.forward_fname = paths.forward_fname
        self.inverse_fname = paths.inverse_fname
        self.answers = paths.answers

    def _create_processed_dir(self):
        Path(self.processed_path).mkdir(parents=True, exist_ok=True)

    def read_MNE_raw(self):
        # First, create a directory for preprocessed data
        self._create_processed_dir()

        # Then begin reading in data for the Raw data structure
        cfg = get_cfg_defaults()
        eog_inds = cfg['PARAMS']['EOG_INDS']
        self.raw_files = [mne.io.read_raw_eeglab(f, eog=eog_inds, preload=False)
                          for f in self.raw_paths]
        self.MNE_Raw = mne.concatenate_raws(self.raw_files, preload=True)

        # Check for incorrect channels
        if self.MNE_Raw.ch_names[1] == 'Fpz':
            channel_mapping = get_channel_mapping()
            mne.rename_channels(self.MNE_Raw.info, channel_mapping)

        # Set the montage
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
        if self.list_names[0] == 'a1l2':
            codes2replace_idx = np.where(self.events[:, 2] < 3)
            self.events[codes2replace_idx, 2] = cfg['EXPERIMENT']['CODES_A1L2']
        if self.list_names[1] == 'a2l2':
            codes2replace_idx = np.where((self.events[:, 2] > 2) and (self.events[:, 2] < 5))
            self.events[codes2replace_idx, 2] = cfg['EXPERIMENT']['CODES_A2L2']

        mne.write_events(self.events_fname, self.events)

    def read_behavioural_log(self):
        self.acc_data = pd.DataFrame()
        for block in np.arange(0, np.size(self.list_names)):
            self.acc_data = self.acc_data.append(pd.read_excel(self.answers,
                                                               sheet_name=block, usecols=[0, 1], header=None))
        self.acc_data = self.acc_data[self.acc_data[0] != 'accuracy']
        self.acc_data = self.acc_data.dropna()
        self.acc_data = self.acc_data.rename(columns={0: 'word', 1: 'correct'})

        # Modify codes for error trials
        # Find codes for target words
        self.target_codes_idx = np.where(self.events[:, 2] < 5)
        self.events_target = self.events[self.target_codes_idx, 2]
        # Find indices of error trials
        self.err_indices = np.where(self.acc_data['correct'] == 0)[0]
        # Replaces codes for error trials with a code that doubles its numeral
        self.events_target[0][self.err_indices] = self.events_target[0][self.err_indices] * 10 + self.events_target[0][
            self.err_indices]
        # Exclude first 8 practice trials
        self.events_target[0][:8] = self.events_target[0][:8] * 100
        self.events_target[0][88:88 + 8] = self.events_target[0][88:88 + 8] * 100
        # Merge modified codes into events structure
        self.events[self.target_codes_idx, 2] = self.events_target
        # Remove absent codes from event_id dict
        self.event_id = get_event_id()
        self.actual_codes = [i for i in list(self.event_id.values()) if i in np.unique(self.events[:, 2])]
        self.event_id_actual = {}
        for k in self.event_id.keys():
            if self.event_id[k] in self.actual_codes:
                self.event_id_actual[k] = self.event_id[k]
        self.event_id = self.event_id_actual

    def process_epochs(self):
        cfg = get_cfg_defaults()
        # Unsure on picks_eeg
        self.picks_eeg = mne.pick_types(self.MNE_Raw_filt.info, eeg=True, eog=True, stim=False, exclude=[])
        self.epochs = mne.Epochs(raw=self.MNE_Raw_filt, events=self.events, event_id=self.event_id,
                                 tmin=cfg['PARAMS']['TMIN'], tmax=cfg['PARAMS']['TMAX'], proj=False,
                                 picks=self.picks_eeg,
                                 baseline=cfg['PARAMS']['BASELINE'], detrend=1, preload=True,
                                 reject=dict(eeg=500e-6,  # V (EEG channels)
                                             eog=500e-6  # V (EOG channels)
                                             )
                                 )
        self.picks_eeg = mne.pick_types(self.epochs.info, eeg=True, eog=False, stim=False, include=[], exclude=[])

        # Plot epochs and reject bad trials
        # Code used is from autoreject API example
        ransac = Ransac(verbose='progressbar', picks=self.picks_eeg, n_jobs=1)
        self.epochs_clean = ransac.fit_transform(self.epochs)
        # Get list of bad channels computes by Ransac
        print('\n'.join(ransac.bad_chs_))

    def process_ICA(self):
        pass
