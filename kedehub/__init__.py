
from kedehub.configuration.server_config import ServerConfiguration

server_config = ServerConfiguration()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class DatabaseNotInitializedError(Exception):
    pass


class OldDatabaseSchemaError(Exception):
    pass