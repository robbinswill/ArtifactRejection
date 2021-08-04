"""
Main driver script
"""
from src.models import batch
from src.utils import generate_data


def run():
    print('Executing main.py...')
    # print('Generating BIDS...')
    # generate_data.generate_BIDS()
    print('Running preprocessing pipeline...')
    subjects = batch.SubjectBatch()
    subjects.generate_subjects()
    # subjects.test()
    # test.execute_serial()
    subjects.execute_parallel()
    print('main.py finished')


if __name__ == '__main__':
    run()
