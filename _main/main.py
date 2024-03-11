import os
import sys
import subprocess
import json
import shutil
import time
from pathlib import Path
from typing import List
from dataclasses import dataclass, field

name = 'AyaPingPing (Py)'
version = 'v4.3.7'
path_separator = os.path.sep


@dataclass
class FeatureDependency:
    domains: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    commons: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)


@dataclass
class Feature:
    name: str = ''
    path: str = ''
    project_path: str = ''
    feature_dependency: FeatureDependency | None = None


class Features(List[Feature]):
    pass


def main():
    print(name + ' ' + version)

    for i in range(len(sys.argv)):
        if sys.argv[i] == 'importFeature':
            import_feature(sys.argv[i + 1:])
            sys.exit(1)

        if sys.argv[i] == 'importDomain':
            import_domain(sys.argv[i + 1:])
            sys.exit(1)

        if sys.argv[i] == 'importCommon':
            import_common(sys.argv[i + 1:])
            sys.exit(1)

    create_new_project()


def create_new_project():
    reader = input_reader()
    project_name = read_input(reader, 'Enter project name (ex: my-project)... ', False)

    print('')
    print('Project name: ' + project_name)
    print('')

    confirmation = read_input(reader, 'Type `y` and press Enter to confirm. Otherwise, the process will be aborted... ',
                              False)
    if confirmation != 'y':
        raise ValueError('process aborted')

    print('')

    if check_file_or_dir_exist(project_name):
        raise ValueError('project `' + project_name + '` already exists, so aborted')

    runtime_dir_contents = get_runtime_dir_contents()

    create_dir(project_name)

    try:
        for path in runtime_dir_contents:
            path_split = path.split(path_separator + '_base_structure' + path_separator)
            len_path_split = len(path_split)

            if is_file(path) and len_path_split == 1:
                destination_path = project_name + path_separator + Path(path_split[0]).name

                copy_file(path, destination_path)

            if is_file(path) and len_path_split >= 2:
                copy_file(path, project_name + path_separator + path_split[-1])

        exec_venv(project_name)
        exec_pip_install_requirements(project_name)
        copy_file(project_name+path_separator+'.env.example', project_name+path_separator+'.env')

    except Exception as e:
        remove_project(project_name)
        print(e)

    print('')
    print('Project created!')


def import_feature(args):
    if len(args) != 3 or args[1] != 'from':
        raise ValueError(
            'invalid `importFeature` arguments, please follow: importFeature [feature1,feature2,...] from ['
            '/local/project or https://example.com/user/project.git or git@example.com:user/project.git]')

    if len(args[0]) < 1 or args[0] == ' ':
        raise ValueError('feature name cannot be empty or blank space')

    if len(args[2]) < 1 or args[2] == ' ':
        raise ValueError('argument `from` cannot be empty or blank space')

    from_path = args[2]

    if is_from_git(from_path):
        try:
            from_path = get_project_path_from_git(from_path)
        except Exception as e:
            remove_dir(from_path)
            print(e)

    print('Checking features... [RUNNING]')

    feats = collect_features_from_argument(args[0], from_path)

    print('Checking features... [OK]')

    if len(feats) > 0:
        print('')
        reader = input_reader()
        print('Features to be imported from `' + from_path + '`: ')

        for feat in feats:
            if feat is None:
                continue

            print('----------------------------------------------------')
            print('Name: ' + feat.name)

            if feat.feature_dependency is None:
                print('Dependency: none (possible missing packages)')
            else:
                print(f'Dependency: Domains: {feat.feature_dependency.domains}')
                print(f'            Commons: {feat.feature_dependency.commons}')
                print(f'            Requirements: {feat.feature_dependency.requirements}')
                print(f'            Other Features: {feat.feature_dependency.features}')

        print('')

        confirmation = read_input(reader,
                                  'Type `y` and press Enter to confirm. Otherwise, the process will be aborted... ',
                                  False)
        if confirmation != 'y':
            raise ValueError('process aborted')

        print('')

    else:
        raise ValueError('no feature found to be imported')

    print('Adding features... [RUNNING]')

    total_imported = 0

    for feat in feats:
        if feat is None:
            continue

        try:
            copy_dir(from_path, feat.path, 'features' + path_separator + feat.name)
        except Exception as e:
            print(e)
            continue

        total_imported += 1

        if feat.feature_dependency:
            for domain_filepath in feat.feature_dependency.domains:
                try:
                    copy_file(feat.project_path + path_separator + 'domain' + path_separator + domain_filepath,
                              'domain' + path_separator + domain_filepath)
                except Exception as e:
                    print(e)
                    continue

            for common_filepath in feat.feature_dependency.commons:
                try:
                    copy_file(feat.project_path + path_separator + 'common' + path_separator + common_filepath,
                              'common' + path_separator + common_filepath)
                except Exception as e:
                    print(e)
                    continue

            for requirement in feat.feature_dependency.requirements:
                try:
                    exec_pip_install_package('', requirement)
                    exec_pip_freeze_requirements('')
                except Exception as e:
                    print(e)
                    continue

    print('Adding features... [OK]')

    print(f'{total_imported} feature(s) imported')

    return None


