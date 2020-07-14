class Session:
    """ETL workflow session

    Example:
        with Session(task_name) as session:
            print(session.id)
            session.loaded_rows = 15
            session.last_key = 884182
            session.success = true
            session.comment = 'Well done'

    """
    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
