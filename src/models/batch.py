import sys
sys.path.append('../src')
from src.dataloader import subjectdata
from src.models import subject


class SubjectBatch:

    def __init__(self):
        self.subject_data = None
        self.batch = None

    def _load_subject_data(self):
        self.subject_data = subjectdata.SubjectData()

    def generate_subjects(self):
        self._load_subject_data()
        self.batch = {}
        for sub, paths in self.subject_data.EEG_paths.items():
            self.batch[sub] = subject.Subject(sub, paths)

    def execute_preprocessing(self):
        for name, sub in self.batch.items():
            sub.read_MNE_raw()
            sub.bandpass_raw()
            sub.process_events()
            sub.read_behavioural_log()
            sub.process_epochs()
