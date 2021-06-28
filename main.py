from src.models import batch


def run():
    test_batch = batch.generate_subjects()
    test_read = batch.subject_read_EEG(test_batch)
    print('test')


if __name__ == '__main__':
    run()
