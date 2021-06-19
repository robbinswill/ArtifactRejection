import sys

sys.path.append('../src')

from src.config import config
from src.dataloader import subject


def read_in():
    """
    Read-in the list of subjects from the CSV in the data folder
    :return: a list of subject names
    """
    return config.get_subject_names()


def generate_subjects():
    """
    Generate a Subject object for each read-in subject
    :return: a dict of Subjects in the form { Subject name: Subject object}
    """
    names = read_in()
    subjects = {}
    for n in names:
        subjects[n] = subject.Subject(n)

    return subjects
