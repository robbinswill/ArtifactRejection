"""
This script acts as an interface between nagl_data\rawdata and sourcedata files,
and the subject_batch script. It gets the subject names, their list params, and the raw file path
to the .set EEG recordings
"""

from src.config.config import get_subject_lists_csv, get_data_path
import pandas as pd


def _load_subject_info():
    subject_lists_path = get_subject_lists_csv()
    subject_df = pd.read_csv(subject_lists_path)
    return subject_df.set_index('subject').T.to_dict()


def _load_subject_EEG_paths(subject_info):
    EEG_paths = {}
    for subject_id in subject_info.keys():
        EEG_paths[subject_id] = PathGenerator(subject_info[subject_id], subject_id)

    return EEG_paths


class DataInterface:

    def __init__(self):
        self.subject_info = _load_subject_info()
        self.EEG_paths = _load_subject_EEG_paths(self.subject_info)


class PathGenerator:
    def __init__(self, subject_lists, subject_id):
        self.list1 = subject_lists['list1']
        self.list2 = subject_lists['list2']
        self.subject_id = subject_id
        self.eeg1 = get_data_path().joinpath('rawdata', 'sub-' + self.subject_id, 'ses-list1', 'eeg',
                                             'sub-' + self.subject_id + '_ses-list1_eeg.set')
        self.eeg2 = get_data_path().joinpath('rawdata', 'sub-' + self.subject_id, 'ses-list2', 'eeg',
                                             'sub-' + self.subject_id + '_ses-list2_eeg.set')
        self.log1 = get_data_path().joinpath('sourcedata', 'sub-' + self.subject_id, 'ses-list1',
                                             self.subject_id + '_' + self.list1.lower() + '.csv')
        self.log2 = get_data_path().joinpath('sourcedata', 'sub-' + self.subject_id, 'ses-list2',
                                             self.subject_id + '_' + self.list2.lower() + '.csv')
        self.answers = get_data_path().joinpath('sourcedata', 'sub-' + self.subject_id,
                                                self.subject_id + '_SPIN_answers.xlsx')
        self.events_fname = get_data_path().joinpath('derivatives', 'sub-' + self.subject_id,
                                                     self.subject_id + '-eve.fif')
        self.epochs_fname = get_data_path().joinpath('derivatives', 'sub-' + self.subject_id,
                                                     self.subject_id + '-epo.fif')
        self.evoked_fname = get_data_path().joinpath('derivatives', 'sub-' + self.subject_id,
                                                     self.subject_id + '-ave.fif')
        self.covariance_fname = get_data_path().joinpath('derivatives', 'sub-' + self.subject_id,
                                                         self.subject_id + '-cov.fif')
        self.trans_fname = get_data_path().joinpath('derivatives', 'sub-' + self.subject_id,
                                                    self.subject_id + '-trans.fif')
        self.forward_fname = get_data_path().joinpath('derivatives', 'sub-' + self.subject_id,
                                                      self.subject_id + '-fwd.fif')
        self.inverse_fname = get_data_path().joinpath('derivatives', 'sub-' + self.subject_id,
                                                      self.subject_id + '-inv.fif')
        self.processed_path = get_data_path().joinpath('derivatives', 'sub-' + self.subject_id,
                                                       'preprocessed')
