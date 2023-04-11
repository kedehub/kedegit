import unittest
from kedehub.__main__ import parse_args
import re

def split_arg_string(string):
    """Given an argument string this attempts to split it into small parts."""
    rv = []
    for match in re.finditer(r"('([^'\\]*(?:\\.[^'\\]*)*)'"
                             r'|"([^"\\]*(?:\\.[^"\\]*)*)"'
                             r'|\S+)\s*', string, re.S):
        arg = match.group().strip()
        if arg[:1] == arg[-1:] and arg[:1] in '"\'':
            arg = arg[1:-1].encode('ascii', 'backslashreplace') \
                .decode('unicode-escape')
        try:
            arg = type(string)(arg)
        except UnicodeError:
            pass
        rv.append(arg)
    return rv

class ArgparseTest(unittest.TestCase):

    def _parse(self, args, **kwargs):
        return parse_args(split_arg_string(args))

    def test_init_project_parsed(self):
        args = self._parse('init-project azbg_virtual_pos ~/git/azbg_virtual_pos --configuration ./kede-config.json')
        self.assertEqual('azbg_virtual_pos', args.project)
        self.assertEqual('~/git/azbg_virtual_pos', args.repository)
        self.assertEqual('./kede-config.json', args.configuration)
        self.assertEqual(None, args.earliest_commit_date)
        self.assertEqual('init-project', args.subparser_name)

    def test_init_project_parsed_no_config(self):
        args = self._parse('init-project azbg_virtual_pos ~/git/azbg_virtual_pos')
        self.assertEqual('azbg_virtual_pos', args.project)
        self.assertEqual('~/git/azbg_virtual_pos', args.repository)
        self.assertIsNone(args.configuration)
        self.assertEqual(None, args.earliest_commit_date)
        self.assertEqual('init-project', args.subparser_name)

    def test_init_project_parsed_no_config_earlest_date(self):
        args = self._parse('init-project azbg_virtual_pos ~/git/azbg_virtual_pos --earliest-commit-date "2020-01-01" ')
        self.assertEqual('azbg_virtual_pos', args.project)
        self.assertEqual('~/git/azbg_virtual_pos', args.repository)
        self.assertIsNone(args.configuration)
        self.assertEqual('2020-01-01', args.earliest_commit_date)
        self.assertEqual('init-project', args.subparser_name)

    def test_list_sources_parsed(self):
        args = self._parse('list-sources ~/git/azbg_virtual_pos --configuration ./kede-config.json')
        self.assertEqual('~/git/azbg_virtual_pos', args.repository)
        self.assertEqual('./kede-config.json', args.configuration)
        self.assertEqual('list-sources', args.subparser_name)

    def test_update_project_parsed(self):
        args = self._parse('update-projects -p azbg_virtual_pos')
        self.assertListEqual(['azbg_virtual_pos'], args.project)
        self.assertEqual('update-projects', args.subparser_name)

    def test_update_projects_parsed(self):
        args = self._parse('update-projects -p azbg_virtual_pos azbg_onko_calc')
        self.assertListEqual(['azbg_virtual_pos', 'azbg_onko_calc'], args.project)
        self.assertEqual('update-projects', args.subparser_name)

    def test_update_project_parsed_all(self):
        args = self._parse('update-projects')
        self.assertIsNone(args.project)
        self.assertEqual(False, args.temp)
        self.assertEqual('update-projects', args.subparser_name)

    def test_update_project_parsed_all_temp(self):
        args = self._parse('update-projects --temp')
        self.assertIsNone(args.project)
        self.assertEqual(True, args.temp)
        self.assertEqual('update-projects', args.subparser_name)

    def test_update_project_parsed_all_clean(self):
        args = self._parse('update-projects --clean')
        self.assertIsNone(args.project)
        self.assertEqual(True, args.clean)
        self.assertEqual('update-projects', args.subparser_name)

    def test_update_project_parsed_all_no_clean(self):
        args = self._parse('update-projects')
        self.assertIsNone(args.project)
        self.assertEqual(False, args.clean)
        self.assertEqual('update-projects', args.subparser_name)

    def test_add_repository_parsed(self):
        args = self._parse('add-repository azbg_virtual_pos ~/projects/baffle-common --configuration ./kede-config.json')
        self.assertEqual('azbg_virtual_pos', args.project)
        self.assertEqual('~/projects/baffle-common', args.repository)
        self.assertEqual('./kede-config.json', args.configuration)
        self.assertEqual(None, args.earliest_commit_date)
        self.assertEqual('add-repository', args.subparser_name)

    def test_add_repository_parsed_no_config(self):
        args = self._parse('add-repository azbg_virtual_pos ~/projects/baffle-common')
        self.assertEqual('azbg_virtual_pos', args.project)
        self.assertEqual('~/projects/baffle-common', args.repository)
        self.assertIsNone(args.configuration)
        self.assertEqual(None, args.earliest_commit_date)
        self.assertEqual('add-repository', args.subparser_name)

    def test_stats_calculate_wekly_kede_parsed(self):
        args = self._parse('stats calculate-weekly-kede -p azbg_virtual_pos')
        self.assertEqual(['azbg_virtual_pos'], args.project)
        self.assertEqual('calculate-weekly-kede', args.type)
        self.assertEqual('stats', args.subparser_name)

    def test_ranklist_today_parsed(self):
        args = self._parse('ranklist calculate -td 2021-2-15')
        self.assertEqual('2021-2-15', args.today)
        self.assertEqual('calculate', args.type)
        self.assertEqual('ranklist', args.subparser_name)

    def test_ranklist_today_and_last_week_parsed(self):
        args = self._parse('ranklist calculate -lw 2020-4-13 -td 2021-2-15')
        self.assertEqual('2021-2-15', args.today)
        self.assertEqual('2020-4-13', args.last_week)
        self.assertEqual('calculate', args.type)
        self.assertEqual('ranklist', args.subparser_name)

    def test_stats_parsed(self):
        args = self._parse('stats calculate-kede -p azbg_virtual_pos')
        self.assertEqual(['azbg_virtual_pos'], args.project)
        self.assertEqual('calculate-kede', args.type)
        self.assertEqual('stats', args.subparser_name)

    def test_stats_parsed_calculate_kede_author(self):
        args = self._parse('stats calculate-kede -p azbg_virtual_pos -a "Stephan Tual <stephan.tual@gmail.com>"')
        self.assertEqual(['azbg_virtual_pos'], args.project)
        self.assertEqual(['Stephan Tual <stephan.tual@gmail.com>'], args.author)
        self.assertEqual('calculate-kede', args.type)
        self.assertEqual('stats', args.subparser_name)

    def test_templates_parsed_author(self):
        args = self._parse('templates find -a "Dimitar <dimitar>" -r w')
        self.assertEqual(None, args.project)
        self.assertListEqual(['Dimitar <dimitar>'], args.author)
        self.assertEqual('find', args.type)
        self.assertEqual('templates', args.subparser_name)
        self.assertEqual('w', args.reporting_interval)

    def test_templates_parsed_project(self):
        args = self._parse('templates find -p azbg_virtual_pos -r w')
        self.assertEqual(None, args.author)
        self.assertListEqual(['azbg_virtual_pos'], args.project)
        self.assertEqual('find', args.type)
        self.assertEqual('templates', args.subparser_name)
        self.assertEqual('w', args.reporting_interval)

    def test_templates_parsed_projects(self):
        args = self._parse('templates find -p azbg_virtual_pos azbg_digital_health_id -r w')
        self.assertEqual(None, args.author)
        self.assertListEqual(['azbg_virtual_pos', 'azbg_digital_health_id'], args.project)
        self.assertEqual('find', args.type)
        self.assertEqual('templates', args.subparser_name)
        self.assertEqual('w', args.reporting_interval)

    def test_templates_parsed_author_and_project(self):
        args = self._parse('templates find -a "Dimitar <dimitar>" -p azbg_virtual_pos -r w')
        self.assertListEqual(['Dimitar <dimitar>'], args.author)
        self.assertListEqual(['azbg_virtual_pos'], args.project)
        self.assertEqual('find', args.type)
        self.assertEqual('templates', args.subparser_name)
        self.assertEqual('w', args.reporting_interval)

    def test_summary_parsed(self):
        args = self._parse('summary azbg_virtual_pos')
        self.assertEqual('azbg_virtual_pos', args.project)
        self.assertEqual('summary', args.subparser_name)

    def test_liast_projects_parsed(self):
        args = self._parse('list-projects')
        self.assertEqual('list-projects', args.subparser_name)

    def test_bulk_import_repos_github(self):
        args = self._parse('clone-import-github --workdir ~/git/facebook --org facebook --token 325103ac88ae8a937be2aef635bcd194696b6d0a')
        self.assertEqual('~/git/facebook', args.workdir)
        self.assertEqual('facebook', args.org)
        self.assertEqual('325103ac88ae8a937be2aef635bcd194696b6d0a', args.token)
        self.assertEqual(False, args.temp)
        self.assertEqual('clone-import-github', args.subparser_name)

    def test_bulk_import_repos_github_temp_folder(self):
        args = self._parse('clone-import-github --temp --workdir ~/git/facebook --org facebook --token 325103ac88ae8a937be2aef635bcd194696b6d0a')
        self.assertEqual('~/git/facebook', args.workdir)
        self.assertEqual('facebook', args.org)
        self.assertEqual('325103ac88ae8a937be2aef635bcd194696b6d0a', args.token)
        self.assertEqual(True, args.temp)
        self.assertEqual('clone-import-github', args.subparser_name)

    def test_bulk_import_repos_gogs(self):
        args = self._parse('clone-import-gogs --workdir ~/git/eLando --host "http://git.elando.bg" --username "dimitar.bakardzhiev" --token 0670a7aa94afc74c587cbf856ea84c0383287308')
        self.assertEqual('~/git/eLando', args.workdir)
        self.assertEqual('http://git.elando.bg', args.host)
        self.assertEqual('dimitar.bakardzhiev', args.username)
        self.assertEqual('0670a7aa94afc74c587cbf856ea84c0383287308', args.token)
        self.assertEqual(False, args.temp)
        self.assertEqual('clone-import-gogs', args.subparser_name)

    def test_bulk_import_repos_gogs_temp_folder(self):
        args = self._parse('clone-import-gogs --temp --workdir ~/git/eLando --host "http://git.elando.bg" --username "dimitar.bakardzhiev" --token 0670a7aa94afc74c587cbf856ea84c0383287308')
        self.assertEqual('~/git/eLando', args.workdir)
        self.assertEqual('http://git.elando.bg', args.host)
        self.assertEqual('dimitar.bakardzhiev', args.username)
        self.assertEqual('0670a7aa94afc74c587cbf856ea84c0383287308', args.token)
        self.assertEqual(True, args.temp)
        self.assertEqual('clone-import-gogs', args.subparser_name)

    def test_bulk_import_repos_gitlab_server(self):
        args = self._parse('clone-import-gitlab-server --workdir ~/git/cisl --host "https://cisl.allianz.at/git/" --token 3v5Qnqx61Lnn1GtxRZzB')
        self.assertEqual('~/git/cisl', args.workdir)
        self.assertEqual('https://cisl.allianz.at/git/', args.host)
        self.assertEqual('3v5Qnqx61Lnn1GtxRZzB', args.token)
        self.assertEqual('clone-import-gitlab-server', args.subparser_name)

    def test_bulk_import_repos_bitbucket_cloud(self):
        args = self._parse('clone-import-bitbucket-cloud --workdir ~/git/taller --workspaceid "tallertechnologiesbulgaria" --username "dimitar_bakardzhiev" --pwd 9711324aA!')
        self.assertEqual('~/git/taller', args.workdir)
        self.assertEqual('tallertechnologiesbulgaria', args.workspaceid)
        self.assertEqual('dimitar_bakardzhiev', args.username)
        self.assertEqual('9711324aA!', args.pwd)
        self.assertEqual('clone-import-bitbucket-cloud', args.subparser_name)

    def test_fix_wrongly_calculated_kede(self):
        args = self._parse('fix-kede -p azbg_virtual_pos')
        self.assertEqual('fix-kede', args.subparser_name)
        self.assertListEqual(['azbg_virtual_pos'], args.project)

    def test_clone_github_epo(self):
        args = self._parse('clone-github-repo --workdir ~/git/facebook --org facebook --token 325103ac88ae8a937be2aef635bcd194696b6d0a')
        self.assertEqual('~/git/facebook', args.workdir)
        self.assertEqual('facebook', args.org)
        self.assertEqual('325103ac88ae8a937be2aef635bcd194696b6d0a', args.token)
        self.assertEqual(False, args.temp)
        self.assertEqual('clone-github-repo', args.subparser_name)

if __name__ == '__main__':
    unittest.main()
