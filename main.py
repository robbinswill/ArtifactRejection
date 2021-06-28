from src.models import batch


def run():
    test = batch.SubjectBatch()
    test.load_subject_data()
    test.generate_subjects()
    test.subject_read_EEG()
    test.subject_bandpass_raw()
    test.subject_event_processing()
    test.subject_behavioural_log()
    print('test')


if __name__ == '__main__':
    run()
