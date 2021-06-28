import sys
sys.path.append('../src')
from src.dataloader import subjectdata
from src.models import subject


class SubjectBatch:

    def __init__(self):
        self.batch = {}
        self.data = None

    def get_data(self):
        return self.data

    def get_batch(self):
        return self.batch

    def load_subject_data(self):
        self.data = subjectdata.SubjectData()

    def generate_subjects(self):
        # Get list of subjects
        subject_names = self.data.get_subject_names()
        # Get subject lists
        subject_lists = self.data.get_subject_lists()
        # Get subject paths
        subject_paths = self.data.get_subject_paths()
        # Generate subject objects and store in a dict
        for s in subject_names:
            list1 = subject_lists[s][0]
            list2 = subject_lists[s][1]
            path1 = subject_paths[s][0]
            path2 = subject_paths[s][1]
            events_fname = subject_paths[s][2]
            self.batch[s] = subject.Subject(s, path1, path2, list1, list2)

    def subject_read_EEG(self):
        for name, sub in self.batch.items():
            sub.read_MNE_raw()

    def subject_bandpass_raw(self):
        for name, sub in self.batch.items():
            sub.bandpass_raw()

    def subject_event_processing(self):
        for name, sub in self.batch.items():
            sub.process_events()
