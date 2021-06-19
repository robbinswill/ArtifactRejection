import os
import pandas as pd

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
    return list(df.Subjects)
