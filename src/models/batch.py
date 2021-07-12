import sys
sys.path.append('../src')
from src.dataloader import data_interface
from src.models import subject


class SubjectBatch:

    def __init__(self):
        self.subject_data = None
        self.subject_batch = None

    def _load_subject_data(self):
        self.subject_data = data_interface.DataInterface()

    def generate_subjects(self):
        self._load_subject_data()
        self.subject_batch = {}
        for sub, paths in self.subject_data.EEG_paths.items():
            self.subject_batch[sub] = subject.Subject(sub, paths)
        del self.subject_data

    def execute_preprocessing(self):
        for name, sub in self.subject_batch.items():
            sub.read_MNE_raw()
            sub.bandpass_raw()
            sub.process_events()
            sub.read_behavioural_log()
            sub.process_epochs()
            sub.process_ICA()
