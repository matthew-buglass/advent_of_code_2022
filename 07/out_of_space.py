
class DirNotFoundError(Exception):
    def __init__(self, *args):
        super(DirNotFoundError, self).__init__(*args)


class Directory:
    def __init__(self, name='/', parent=None, root=None, level=0):
        self.name = name
        self.root = root or self
        self.parent = parent or self
        self.level = level
        self.sub_dirs = {}
        self.files = {}

    def __str__(self):
        return "\n".join(self._str_list())

    def sub_dir_sizes(self):
        sizes_str = "{}- {} {}".format('\t'*self.level, self.name, self.size())
        sizes = [sizes_str] + [d.sub_dir_sizes() for d in self.sub_dirs.values()]

        return '\n'.join(sizes)

    def _str_list(self):
        sub_entities = list(self.files.values()) + list(self.sub_dirs.values())
        sub_entities.sort(key=lambda x: x.name)
        sub_entities_str = ["{}{}".format('\t'*(self.level+1),
                                          str(e)) for e in sub_entities]

        self_str = "- {} (dir)".format(self.name)

        self_str_list = [self_str] + sub_entities_str

        return self_str_list

    def add_dir(self, sub_dir):
        self.sub_dirs[sub_dir.name] = sub_dir

    def add_file(self, file):
        self.files[file.name] = file

    def get_dir(self, path):
        if path == '/':
            return self.root

        try:
            dir_name, sub_path = path.split('/', maxsplit=1)
        except ValueError:
            dir_name, sub_path = path.split('/', maxsplit=1) + [None]

        if dir_name == '..':
            return self.parent
        elif dir_name == '.':
            return self
        else:
            try:
                child_dir = self.sub_dirs[dir_name]
            except KeyError:
                raise DirNotFoundError('Cannot find the directory {}'.format(dir_name))

            if sub_path:
                return child_dir.get_dir(sub_path)
            else:
                return child_dir

    def get_all_dirs(self):
        dirs = [self]
        for d in self.sub_dirs.values():
            dirs += d.get_all_dirs()

        return dirs

    def size(self, recursive=True):
        if recursive:
            sub_dir_size = sum([d.size() for d in self.sub_dirs.values()])
        else:
            sub_dir_size = 0

        file_size = sum([f.size for f in self.files.values()])

        return sub_dir_size + file_size


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __str__(self):
        return "- {} (file, size={})".format(self.name, self.size)


def infer_directory(instructions):
    root_dir = Directory()
    current_dir = root_dir

    for i in instructions[1:]:
        if i[0] == '$':  # Command
            cmd = i.lstrip('$ ')
            if cmd[0:2] == 'cd':
                cmd, path_name = cmd.split()
                try:
                    current_dir = current_dir.get_dir(path_name)
                except DirNotFoundError:
                    new_dir = Directory(name=path_name, parent=current_dir, root=root_dir, level=current_dir.level + 1)
                    current_dir.add_dir(Directory(name=path_name))
                    current_dir = new_dir
            elif i[0:2] == 'ls':
                pass
        else:
            type_or_size, name = i.split(' ')
            if type_or_size == 'dir':
                current_dir.add_dir(Directory(name=name, parent=current_dir, root=root_dir, level=current_dir.level + 1))
            else:
                size = int(type_or_size)
                current_dir.add_file(File(name=name, size=size))

    return root_dir


def infer_directory_from_file(file_name):
    with open(file_name, 'r') as f:
        instruct = [l.strip() for l in f.readlines()]

    return infer_directory(instruct)


# Testing
root = infer_directory_from_file('out_of_space_sample_input.txt')

print(root)
print()
print(root.sub_dir_sizes())
print()


# pt 1
root = infer_directory_from_file('out_of_space_intput.txt')
all_dirs_less_than_100000 = [d for d in root.get_all_dirs() if d.size() <= 100000]
print('Sum of the size of dirs whose size is less than 100,000: {}'.format(
    sum([d.size() for d in all_dirs_less_than_100000])
))

# pt 2
total_disk_space = 70000000
min_headroom = 30000000
max_root_size = total_disk_space - min_headroom
remaining_disk_space = total_disk_space - root.size()
space_to_clear = min_headroom - remaining_disk_space

print('Remaining disk space: {}'.format(remaining_disk_space))
print('Space to clear: {}'.format(space_to_clear))

all_dirs_worth_clearing = [d for d in root.get_all_dirs() if d.size() >= space_to_clear]
all_dirs_worth_clearing.sort(key=lambda x: x.size())
dir_to_delete = all_dirs_worth_clearing[0]
print('smallest single directory to delete: {} at size of {}'.format(dir_to_delete.name, dir_to_delete.size()))
