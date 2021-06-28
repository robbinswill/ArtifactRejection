import sys
sys.path.append('../src')
from src.dataloader import subjectdata
from src.models import subject


class SubjectBatch:

    def __init__(self):
        self.subject_data = None
        self.batch = None

    def load_subject_data(self):
        self.subject_data = subjectdata.SubjectData()

    def generate_subjects(self):
        self.batch = {}
        for sub, paths in self.subject_data.EEG_paths.items():
            self.batch[sub] = subject.Subject(sub, paths)

    def subject_read_EEG(self):
        for name, sub in self.batch.items():
            sub.read_MNE_raw()

    def subject_bandpass_raw(self):
        for name, sub in self.batch.items():
            sub.bandpass_raw()

    def subject_event_processing(self):
        for name, sub in self.batch.items():
            sub.process_events()

    def subject_behavioural_log(self):
        for name, sub in self.batch.items():
            sub.read_behavioural_log()
