class FileHandler:

    @staticmethod
    def get_employers_from_file(path):
        try:
            with open(path, 'r') as f:
                data = f.read()
            return [int(data.strip()) for data in data.split(',')]
        except FileNotFoundError as e:
            print(e)



