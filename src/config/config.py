import os
import pandas as pd
import mne

from dotenv import find_dotenv, load_dotenv
from yacs.config import CfgNode as ConfigurationNode
from pathlib import Path

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables*
load_dotenv(dotenv_path)

# Retrieve path to raw EEG data
PATH_DATA_RAW = Path(os.getenv("PATH_DATA_RAW"))
# PATH_DATA_NAMES = Path(os.getenv("PATH_DATA_NAMES"))

# Declare hyperparameters
# More specific parameters for other experiments can be declared in separate YAML files
__C = ConfigurationNode()
cfg = __C

__C.DESCRIPTION = 'Default config for subject preprocessing'

__C.PARAMS = ConfigurationNode()
__C.PARAMS.TMIN = -0.2
__C.PARAMS.TMAX = 1.0
__C.PARAMS.EOG_INDS = [64, 65]
__C.PARAMS.L_FREQ = 0.1
__C.PARAMS.H_FREQ = 30.0
__C.PARAMS.L_TRANS_BANDWIDTH = 'auto'
__C.PARAMS.H_TRANS_BANDWIDTH = 'auto'
__C.PARAMS.FILTER_LENGTH = 'auto'
__C.PARAMS.ICA_RANDOM_STATE = 42
__C.PARAMS.N_COMPONENTS = 0.975
__C.PARAMS.BASELINE = (None, 0)
__C.PARAMS.MONTAGE_FNAME = 'standard_1005'

__C.EXPERIMENT = ConfigurationNode()
__C.EXPERIMENT.EVENT_ID = {'Quiet/Control/Correct': 1, 'Quiet/Violation/Correct': 2,
                           'Noise/Control/Correct': 3, 'Noise/Violation/Correct': 4,
                           'VisualCue': 5,

                           'Quiet/Control/Error': 11, 'Quiet/Violation/Error': 22,
                           'Noise/Control/Error': 33, 'Noise/Violation/Error': 44,

                           'Quiet/Control/Practice': 100, 'Quiet/Violation/Practice': 200,
                           'Noise/Control/Practice': 300, 'Noise/Violation/Practice': 400,
                           }
__C.EXPERIMENT.COND_OF_INTEREST = sorted(__C.EXPERIMENT.EVENT_ID.values())
__C.EXPERIMENT.CODES_A1L2 = [2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1,
                             2, 1, 2, 2, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 1, 2,
                             2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2]
__C.EXPERIMENT.CODES_A2L2 = [4, 3, 4, 3, 3, 4, 4, 4, 3, 3, 3, 4, 4, 4, 3, 4, 3, 4, 3, 3, 4, 3, 3, 4, 4, 3, 3, 3, 4, 3,
                             4, 3, 4, 4, 3, 3, 4, 4, 4, 3, 4, 3, 3, 3, 4, 4, 3, 3, 4, 3, 4, 4, 4, 4, 3, 3, 4, 3, 3, 4,
                             4, 4, 3, 4, 4, 3, 4, 3, 3, 4, 3, 4, 3, 4, 3, 3, 3, 4, 3, 4, 4, 4, 3, 3, 4, 3, 3, 4]
__C.EXPERIMENT.EXPT_CONTRASTS = {'Quiet_Viol-Ctrl': ['Quiet/Violation/Correct', 'Quiet/Control/Correct'],
                                 'Noise_Viol-Ctrl': ['Noise/Violation/Correct', 'Noise/Control/Correct'],
                                 }


def get_cfg_defaults():
    """
    Get a YACS CfgNode object with default values
    """
    return __C.clone()


def get_subject_names():
    """
    Get the subject names from the CSV file in the data folder
    :return: a list of subjects from the subject-names.csv (column is "Subjects")
    """
    df = pd.read_csv(Path(os.getenv("PATH_DATA_NAMES")))
    return list(df.Subjects)  # Is it okay to use the column name here?
