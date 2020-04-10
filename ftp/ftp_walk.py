from os import path as ospath


class FTPWalk:
    """
    This class is contain corresponding functions for traversing the FTP
    servers using BFS algorithm.
    """

    def __init__(self, connection):
        self.connection = connection

    def listdir(self, _path):
        """
        return files and directory names within a path (directory)
        """

        file_list, dirs, nondirs = [], [], []
        try:
            self.connection.cwd(_path)
        except Exception as exp:
            print("the current path is : ", self.connection.pwd(), exp.__str__(), _path)
            return [], []
        else:
            self.connection.retrlines('LIST', lambda x: file_list.append(x.split()))
            for info, filename in zip(file_list, self.connection.nlst()):
                if info[2] == '<DIR>':
                    dirs.append(filename)
                else:
                    nondirs.append(filename)
            return dirs, nondirs

    def walk(self, path='/'):

        dirs, nondirs = self.listdir(path)
        yield path, dirs, nondirs
        for name in dirs:
            path = ospath.join(path, name)
            yield from self.walk(path)
            self.connection.cwd('..')
            path = ospath.dirname(path)
