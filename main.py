from src.models import batch


def run():
    test = batch.SubjectBatch()
    test.generate_subjects()
    test.execute_preprocessing()
    print('test')


if __name__ == '__main__':
    run()