def import_domain(args):
    if len(args) != 3 or args[1] != 'from':
        raise ValueError(
            'invalid `importDomain` arguments, please follow: importDomain [domain1.py,domain2.py,...] from ['
            '/local/project or https://example.com/user/project.git or git@example.com:user/project.git]')

    if len(args[0]) < 1 or args[0] == ' ':
        raise ValueError('domain name cannot be empty or blank space')

    if len(args[2]) < 1 or args[2] == ' ':
        raise ValueError('argument `from` cannot be empty or blank space')

    from_path = args[2]

    if is_from_git(from_path):
        try:
            from_path = get_project_path_from_git(from_path)
        except Exception as e:
            remove_dir(from_path)
            print(e)

    print('Checking domains... [RUNNING]')

    domains = args[0].replace(' ', '').split(',')

    print('Checking domains... [OK]')

    if len(domains) > 0:
        print('')
        reader = input_reader()
        print('Domains to be imported from `' + from_path + '`: ')

        for domain in domains:
            print('Name: ' + domain)

        print('')

        confirmation = read_input(reader,
                                  'Type `y` and press Enter to confirm. Otherwise, the process will be aborted... ',
                                  False)
        if confirmation != 'y':
            raise ValueError('process aborted')

        print('')

    else:
        raise ValueError('no domain found to be imported')

    print('Adding domains... [RUNNING]')

    total_imported = 0

    for domain in domains:
        try:
            copy_file(from_path + path_separator + 'domain' + path_separator + domain,
                      'domain' + path_separator + domain)
        except Exception as e:
            print(e)
            continue

        total_imported += 1

    print('Adding domains... [OK]')

    print(f'{total_imported} domain(s) imported')

    return None


def import_common(args):
    if len(args) != 3 or args[1] != 'from':
        raise ValueError(
            'invalid `importCommon` arguments, please follow: importCommon [commonFunction1.py,commonFunction2.py,'
            '...] from [/local/project or https://example.com/user/project.git or git@example.com:user/project.git]')

    if len(args[0]) < 1 or args[0] == ' ':
        raise ValueError('common function name cannot be empty or blank space')

    if len(args[2]) < 1 or args[2] == ' ':
        raise ValueError('argument `from` cannot be empty or blank space')

    from_path = args[2]

    if is_from_git(from_path):
        try:
            from_path = get_project_path_from_git(from_path)
        except Exception as e:
            remove_dir(from_path)
            print(e)

    print('Checking common functions... [RUNNING]')

    commons = args[0].replace(' ', '').split(',')

    print('Checking common functions... [OK]')

    if len(commons) > 0:
        print('')
        reader = input_reader()
        print('Common functions to be imported from `' + from_path + '`: ')

        for common in commons:
            print('Name: ' + common)

        print('')

        confirmation = read_input(reader,
                                  'Type `y` and press Enter to confirm. Otherwise, the process will be aborted... ',
                                  False)
        if confirmation != 'y':
            raise ValueError('process aborted')

        print('')

    else:
        raise ValueError('no common function found to be imported')

    print('Adding common functions... [RUNNING]')

    total_imported = 0

    for common in commons:
        try:
            copy_file(from_path + path_separator + 'common' + path_separator + common,
                      'common' + path_separator + common)
        except Exception as e:
            print(e)
            continue

        total_imported += 1

    print('Adding common functions... [OK]')

    print(f'{total_imported} common function(s) imported')

    return None


