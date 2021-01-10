import os


def cwd():
    print(os.getcwd())


def listdir():
    return sorted(os.listdir(), key=lambda i: (not os.path.isdir(i), i))


def ls(force_list=False):
    cwd()
    contents = listdir()
    size = len(contents)
    hint = f'是否显示全部{size}项内容？(y)'
    if size > 100 and not force_list and input(hint).lower() != 'y':
        return
    for i, v in enumerate(contents):
        v = v if not os.path.isdir(v) else "(D) " + v
        print(f'[{i}]:\t{v}')


def cd(i: int):
    contents = listdir()
    os.chdir(contents[i])
    ls()


def cdn(name: str):
    os.chdir(name)
    ls()


def cds():
    cdn('..')


class PathTool:

    @property
    def e(self):
        return exit()

    @property
    def cwd(self):
        return cwd()

    @property
    def ls(self):
        return ls()

    @property
    def lss(self):
        return ls(force_list=True)

    @property
    def cds(self):
        return cds()

    @staticmethod
    def cd(i: int):
        cd(i)

    @staticmethod
    def cdn(name: str):
        cdn(name)

    # raw function wrap
    rcd = os.chdir
    rls = os.listdir
    rcwd = os.getcwd

    def __getattr__(self, item):
        try:
            if item.startswith('cd') and item[2:].isnumeric():
                self.cd(int(item[2:]))
            elif item.startswith('cdn'):
                self.cdn(item[3:])
            else:
                super().__getattribute__(item)
        except Exception as e:
            print(e)
