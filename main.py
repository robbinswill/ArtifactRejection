from src.models import batch


def run():
    test = batch.SubjectBatch()
    test.load_subject_data()
    test.generate_subjects()
    test.subject_read_EEG()
    test.subject_bandpass_raw()
    print('test')


if __name__ == '__main__':
    run()
