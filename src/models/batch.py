import sys
sys.path.append('../src')
from src.dataloader import subjectdata
from src.models import subject


def _load_subject_data():
    return subjectdata.SubjectData()


def generate_subjects():
    """
    :return: a dict of generated subjects
    """
    # Get subject class
    subject_loader = _load_subject_data()
    # Get list of subjects
    subject_names = subject_loader.get_subject_names()
    # Get subject lists
    subject_lists = subject_loader.get_subject_lists()
    # Get subject paths
    subject_paths = subject_loader.get_subject_paths()
    # Generate subject objects and store in a dict
    subject_dict = {}
    for s in subject_names:
        list1 = subject_lists[s][0]
        list2 = subject_lists[s][1]
        path1 = subject_paths[s][0]
        path2 = subject_paths[s][1]
        subject_dict[s] = subject.Subject(s, path1, path2, list1, list2)
    return subject_dict


def subject_read_EEG(subject_dict):
    for name, sub in subject_dict.items():
        sub.read_MNE_raw()
