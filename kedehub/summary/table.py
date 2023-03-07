from beautifultable import BeautifulTable

from kedehub.services.commit_service import get_project_commits


class NoDataForTableError(Exception):
    pass

def _make_table(columns):
    table = BeautifulTable()
    table.set_style(BeautifulTable.STYLE_COMPACT)
    table.columns.header = columns
    for column in columns:
        if column == 'Author':
            table.columns.alignment[column] = BeautifulTable.ALIGN_LEFT
        else:
            table.columns.alignment[column] = BeautifulTable.ALIGN_RIGHT
    return table


def commit_count_table( project_name):
    commit_counts = {}
    for commit in get_project_commits(project_name):
        commit_counts[commit.author_name] = commit_counts.get(commit.author_name, 0) + 1
    table = _make_table(['Author', 'Commits'])
    for author_name, commit_count in commit_counts.items():
        table.append_row([author_name, commit_count])
    table.rows.sort('Commits', reverse=True)
    return table

