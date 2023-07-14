class FileHandler:
    @staticmethod
    def get_employers_from_file(path):
        """
        Read employer names from a file.

        Args:
            path (str): Path to the file.

        Returns:
            list: List of employer names.
        """
        try:
            with open(path, 'r') as f:
                data = f.read()
            return [
                data.strip()
                if data.count(',') > 0
                else data
                for data in data.split(',')
            ]
        except FileNotFoundError as e:
            print(e)
