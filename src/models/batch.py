import sys

sys.path.append('../src')

from src.config import config
from src.dataloader import subject

# Get the list of subjects
subjects = config.get_subject_names()
