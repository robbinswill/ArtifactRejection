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
    test = batch.SubjectBatch()
    test.generate_subjects()
    test.test()
    # test.execute_serial()
    test.execute_preprocessing()
    print('main.py finished')


if __name__ == '__main__':
    run()
