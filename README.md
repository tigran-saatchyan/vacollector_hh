# Vacancy Parser
***
[![Python Version](https://img.shields.io/badge/Python-3.10.6-blue.svg)](https://www.python.org/downloads/release/python-3106/)
[![Poetry Version](https://img.shields.io/badge/Poetry-1.5.1-blueviolet.svg)](https://python-poetry.org/docs/)


The Vacancy Parser is a Python project that utilizes the HeadHunter API to retrieve job vacancies and employers based on specific criteria. It provides a convenient way to search and filter job listings and obtain details about the corresponding companies.


## Installation

To install and set up the project using Poetry, follow the steps below:

1. Make sure you have Poetry installed. If you don't, you can install it by following the official [Poetry installation guide](https://python-poetry.org/docs/#installation).

2. Clone the repository to your local machine:
   ```shell
   git clone https://github.com/tigran-saatchyan/vacollector_hh.git
   ```

3. Navigate to the project directory:
   ```shell
   cd vacolector_hh
   ```

4. Use Poetry to install the project dependencies:
   ```shell
   poetry install
   ```

5. Activate the virtual environment created by Poetry:
   ```shell
   poetry shell
   ```
6. Create database.ini in the project directory vacolector_hh/vacolector_hh:
   ```shell
   [postgres]
   host = 
   user = 
   password = 
   port = 
   ```
7. Start using the Vacancy Parser!

## Usage

The project provides a command-line interface (CLI) for interacting with the HeadHunter API and retrieving job vacancies and employers.

To run the Vacancy Parser, use the following command:
```shell
python vacolector_hh/main.py [command]
```
To run the Vacancy Parser no parameters to be passed to the `[command]`

For detailed information about the available commands and options, run:
```shell
python vacolector_hh/main.py --help
```

## Contributing

Contributions to the Vacancy Parser project are welcome! If you find a bug, have a suggestion, or want to contribute new features, please follow these steps:

1. Fork the repository on GitHub.

2. Create a new branch from the `main` branch with a descriptive name:
   ```shell
   git checkout -b feature/my-new-feature
   ```

3. Make your changes, ensuring that your code adheres to the project's coding style.

4. Write tests for your new features or modifications to maintain good test coverage.

5. Run the test suite and ensure that all tests pass:
   ```shell
   poetry run pytest
   ```

6. Commit your changes with a clear and descriptive commit message:
   ```shell
   git commit -m "Add my new feature"
   ```

7. Push your branch to your forked repository on GitHub:
   ```shell
   git push origin feature/my-new-feature
   ```

8. Open a pull request on the main repository and provide a clear description of your changes.

## License

The Vacancy Parser project is released under the [MIT License](https://github.com/tigran-saatchyan/vacollector_hh/blob/develop/LICENSE).

## Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tigran-o-saatchyan/)
---

Happy parsing! If you have any questions or need assistance, please don't hesitate to reach out.