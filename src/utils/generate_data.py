# Script to generate nagl_data in BIDS format from project source taken from the NCIL NAS
# A required input is the subject_lists.csv in NAGL_SOURCE
# This script is located in nagl_dataset\code\generate_data.py

import os
from pathlib import Path
import mne.io
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from src.config.config import get_cfg_defaults, get_data_path, get_subject_lists_csv
from mne_bids import write_raw_bids, BIDSPath
import shutil


# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()
# load up the entries as environment variables*
load_dotenv(dotenv_path)

# Get the source directory and desired rawdata directory
NAGL_SOURCE = Path(os.getenv("NAGL_SOURCE"))
bids_root = get_data_path().joinpath('rawdata')

# Each sessions refers to one of two lists that the subject was tested on
sessions = ['list1', 'list2']

# Read-in subjects and list parameters, creating a dictionary
subject_lists_path = get_subject_lists_csv()
subject_df = pd.read_csv(subject_lists_path)
subject_list_params = subject_df.set_index('subject').T.to_dict()

# Begin creating BIDS
bids_list = list()
cfg = get_cfg_defaults()

for subject_id in subject_list_params.keys():
    subject_name_dir = None

    for session_list in sessions:
        # Get the list
        subject_list = subject_list_params[subject_id][session_list]
        # Get the path for this subject
        raw_fname = NAGL_SOURCE.joinpath(subject_id, 'EEG', 'SPIN', subject_list,
                                         subject_id + '_SPIN_' + subject_list.lower() + '.set')
        raw = mne.io.read_raw_eeglab(raw_fname.__str__(), cfg['PARAMS']['EOG_INDS'], preload=False)
        raw.set_montage(cfg['PARAMS']['MONTAGE_FNAME'])
        raw.info['line_freq'] = cfg['PARAMS']['LINE_FREQ']
        bids_path = BIDSPath(subject=subject_id, session=session_list, root=bids_root)
        bids_list.append(bids_path)
        write_raw_bids(raw, bids_path, overwrite=True)

        # Get the sub-nagl###\ses-list# directory names to be used in the sourcedata directory
        subject_name_dir = bids_path.fpath.parent.parent.parent
        subject_list_dir = bids_path.fpath.parent.parent.stem
        logs_dir = get_data_path().joinpath('sourcedata', subject_name_dir.stem, subject_list_dir)
        logs_dst = logs_dir.joinpath(subject_id + '_' + subject_list.lower() + '.csv')

        # Get the path, including the name, of the file to be copied
        logs_src = NAGL_SOURCE.joinpath(subject_id, 'EEG', 'SPIN', subject_list,
                                        subject_id + '_' + subject_list.lower() + '.csv')

        # Copy the file to ..\sourcedata\sub-nagl###\ses-list#
        os.makedirs(os.path.dirname(logs_dst.__str__()), exist_ok=True)
        # Had to rename A2L2 log file for subject 9, A1L1 for subject 37
        shutil.copyfile(logs_src, logs_dst)

    # Copy nagl###_SPIN_answers.xlsx to sourcedata\sub-nagl###
    answers_src = NAGL_SOURCE.joinpath(subject_id, 'EEG', 'SPIN', subject_id + '_SPIN_answers.xlsx')
    answers_dst = get_data_path().joinpath('sourcedata', subject_name_dir.stem, subject_id + '_SPIN_answers.xlsx')
    shutil.copyfile(answers_src, answers_dst)
