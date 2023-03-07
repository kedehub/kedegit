from collections import defaultdict
import numpy as np
import pandas as pd
from beautifultable import BeautifulTable
from kedehub import bcolors
from kedehub.services.outliers_service import find_outliers, update_outliers
from kedehub.services.template_service import save_templates
from kedehub.utility.input_utility import get_bool_input


def manage_suspected_templates(current_person):
    template_commits = defaultdict(list)

    suspected_templates = find_outliers(current_person)
    if suspected_templates.empty:
        return suspected_templates
    process_suspected_data(suspected_templates, current_person, template_commits)
    template_commits_df = pd.DataFrame.from_dict(template_commits)

    return template_commits_df

def update_suspected_templates(current_person):
    status = update_outliers(current_person)

    return status

def process_suspected_data(suspected_templates, person, template_commits):
    print('----------------------------------------------------------------')
    print('Templates finding for: ' + bcolors.OKBLUE + person, bcolors.ENDC)
    print('----------------------------------------------------------------')
    gropuped_data = _group_by_commit_date(suspected_templates)
    for row in zip(gropuped_data.index.values,
                   gropuped_data['added_chars'],
                   gropuped_data['deleted_chars']):
        print('For date: ' + np.datetime_as_string(row[0],
                                                   unit='D') + ' there are total of: ')
        print(' - '+bcolors.OKBLUE + f"{row[1]:,}" + bcolors.ENDC+ ' chars added greater tnan UCL' + ' and ')
        print(' - ' + bcolors.OKBLUE + f"{row[2]:,}" + bcolors.ENDC+ ' chars deleted lesser than LCL')
        print('\tOut of all daily commits pick commits that are templetes.')
        # https://stackoverflow.com/questions/20383647/pandas-selecting-by-label-sometimes-return-series-sometimes-returns-dataframe
        suspected_commit = find_commits_for_dates([row[0]], suspected_templates)
        for row1 in zip(suspected_commit['added_chars'],
                        suspected_commit['hexsha'],
                        suspected_commit.index.values,
                        suspected_commit['repository'],
                        suspected_commit['deleted_chars']):
            is_template = get_bool_input(two_tabs() +'repository: ' + row1[3] + '\n'
                                         + two_tabs() +'commit time: ' + str(row1[2]) + '\n'
                                         + two_tabs() + 'hexsha: ' + str(row1[1]) + '\n'
                                         + two_tabs() + 'added chars: ' + bcolors.OKBLUE + f"{row1[0]:,}" + bcolors.ENDC + '\n'
                                         + two_tabs() + 'deleted chars: ' + bcolors.OKBLUE + f"{row1[4]:,}" + bcolors.ENDC + '\n'
                                         + bcolors.HEADER + '\t\t\tType "y" if this commit is a templete: ' + bcolors.ENDC)
            if is_template:
                template_commits['repository'].append(row1[3])
                template_commits['hexsha'].append(row1[1])
                template_commits['added_chars'].append(row1[0])
                template_commits['deleted_chars'].append(row1[4])


def _group_by_commit_date(suspected_templates):
    gropuped_data = suspected_templates \
        .groupby(pd.Grouper(freq='D', level='commit_time')) \
        .agg({'added_chars': 'sum','deleted_chars': 'sum'})
    gropuped_data = gropuped_data[(gropuped_data.T != 0).any()]
    return gropuped_data


def two_tabs():
    return '\t\t'


def ask_to_save_templates(template_commits_df,  person : str):
    if get_template_condirmation(template_commits_df):
        template_commits_df = template_commits_df.drop(['repository'], axis = 1)
        save_templates(template_commits_df, person)
        print('Templates saved.')
    print('----------------------------------------------------------------')


def get_template_condirmation(template_commits_df):
    if template_commits_df.empty:
        print('No templates identified.')
        return False
    print('----------------------------------------------------------------')
    want_to_save_templates = get_bool_input("Below are the templates you have selected:\n"+
                                            str(_make_table(template_commits_df))+'\n'+
                                            bcolors.HEADER + "Are you ready to save the above templates?" + bcolors.ENDC)
    return want_to_save_templates

def _make_table(template_commits_df):
    table = BeautifulTable(maxwidth=200)
    columns = ['Repository','hexsha of the template commit', 'Added chars of template', 'Deleted chars of template']
    table.columns.header = columns
    table.columns.alignment = BeautifulTable.ALIGN_RIGHT
    table.columns.alignment['Repository'] = BeautifulTable.ALIGN_LEFT
    for row in zip(template_commits_df['added_chars'],
                    template_commits_df['hexsha'],
                    template_commits_df['repository'],
                    template_commits_df['deleted_chars']):
        table.append_row([row[2],
                          row[1],
                          (bcolors.OKGREEN + f"{row[0]:,}" + bcolors.ENDC),
                          (bcolors.OKGREEN + f"{row[3]:,}" + bcolors.ENDC)])
    table.rows.sort('Repository')
    return table

def find_commits_for_dates(dates, df):

    suspected_commits = df[df.index.get_level_values('commit_time').normalize().isin(dates)].copy()
    suspected_commits.dropna(inplace = True)
    return suspected_commits