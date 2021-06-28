import os
import sys
sys.path.append('../src')
from src.config.config import get_raw_path, get_lists_path, FileExtensions


def _load_subjects():
    raw_path = get_raw_path()
    return os.listdir(raw_path)


class SubjectData:

    def __init__(self):
        self.subjects = _load_subjects()
        self.lists = self._load_lists()
        self.EEG_paths = self._load_EEG_paths()

    def _load_lists(self):
        subject_lists = {}
        for s in self.subjects:
            sub_path = get_lists_path(s)
            sub_lists = os.listdir(sub_path)
            subject_lists[s] = (sub_lists[0], sub_lists[1])
        return subject_lists

    def _load_EEG_paths(self):
        subject_paths = {}
        for sub, lists in self.lists.items():
            subject_paths[sub] = FileExtensions(sub, lists[0], lists[1])
        return subject_paths
