import os
import sys
sys.path.append('../src')
from src.config.config import get_raw_path, get_interim_path


def _get_raw_path(subject_name):
    return get_raw_path().joinpath(subject_name, 'EEG', 'SPIN')


def _get_interim_path(subject_name):
    return get_interim_path().joinpath(subject_name, 'EEG', 'SPIN')


def _load_subjects():
    raw_path = get_raw_path()
    return os.listdir(raw_path)


def _load_lists(subjects):
    subject_lists = {}
    raw_path = get_raw_path()
    for s in subjects:
        sub_path = _get_raw_path(s)
        sub_lists = os.listdir(sub_path)
        subject_lists[s] = (sub_lists[0], sub_lists[1])
    return subject_lists


def _load_EEG_paths(subjects):
    subject_paths = {}
    for s, l in subjects.items():
        lower_list1 = l[0].lower()
        lower_list2 = l[1].lower()
        subject_paths[s] = (_get_raw_path(s).joinpath(subjects[s][0], s + '_' + 'SPIN' + '_' + lower_list1 + '.set'),
                            _get_raw_path(s).joinpath(subjects[s][1], s + '_' + 'SPIN' + '_' + lower_list2 + '.set'),
                            _get_interim_path(s).joinpath(s + '-eve.fif'))
    return subject_paths


class SubjectData:

    def __init__(self):
        self.subjects = _load_subjects()
        self.lists = _load_lists(self.subjects)
        self.EEG_paths = _load_EEG_paths(self.lists)


    def get_subject_names(self):
        """
        :return: a list of subject names
        """
        return self.subjects


    def get_subject_lists(self):
        """
        :return: a dict of subject lists in the form {subject_name: (list1, list2)}
        """
        return self.lists


    def get_subject_paths(self):
        """
        :return: a dict of subject .set paths in the form {subject_name: (path1, path2)}
        """
        return self.EEG_paths
