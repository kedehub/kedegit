import os
import unittest
from kedehub import ServerConfiguration
from tests import working_directory, create_temporary_copy


class KEDEGitFormatTestCase(unittest.TestCase):
    def test_non_ascii(self):
        db_file_name = 'test_non_ascii.yaml'
        db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')) + '/' + db_file_name
        temp_file_path = create_temporary_copy(db_file_path, 'config.yaml', working_directory)
        os.environ['KEDEGITDIR'] = working_directory.name

        with self.assertRaises(ValueError) as context:
            server_config = ServerConfiguration()

        self.assertIn("YAML file", str(context.exception))
        self.assertIn("contains non-ASCII characters", str(context.exception))

    def test_with_bom(self):
        db_file_name = 'test_with_bom.yaml'
        db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')) + '/' + db_file_name
        temp_file_path = create_temporary_copy(db_file_path, 'config.yaml', working_directory)
        os.environ['KEDEGITDIR'] = working_directory.name

        with self.assertRaises(ValueError) as context:
            server_config = ServerConfiguration()

        self.assertIn("YAML file", str(context.exception))
        self.assertIn("contains a BOM (Byte Order Mark), which should be removed", str(context.exception))

    def test_missing_keys(self):
        db_file_name = 'test_missing_keys.yaml'
        db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')) + '/' + db_file_name
        temp_file_path = create_temporary_copy(db_file_path, 'config.yaml', working_directory)
        os.environ['KEDEGITDIR'] = working_directory.name

        with self.assertRaises(SystemExit) as context:
            server_config = ServerConfiguration()

        self.assertIn( "Missing required key: 'server.protocol", context.exception.code,)

    def test_missing_config_file(self):
        db_file_name = 'non_existent_file.yaml'
        db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')) + '/' + db_file_name
        os.environ['KEDEGITDIR'] = working_directory.name

        with self.assertRaises(SystemExit) as context:
            server_config = ServerConfiguration()
            server_config.validate_yaml_file(db_file_path)

        self.assertIn(f"YAML file '{db_file_path}' not found!", context.exception.args)

    def test_yaml_formatting_error(self):
        db_file_name = 'test_invalid_yaml.yaml'
        db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')) + '/' + db_file_name
        temp_file_path = create_temporary_copy(db_file_path, 'config.yaml', working_directory)
        os.environ['KEDEGITDIR'] = working_directory.name

        with self.assertRaises(SystemExit) as context:
            server_config = ServerConfiguration()

        self.assertIn(f"Error initializing configuration: ", context.exception.code)


if __name__ == '__main__':
    unittest.main()
