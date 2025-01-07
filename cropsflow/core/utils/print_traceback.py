import sys
import traceback


def print_traceback(excluded_packages=None):
    if excluded_packages is None:
        excluded_packages = []
    excluded_packages.append('cropsflow')
    # Extract the complete traceback
    exc_type, exc_value, exc_tb = sys.exc_info()
    tb = traceback.extract_tb(exc_tb)

    # Filter the traceback by excluding any frames with paths from the excluded_packages list
    for frame in tb:
        if not any(excluded in frame.filename for excluded in excluded_packages):
            print(f'  File "{frame.filename}", line {frame.lineno}, in {frame.name}')
            print(f'    {frame.line.strip()}')

    # Finally, print the error message itself
    print(f'{exc_type.__name__}: {exc_value}')
