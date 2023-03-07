import shutil, os
import tempfile

def create_temporary_copy(path, file_name, temp_dir):
    temp_path = os.path.join(temp_dir.name, file_name)
    shutil.copy2(path, temp_path)
    return temp_path

working_directory = tempfile.TemporaryDirectory(prefix='git-kedegit-')
db_file_name = 'empty_config.yaml'
db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../tests/data')) + '/' + db_file_name
temp_file_path = create_temporary_copy(db_file_path, 'config.yaml', working_directory)
os.environ['KEDEGITDIR'] = working_directory.name