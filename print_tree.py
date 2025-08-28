import os

def print_tree(start_path, prefix=''):
    for i, item in enumerate(os.listdir(start_path)):
        path = os.path.join(start_path, item)
        connector = '├── ' if i < len(os.listdir(start_path)) - 1 else '└── '
        print(prefix + connector + item)
        if os.path.isdir(path):
            extension = '│   ' if i < len(os.listdir(start_path)) - 1 else '    '
            print_tree(path, prefix + extension)

# 시작 경로를 프로젝트 루트 경로로 설정
print_tree('.')