def read_input(reader: input, text: str, is_wrong: bool) -> str:
    if is_wrong:
        print(f'Wrong, {text.lower()}', end='')
    else:
        print(text, end='')

    input_str = reader()
    input_str = input_str.strip()

    if not input_str:
        return read_input(reader, text, True)

    return input_str


def input_reader() -> input:
    return input


def get_runtime_dir() -> str:
    return Path(__file__).resolve().parent.__str__()


def get_runtime_dir_contents() -> List[str]:
    runtime_dir = get_runtime_dir()
    len_runtime_dir = len(runtime_dir)

    list_contents = []

    for root, dirs, files in os.walk(runtime_dir):
        path_cut = root[len_runtime_dir:]

        if '__pycache__' not in path_cut:
            if len(files) < 1:
                if len(path_cut) >= 16 and path_cut[:16] == path_separator + '_base_structure':
                    list_contents.append(root)

            for file in files:
                if len(path_cut) >= 16 and path_cut[:16] == path_separator + '_base_structure':
                    list_contents.append(root + path_separator + file)

    return list_contents


def get_dir_contents(dir_path: str) -> List[str]:
    list_contents = []

    for root, dirs, files in os.walk(dir_path):
        if '__pycache__' not in root:
            if len(files) < 1:
                list_contents.append(root)
            for file in files:
                list_contents.append(root + path_separator + file)

    return list_contents


def check_file_or_dir_exist(path: str) -> bool:
    return os.path.exists(path)


def is_dir(path: str) -> bool:
    return os.path.isdir(path)


def is_file(path: str) -> bool:
    return os.path.isfile(path)


def create_dir(dir_path: str):
    print(f'Creating `{dir_path}`... [RUNNING]')

    if check_file_or_dir_exist(dir_path):
        print(f'         `{dir_path}`... [EXIST], so skipping...')
        return

    try:
        os.makedirs(dir_path)
    except Exception as e:
        print(f'         `{dir_path}`... [ERROR], so skipping...')
        print(e)
        return

    print(f'         `{dir_path}`... [OK]')


def copy_file(source_path: str, destination_path: str):
    print(f'Copying `{source_path}`... [RUNNING]')

    create_dir(Path(destination_path).parent.__str__())

    if check_file_or_dir_exist(destination_path):
        print(f'        `{source_path}`... [EXIST], so skipping...')
        return

    try:
        file_data = Path(source_path).read_bytes()
        Path(destination_path).write_bytes(file_data)
    except Exception as e:
        print(f'        `{source_path}`... [ERROR], so skipping...')
        print(e)
        return

    print(f'        `{source_path}`... [OK]')


def copy_dir(source_project_base_path: str, source_path: str, destination_path: str):
    create_dir(destination_path)

    dir_contents = get_dir_contents(source_path)

    for path in dir_contents:
        sub_destination_path = str(Path(path).relative_to(source_project_base_path))

        if len(sub_destination_path) > 0 and sub_destination_path[:1] == path_separator:
            sub_destination_path = sub_destination_path[1:]

        if is_dir(path):
            create_dir(sub_destination_path)

        if is_file(path):
            copy_file(path, sub_destination_path)


def remove_project(dir_path: str):
    shutil.rmtree(dir_path, ignore_errors=True)


def remove_dir(dir_path: str):
    return shutil.rmtree(dir_path, ignore_errors=True)


