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


def get_channel_mapping():
    return {'Fp1': 'Fp1', 'Fpz': 'Fp2', 'Fp2': 'F7', 'F7': 'F3', 'F3': 'Fz', 'Fz': 'F4', 'F4': 'F8',
            'F8': 'FC5', 'FC5': 'FC1', 'FC1': 'FC2', 'FC2': 'FC6', 'FC6': 'T7', 'M1': 'C3', 'T7': 'Cz',
            'C3': 'C4', 'Cz': 'T8', 'C4': 'TP9', 'T8': 'CP5', 'M2': 'CP1', 'CP5': 'CP2', 'CP1': 'CP6',
            'CP2': 'TP10', 'CP6': 'P7', 'P7': 'P3', 'P3': 'Pz', 'Pz': 'P4', 'P4': 'P8', 'P8': 'PO9',
            'POz': 'O1', 'O1': 'Oz', 'Oz': 'O2', 'O2': 'PO10', 'AF7': 'AF7', 'AF3': 'AF3', 'AF4': 'AF4',
            'AF8': 'AF8', 'F5': 'F5', 'F1': 'F1', 'F2': 'F2', 'F6': 'F6', 'FC3': 'FT9', 'FCz': 'FT7',
            'FC4': 'FC3', 'C5': 'FC4', 'C1': 'FT8', 'C2': 'FT10', 'C6': 'C5', 'CP3': 'C1', 'CPz': 'C2',
            'CP4': 'C6', 'P5': 'TP7', 'P1': 'CP3', 'P2': 'CPz', 'P6': 'CP4', 'PO5': 'TP8', 'PO3': 'P5',
            'PO4': 'P1', 'PO6': 'P2', 'FT7': 'P6', 'FT8': 'PO7', 'TP7': 'PO3', 'TP8': 'POz', 'PO7': 'PO4',
            'PO8': 'PO8', 'HEOG': 'HEOG', 'VEOG': 'VEOG',
            }


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
