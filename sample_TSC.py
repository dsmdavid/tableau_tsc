import tableauserverclient as TSC
from pathlib import Path
import os
from log import MyLogger
from functools import wraps
from datetime import datetime
import argparse

import sys

TABLEAU_PAT_NAME = os.environ['tableau_pat_name']
TABLEAU_PAT_TOKEN = os.environ['tableau_pat_token']
TABLEAU_SITE = os.environ['tableau_site']

logger = MyLogger(log_file='tableau.log', log_path='logs', name=__name__)

# tableau_auth = TSC.TableauAuth('USERNAME', 'PASSWORD', 'SITENAME')
tableau_auth = TSC.PersonalAccessTokenAuth(TABLEAU_PAT_NAME,
        TABLEAU_PAT_TOKEN,
        TABLEAU_SITE)

server = TSC.Server('https://10ax.online.tableau.com/', use_server_version=True)

def log_start(func):
    @wraps(func)
    def call(*arg, **kwargs):
        logger.debug(f'Starting function {func.__name__}')
        return func(*arg, **kwargs)
    return call 

def login(func):
    @wraps(func)
    def login(*args, **kwargs):
        logger.debug(f'Logging in from {func.__name__}')
        with server.auth.sign_in(tableau_auth):
            return func(*args, **kwargs)
    return login

# with server.auth.sign_in(tableau_auth):
#     all_datasources, pagination_item = server.datasources.get()
#     print("\nThere are {} datasources on site: ".format(pagination_item.total_available))
#     print([datasource.name for datasource in all_datasources])
#     all_workbooks = list(TSC.Pager(server.workbooks))
#     print('all_workbooks')
#     print(all_workbooks)
#     all_project_items = list(TSC.Pager(server.projects))
#     print([proj.name for proj in all_project_items])
#     items =[(proj.id, proj.name, proj.parent_id, proj.description, proj.content_permissions) for proj in all_project_items] # if proj.name in ('child_github_1', 'parent_github_1')]
#     for item in items:
#         print(item)
#     for proj in all_project_items:
#         if proj.parent_id is None:
#             print(proj.name)

def upload_file(filepath):
    print(filepath)

@log_start    
@login
def get_project(parent_id=None,project_name='default', tableau_auth=tableau_auth):
    # with server.auth.sign_in(tableau_auth):
    all_project_items = list(TSC.Pager(server.projects))
    project = [proj for proj in all_project_items if proj.name == project_name and proj.parent_id == parent_id]
    if project:
        return project[0]
    else:
        return None

@log_start    
@login
def create_project(parent_id=None,project_name='', description='',content_permissions='LockedToProject', **kwargs):
    with server.auth.sign_in(tableau_auth):
        new_project = TSC.ProjectItem(name=project_name,
                content_permissions=content_permissions,
                parent_id=parent_id,
                description=description)                
        # # create the project
        new_project = server.projects.create(new_project)
        logger.info(f'{new_project.name, new_project.id} was created')
        return new_project

def process_full_path(filename):
    ''' Checks that the full hierarchy of projects used
    exists, or creates it.
    receives a filename with relative path:
    ./parent_github_1/child_github_3/WorkoutWednesday-2021-19-Layers.twbx
    checks that "parent_github_1
    returns the project_id of the last children
    '''
    p = Path(filename)
    parent = p.parts[0]
    resource = p.parts[-1]
    project =  get_project(project_name=parent)
    if not project:
        project = create_project(project_name=parent)
    # creare all intermediate steps
    for position in range(1,len(p.parts)-1):
        previous_id = project.id or None
        project =  get_project(project_name=p.parts[position], parent_id=previous_id)
        if not project:
            project = create_project(project_name=p.parts[position], parent_id=previous_id)
        # process intermediate
    logger.debug(f'Finished processing full path forxs {filename}')
    return project.id

def modified_files():
    '''sample code to return modified files'''
    lf = []
    for root, dirs, files in os.walk('.', topdown=False):
        lf.extend([os.path.join(root, name) for name in files])
    return lf

    print('start_processing')
    print(process_full_path(sample))
    print('end_processing')

