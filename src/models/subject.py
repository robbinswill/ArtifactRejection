import sys

sys.path.append('../src')
from src.config.config import get_cfg_defaults, get_channel_mapping, get_event_id
import mne
from autoreject import Ransac, get_rejection_threshold, AutoReject
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
        self.plot_path = paths.plot_path
        self.report = mne.Report(verbose=True)
        self.report_fname = paths.report_fname

        # First, create a directory for preprocessed data
        Path(self.processed_path).mkdir(parents=True, exist_ok=True)
        # Create a path for plots
        Path(self.plot_path).mkdir(parents=True, exist_ok=True)


    def read_MNE_raw(self):

        # Begin reading in data for the Raw data structure
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

    def preprocessing(self):
        # Retrieve parameters from configuration file
        cfg_params = get_cfg_defaults()['PARAMS']
        l_freq_ica = cfg_params['L_FREQ_ICA']
        h_freq = cfg_params['H_FREQ']
        l_freq = cfg_params['L_FREQ']
        l_trans_bandwidth = cfg_params['L_TRANS_BANDWIDTH']
        h_trans_bandwidth = cfg_params['H_TRANS_BANDWIDTH']
        filter_length = cfg_params['FILTER_LENGTH']
        filter_method = cfg_params['FILTER_METHOD']
        n_jobs = cfg_params['N_JOBS']
        filter_picks = cfg_params['FILTER_PICKS']
        t_step = cfg_params['T_STEP']
        random_state = cfg_params['ICA_RANDOM_STATE']
        n_components = cfg_params['N_COMPONENTS']
        num_excl = cfg_params['NUM_EXCL']
        z_thresh = cfg_params['Z_THRESHOLD']
        z_step = cfg_params['Z_STEP']
        t_min = cfg_params['TMIN']
        t_max = cfg_params['TMAX']
        detrend = cfg_params['DETREND']
        baseline = cfg_params['BASELINE'][0]
        ref_channels = cfg_params['REF_CHANNELS']

        # Generate two copies of the raw object:
        # Filter data w/ 1.0Hz lowpass cutoff for ICA
        raw_ica = self.MNE_Raw.copy().filter(l_freq=l_freq_ica, h_freq=h_freq,
                                             l_trans_bandwidth=l_trans_bandwidth,
                                             h_trans_bandwidth=h_trans_bandwidth,
                                             filter_length=filter_length,
                                             method=filter_method,
                                             picks=mne.pick_types(self.MNE_Raw.info, eeg=True, eog=True),
                                             n_jobs=n_jobs)

        # Bandpass filter second copy of MNE_raw
        raw_filt = self.MNE_Raw.copy().filter(l_freq=l_freq, h_freq=h_freq,
                                              l_trans_bandwidth=l_trans_bandwidth,
                                              h_trans_bandwidth=h_trans_bandwidth,
                                              filter_length=filter_length,
                                              method=filter_method,
                                              picks=filter_picks,
                                              n_jobs=n_jobs)
        raw_filt_plot = raw_filt.plot_psd(fmax=65, n_jobs=n_jobs, average=False, spatial_colors=True, show=False)
        self.report.add_figs_to_section(raw_filt_plot, captions='Raw data: Filtered', section='Preprocessing')
        self.report.save(self.report_fname, overwrite=True, open_browser=False)

        # Convert raw_ica to a series of 1s epochs
        events_ica = mne.make_fixed_length_events(raw_ica, duration=t_step)
        epochs_ica = mne.Epochs(raw_ica, events_ica, tmin=0.0, tmax=t_step, baseline=None, preload=True)
        del events_ica

        # Mark bad channels and exclude them from ICA fitting, using RANSAC algorithm
        ransac = Ransac(n_jobs=n_jobs, random_state=random_state)
        ransac.fit(epochs_ica)
        epochs_ica.info['bads'] = ransac.bad_chs_

        # Auto-determine rejection threshold (dict) to eliminate noisy trials from ICA fitting
        reject = get_rejection_threshold(epochs_ica)

        # Fit ICA to the raw data
        ica = mne.preprocessing.ICA(n_components=n_components,
                                    random_state=random_state)
        ica.fit(epochs_ica, reject=reject, tstep=t_step)

        # Identify independent components associated with EOG artifacts
        ica.exclude = []
        eog_indices = None

        while num_excl < 2:
            eog_indices, eog_scores = ica.find_bads_eog(raw_ica, threshold=z_thresh)
            num_excl = len(eog_indices)
            z_thresh -= z_step

        # Finally, ICA should have dropped ocular artifacts
        ica.exclude = eog_indices

        # Segment filtered raw data into epochs
        epochs = mne.Epochs(raw_filt, self.events, self.event_id, t_min, t_max,
                            baseline=baseline, detrend=detrend, reject=None, flat=None, preload=True)

        # Apply ICA correction
        epochs_postica = ica.apply(epochs.copy())
        epochs_postica.info['bads'] = ransac.bad_chs_
        epochs_postica = epochs_postica.interpolate_bads()

        # Apply AutoReject to epochs to clean up noise
        ar = AutoReject(n_jobs=n_jobs, random_state=random_state, verbose=False)
        epochs_clean = ar.fit_transform(epochs_postica)
        epochs_clean.set_eeg_reference(ref_channels=ref_channels)

        # Save cleaned epochs
        epochs_clean.save(self.epochs_fname, overwrite=True)
