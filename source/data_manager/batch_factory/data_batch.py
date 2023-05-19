class DataBatch:
    def __init__(self):
        pass

    def create_batch(self):
        pass

    def delete_batch(self):
        pass

    def save(self):
        pass

    def upload(self):
        pass

    def observe_file(self, file_path):
        if Path.is_file(file_path):
            analyze_max_size_of_batch(file_path)
        else:
            raise FileExistsError