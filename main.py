"""
Main driver script
"""
from src.models import batch


def run():
    print('Executing main.py...')
    test = batch.SubjectBatch()
    test.generate_subjects()
    test.test()
    # test.execute_serial()
    # test.execute_preprocessing()
    print('main.py finished')


if __name__ == '__main__':
    run()
