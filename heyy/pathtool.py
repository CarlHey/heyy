import os


def cwd():
    print(os.getcwd())


def ls():
    cwd()
    for i, v in enumerate(os.listdir()):
        print(f'[{i}]:\t{v}')


def cd(i: int):
    os.chdir(os.listdir()[i])
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