def identify_type(filename):
    '''Receives the filename, with extension.
    Four valid options:
    - twb
    - twbx
    - tds
    - tdsx
    Anything else will result in a: 'skip' option
    returns the type
    '''
    extension = os.path.splitext(filename)[1]
    if extension == '.twb':
        pass
    elif extension == '.twbx':
        upload_file
    elif extension == '.tds':
        pass
    elif extension == '.tdsx':
        pass
    else:
        return 'skip'

@log_start
def assign_types(list_of_modified_files):
    types = ['.twb','.twbx','.tds','.tdsx']
    types = {t:[] for t in types}
    for filename in list_of_modified_files:
        types[os.path.splitext(filename)[1]].append(filename)

if __name__ == '__main__':
    with open('modified_files.txt','r') as f:
        lf = f.read()
    print(lf)
    lf = lf.replace('"','').replace('\n','').replace("'",'')
    lf = lf.split(' ')
    lf = list(filter(lambda x: 'twb' in x or 'tds' in x, lf))
    print(lf)
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--modified', help='Files to process as a space separated list', required=False)
    # args = parser.parse_args()
    # print('Modified files passed:')
    # print(args.modified)
    # lf = args.modified
    if not lf:
        lf = modified_files()

    twbx = list(filter(lambda x: 'twbx' in x, lf))
    print(twbx)
    sample = twbx[0]
    print(sample)
    process_full_path(sample)
## adding a comment    

# does the parent project exist?
# parents = {proj.name:proj.id for proj in all_project_items if not proj.parent_id}
# print('Project that we are checking == ', parent)
# if not get_project(project_name=parent):
#     new_project = create_project(project_name=parent)

# if parent in parents:
#     print(f'{parent} project exists')
# else:
#     # create project:
#     with server.auth.sign_in(tableau_auth):
#         new_project = TSC.ProjectItem(name=parent, content_permissions='LockedToProject')
#         # # create the project
#         new_project = server.projects.create(new_project)
#         print(f'{new_project.name, new_project.id} was created')

# Check if the project exists, create if not:

    # for proj in all_project_items:
    #     print(f'\nPrinting {proj.id}\n')
    #     print(proj.__dict__)
    # new_project = TSC.ProjectItem(name='child_github_1.2', content_permissions='LockedToProject', description='Project created for testing', parent_id='10627a18-93a5-43c8-95e2-add109825b80')
    # # # create the project
    # new_project = server.projects.create(new_project)
    # print(new_project.__dict__)
    # print('\n\n\nUpdated projects \n\n\n')
    # all_project_items, pagination_item = server.projects.get()

    # items =[(proj.id, proj.name, proj.parent_id, proj.description, proj.content_permissions) for proj in all_project_items] # if proj.name in ('child_github_1', 'parent_github_1')]
    # for item in items:
    #     print(item)
# print(all_project_items)
# print(all_project_items[0].id)
# def parse_relations(lines):
#     relations = {}
#     splitted_lines = ([line.id, line.parent_id] for line in lines)
#     for parent, child in splitted_lines:
#         relations.setdefault(parent, []).append(child)
#     return relations

# def flatten_hierarchy(relations, parent='Earth'):
#     try:
#         children = relations[parent]
#         for child in children:
#             sub_hierarchy = flatten_hierarchy(relations, child)
#             for element in sub_hierarchy:
#                 try:
#                     yield (parent, *element)
#                 except TypeError:
#                     # we've tried to unpack `None` value,
#                     # it means that no successors left
#                     yield (parent, child)
#     except KeyError:
#         # we've reached end of hierarchy
#         yield None

# relations = parse_relations(all_project_items)
# hierarchy = list(flatten_hierarchy(relations))
# print(hierarchy)


# from treelib import Node, Tree
# tree = Tree()
# tree.create_node("Product Catalogue", 0)
# # Creating nodes under root
# for item in all_project_items:
#     for i, c in [item['id'], item['parent_id']]:
#         tree.create_node(item["name"], c["category_id"], parent=0)
# # Moving nodes to reflect the parent-child relationship
# # for i, c in categories_df.iterrows():
# #     if c["parent_id"] == c["parent_id"]:
# #         tree.move_node(c["category_id"], c["parent_id"])
# tree.show()