"""
define every single thing that can be configurable and can be changed in the future. Good examples are training
hyperparameters, folder paths, the model architecture, metrics, flags.
"""

from dotenv import find_dotenv, load_dotenv
from yacs.config import CfgNode as ConfigurationNode
from pathlib import Path
import os
import pandas as pd


# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables*
load_dotenv(dotenv_path)

# Retrieve path to raw EEG data
PATH_DATA_RAW = Path(os.getenv("PATH_DATA_RAW"))



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
__C.EXPERIMENT.EVENT_ID = ConfigurationNode()
__C.EXPERIMENT.EVENT_ID.QUIETCONTROLCORRECT = 1
__C.EXPERIMENT.EVENT_ID.QUIETVIOLATIONCORRECT = 2
__C.EXPERIMENT.EVENT_ID.NOISECONTROLCORRECT = 3
__C.EXPERIMENT.EVENT_ID.NOISEVIOLATIONCORRECT = 4
__C.EXPERIMENT.EVENT_ID.VISUALCUE = 5
__C.EXPERIMENT.EVENT_ID.QUIETCONTROLERROR = 11
__C.EXPERIMENT.EVENT_ID.QUIETVIOLATIONERROR = 22
__C.EXPERIMENT.EVENT_ID.NOISECONTROLERROR = 33
__C.EXPERIMENT.EVENT_ID.NOISEVIOLATIONERROR = 44
__C.EXPERIMENT.EVENT_ID.QUIETCONTROLPRACTICE = 100
__C.EXPERIMENT.EVENT_ID.QUIETVIOLATIONPRACTICE = 200
__C.EXPERIMENT.EVENT_ID.NOISECONTROLPRACTICE = 300
__C.EXPERIMENT.EVENT_ID.NOISEVIOLATIONPRACTICE = 400
__C.EXPERIMENT.COND_OF_INTEREST = ['Noise/Control/Correct', 'Noise/Control/Error', 'Noise/Control/Practice',
                                   'Noise/Violation/Correct', 'Noise/Violation/Error', 'Noise/Violation/Practice',
                                   'Quiet/Control/Correct', 'Quiet/Control/Error', 'Quiet/Control/Practice',
                                   'Quiet/Violation/Correct', 'Quiet/Violation/Error', 'Quiet/Violation/Practice',
                                   'VisualCue']
__C.EXPERIMENT.CODES_A1L2 = [2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1,
                             2, 1, 2, 2, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 1, 2,
                             2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2]
__C.EXPERIMENT.CODES_A2L2 = [4, 3, 4, 3, 3, 4, 4, 4, 3, 3, 3, 4, 4, 4, 3, 4, 3, 4, 3, 3, 4, 3, 3, 4, 4, 3, 3, 3, 4, 3,
                             4, 3, 4, 4, 3, 3, 4, 4, 4, 3, 4, 3, 3, 3, 4, 4, 3, 3, 4, 3, 4, 4, 4, 4, 3, 3, 4, 3, 3, 4,
                             4, 4, 3, 4, 4, 3, 4, 3, 3, 4, 3, 4, 3, 4, 3, 3, 3, 4, 3, 4, 4, 4, 3, 3, 4, 3, 3, 4]
__C.EXPERIMENT.EXPT_CONTRASTS = ['Quiet_Viol-Ctrl - Quiet/Violation/Correct', 'Quiet_Viol-Ctrl - Quiet/Control/Correct',
                                 'Noise_Viol-Ctrl - Noise/Violation/Correct', 'Noise_Viol-Ctrl - Noise/Control/Correct']


def get_raw_path():
    """
    :return: The raw directory path as a resolved path
    """
    return PATH_DATA_RAW


def get_cfg_defaults():
    """
    Get a YACS CfgNode object with default values
    """
    return __C.clone()