def exec_venv(project_dir: str):
    print('Executing `python3 -m venv venv`... [RUNNING]')

    cmd = ['python3', '-m', 'venv', 'venv']

    try:
        if project_dir == '':
            subprocess.run(cmd, check=True)
        else:
            subprocess.run(cmd, check=True, cwd=project_dir)
    except subprocess.CalledProcessError as e:
        print('`python3 -m venv venv`... [ERROR], so skipping...')
        print(e)
        return

    print('`python3 -m venv venv`... [OK]')


def exec_pip_install_requirements(project_dir: str):
    print('Executing `venv/bin/pip install -r requirements.txt`... [RUNNING]')

    cmd = ['venv/bin/pip', 'install', '-r', 'requirements.txt']

    try:
        if project_dir == '':
            subprocess.run(cmd, check=True)
        else:
            subprocess.run(cmd, check=True, cwd=project_dir)
    except subprocess.CalledProcessError as e:
        print('`venv/bin/pip install -r requirements.txt`... [ERROR], so skipping...')
        print(e)
        return

    print('`venv/bin/pip install -r requirements.txt`... [OK]')


def exec_pip_install_package(project_dir: str, package_name: str):
    print(f'Executing `venv/bin/pip install {package_name}`... [RUNNING]')

    cmd = ['venv/bin/pip', 'install', package_name]

    try:
        if project_dir == '':
            subprocess.run(cmd, check=True)
        else:
            subprocess.run(cmd, check=True, cwd=project_dir)
    except subprocess.CalledProcessError as e:
        print(f'`venv/bin/pip install {package_name}`... [ERROR], so skipping...')
        print(e)
        return

    print(f'`venv/bin/pip install {package_name}`... [OK]')


def exec_pip_freeze_requirements(project_dir: str):
    print('Executing `venv/bin/pip freeze > requirements.txt`... [RUNNING]')

    cmd = ['venv/bin/pip', 'freeze']

    try:
        if project_dir == '':
            subprocess.run(cmd, stdout=open('requirements.txt', 'w'), check=True)
        else:
            subprocess.run(cmd, stdout=open('requirements.txt', 'w'), check=True, cwd=project_dir)
    except subprocess.CalledProcessError as e:
        print('`venv/bin/pip freeze > requirements.txt`... [ERROR], so skipping...')
        print(e)
        return

    print('`venv/bin/pip freeze > requirements.txt`... [OK]')


def is_from_git(from_str: str) -> bool:
    return '.git' in from_str and ('https://' in from_str or 'http://' in from_str or 'git@' in from_str)


def read_dependency_file(filepath: str) -> FeatureDependency:
    with open(filepath, 'r') as file:
        file_data = file.read()

    dependency = json.loads(file_data)

    return FeatureDependency(**dependency)


def collect_features_from_argument(fea_arg: str, from_path: str) -> Features:
    feats = Features()

    for fea in fea_arg.replace(' ', '').split(','):
        fea_path = from_path + path_separator + 'features' + path_separator + fea

        if not check_file_or_dir_exist(fea_path):
            print(f'`{fea}` feature directory not exist, so skipping...')
            continue

        feature_dependency = None

        feature_dependency_filepath = fea_path + path_separator + 'dependency.json'

        if not check_file_or_dir_exist(feature_dependency_filepath):
            print(f'WARNING, `{fea}` feature `dependency.json` file not exist')
        else:
            try:
                feature_dependency = read_dependency_file(feature_dependency_filepath)
            except Exception as e:
                print(f'WARNING, error when parsing `{fea}` feature `dependency.json` file: {e}')

        feat = Feature(name=fea, path=fea_path, project_path=from_path, feature_dependency=feature_dependency)

        feats.append(feat)

    return feats


def get_project_path_from_git(url: str) -> str:
    tmp_git_project_dir = f'tmp-importFeature-from-git-{time.time_ns()}'

    subprocess.run(['git', 'clone', url, tmp_git_project_dir], check=True)

    return tmp_git_project_dir


if __name__ == '__main__':
    main()
