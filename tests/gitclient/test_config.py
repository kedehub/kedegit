import os
import unittest

from kedehub.config import Configuration


class KedeGitConfigurationTest(unittest.TestCase):

    def setUp(self) -> None:
        configuration_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data', 'kede-config.json') #os.path.join(repository_path, 'git-kedegit-config.json')
        self.configuration = Configuration(configuration_file_path)

    def test_non_existent_file_extention(self):
        # test non-existent file extention
        self.assertEqual(False, self.configuration.is_source_file(
            'virtualpos_frontend/src/assets/fonts/AvertaDemoPE-ExtraboldItalic.eot'))
        self.assertEqual(False, self.configuration.is_source_file('virtualpos_frontend/src/assets/fonts/Cargo.lock'))

    def test_included_file_extentions(self):
        # test included file extentions
        self.assertEqual(True, self.configuration.is_source_file('virtualpos_frontend/src/assets/fonts/AvertaDemoPE-ExtraboldItalic.java'))
        self.assertEqual(True, self.configuration.is_source_file(
            'virtualpos_frontend/src/assets/test.json'))
        self.assertEqual(True, self.configuration.is_source_file(
            'virtualpos_frontend/src/assets/fonts/AvertaDemoPE-ExtraboldItalic.ros'))
        self.assertEqual(True, self.configuration.is_source_file(
            'virtualpos_frontend/src/assets/test.txt'))


    def test_excluded_file_names(self):
        # test excluded file names
        self.assertEqual(False,
                         self.configuration.is_source_file('virtualpos_frontend/src/assets/fonts/package-lock.json'))
        self.assertEqual(False, self.configuration.is_source_file('virtualpos_frontend/src/assets/fonts/yarn.lock'))
        self.assertEqual(False, self.configuration.is_source_file('virtualpos_frontend/src/assets/fonts/LICENSE'))
        self.assertEqual(False, self.configuration.is_source_file('virtualpos_frontend/src/assets/asset-manifest.json'))
        self.assertEqual(False, self.configuration.is_source_file('virtualpos_frontend/src/assets/precache-manifest.6a26e0c2e4eedd6141bec241ad88e64f.js'))
        self.assertEqual(False, self.configuration.is_source_file('build/static/js/main.68588f39.chunk.js'))
        self.assertEqual(False, self.configuration.is_source_file('build/static/css/main.899c8c77.chunk.css'))
        self.assertEqual(False, self.configuration.is_source_file('build/static/service-worker.js'))
        self.assertEqual(False, self.configuration.is_source_file('static/LICENSE.txt'))
        self.assertEqual(False, self.configuration.is_source_file('static/js/2.f504fe56.chunk.js.LICENSE.txt'))
        self.assertEqual(False, self.configuration.is_source_file('packages/bridge/contracts/ERC20.json'))
        self.assertEqual(False, self.configuration.is_source_file('packages/bridge/contracts/Wormhole.json'))
        self.assertEqual(False, self.configuration.is_source_file('packages/bridge/contracts/WrappedAsset.json'))
        self.assertEqual(False, self.configuration.is_source_file('packages/bridge/src/contracts/Erc20Factory.ts'))
        self.assertEqual(False, self.configuration.is_source_file('packages/bridge/src/contracts/WormholeFactory.ts'))
        self.assertEqual(False, self.configuration.is_source_file('packages/bridge/src/contracts/WrappedAssetFactory.ts'))
        self.assertEqual(False,
                         self.configuration.is_source_file('virtualpos_frontend/src/assets/fonts/npm-shrinkwrap.json'))
        self.assertEqual(False,
                         self.configuration.is_source_file('GangwayForecast.Worker/output.json'))

    def test_excluded_file_extentions(self):
        # test excluded file extentions
        self.assertEqual(False, self.configuration.is_source_file('virtualpos_frontend/src/assets/fonts/test.css.map'))
        self.assertEqual(False, self.configuration.is_source_file('virtualpos_frontend/src/assets/fonts/.gitignore'))
        self.assertEqual(False, self.configuration.is_source_file('virtualpos_frontend/src/assets/fonts/.env'))
        self.assertEqual(False, self.configuration.is_source_file('packages/bridge/src/contracts/Erc20.d.ts'))

    def test_excluded_folders(self):
        # test excluded folders
        self.assertEqual(False, self.configuration.is_source_file('virtualpos_frontend/src/image_build/test.java'))

if __name__ == '__main__':
    unittest.main()
