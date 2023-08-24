"""
Module containing all the extensions used in the application
"""



import sys
from dotenv import dotenv_values

env_values = dotenv_values(".env")

# here listed required .env variables
required_variables = [
    "DB_USER",
    "DB_PASSWORD",
    "DB_IP",
    "DB_NAME",
    "DB_TEST_NAME",
    "DB_PORT",
]

class SecurityManager:
    """
    Class containing security related methods
    """

    @staticmethod
    def validate_env():
        """
        Function to validate the .env file
        """
        missing_variables = [var for var in required_variables if var not in env_values]

        if missing_variables:
            missing = list(missing_variables)
            print(f"ERROR: .env variables missing: {missing}")
            sys.exit(1)