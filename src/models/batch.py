"""
Batch script that generates subjects and executes preprocessing
"""
from src.dataloader.data_interface import DataInterface
from src.models.subject import Subject
from src.utils.subject_report import SubjectReport
import concurrent.futures
import multiprocessing


class SubjectBatch:

    def __init__(self):
        self.subject_data = None
        self.subject_batch = None
        self.report = SubjectReport()

    def _load_subject_data(self):
        self.subject_data = DataInterface()

    def generate_subjects(self):
        self._load_subject_data()
        self.subject_batch = {}
        for sub, paths in self.subject_data.EEG_paths.items():
            self.subject_batch[sub] = Subject(sub, paths)
        del self.subject_data

    def test(self):
        sub = self.subject_batch['nagl001']
        print('Processing subject: ' + sub.name)
        print('Reading raw files...')
        sub.read_MNE_raw()
        print('Processing events...')
        sub.process_events()
        print('Reading behavioural log...')
        sub.read_behavioural_log()
        print('Preprocessing...')
        sub.preprocessing()
        print('Creating evoked responses...')
        sub.evoked()

        # After preprocessing has finished for this subject, give their figures to SubjectReport
        self.report.add_subject_figures(sub.name, sub.figures)
        print('Preprocessing complete for: ' + sub.name)
        # Generate report
        print("Generating preprocessing report...")
        self.report.generate_report()

    def execute_serial(self):
        for name, sub in self.subject_batch.items():
            self._preprocess_subject(sub)

        # Generate report
        print("Generating preprocessing report...")
        self.report.generate_report()

    def execute_parallel(self):
        # Multiprocessing test
        with multiprocessing.Pool() as executor:
            executor.map_async(self._preprocess_subject, self.subject_batch.values(), chunksize=1)
            executor.close()
            executor.join()
            # After preprocessing all subjects generate the report
            self.report.generate_report()


    def _preprocess_subject(self, sub):
        print('Processing subject: ' + sub.name)
        print('Reading raw files...')
        sub.read_MNE_raw()
        print('Processing events...')
        sub.process_events()
        print('Reading behavioural log...')
        sub.read_behavioural_log()
        print('Preprocessing...')
        sub.preprocessing()
        print('Creating evoked responses...')
        sub.evoked()

        # After preprocessing has finished for this subject, give their figures to SubjectReport
        self.report.add_subject_figures(sub.name, sub.figures)
        print('Preprocessing complete for: ' + sub.name)
