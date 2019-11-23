""" Простой модуль для нахождения одинаковых файлов в выбранных директориях """
import os
import sys
import humanize

FILES = {}
EXCEPT = ['Thumbs.db']


def get_files_recursive(path, local_path=''):
    """
    :param path: path to directory to get files from
    :param local_path: relative to path (needed for recursive launch)
    """
    for file_name in os.listdir(os.path.join(path, local_path)):
        if os.path.isdir(os.path.join(path, local_path, file_name)):
            get_files_recursive(path, os.path.join(local_path, file_name))
        else:
            if file_name in EXCEPT:
                continue
            if file_name not in FILES.keys():
                FILES[file_name] = [os.path.join(path, local_path)]
            else:
                FILES[file_name].append(os.path.join(path, local_path))
                print(f'{file_name}:')
                for same_file in FILES[file_name]:
                    print(f'\t{same_file}')


PATHS = []
if len(sys.argv) == 1:
    PATH_NUM = 1
    print("Введите пустую строку для окончания ввода")
    PATH = input(f"Каталог #{PATH_NUM}: ")
    while PATH != '':
        PATH += 1
        PATHS.append(PATH)
        PATH = input(f"Каталог #{PATH_NUM}: ")
else:
    for PATH_NUM in range(1, len(sys.argv)):
        PATHS.append(sys.argv[PATH_NUM])

for PATH in PATHS:
    get_files_recursive(PATH)

SAME_FILES = {}
for file in FILES:
    if len(FILES[file]) > 1:
        SAME_FILES[file] = FILES[file]

if not SAME_FILES:
    print('Общих файлов не найдено')
    sys.exit(0)

for file in SAME_FILES:
    print(file + ":")
    for file_path in SAME_FILES[file]:
        print(f"\t{file_path}: {humanize.naturalsize(os.path.getsize(file_path))}")

print('Удалить файлы в:')
for i, PATH in enumerate(PATHS):
    print(f'{i + 1}. {PATH}')
print(f'{len(PATHS) + 1}. Решить для каждого файла отдельно')
print(f'{len(PATHS) + 2}. Не удалять файлы')
CHOICE = int(input('>>>'))

for file in SAME_FILES:
    if CHOICE == len(PATHS) + 2:
        pass
    elif CHOICE == len(PATHS) + 1:
        print(file + ':')
        for i in range(len(SAME_FILES[file])):
            print(f'{i + 1}. {SAME_FILES[file][i]}')
        CHOICE = int(input('>>>')) - 1
    else:
        os.remove(os.path.join(SAME_FILES[file][CHOICE], file))
print('Успех')
