import os
import hashlib

root_folder = 'H:\\test_folder'

def AbsPath(*args):
    abs_path = os.path.join(root_folder, *args)
    return abs_path


def FoldersInFolder(folder):
    objects = os.walk(folder).__next__()
    if objects:
        AbsPathFolders = []
        for folder in objects[1]:
            AbsPathFolders.append(AbsPath(folder))
        return AbsPathFolders


def FilesInFolder(folder):
    objects = os.walk(folder).__next__()
    if objects:
        AbsPathFiles = []
        for file in objects[2]:
            AbsPathFiles.append(AbsPath(folder, file))
        return AbsPathFiles


def GetHashMD5(filename='', string=''):
    if filename:
        with open(filename, 'rb') as f:
            m = hashlib.md5()
            while True:
                data = f.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()
    if string:
        hash_string = hashlib.md5(string.encode()).hexdigest()
        return hash_string

ListFoldersHash = {}
if FoldersInFolder(root_folder):
    DirCount = 0
    for folder in FoldersInFolder(root_folder):
        if folder:
            DirCount += 1
            FolderHashTemp = ''
            files = FilesInFolder(folder)
            if files:
                FileCount = 0
                for file in files:
                    FileCount += 1
                    FileHash = GetHashMD5(filename=file)
                    FolderHashTemp += FileHash
                    print(FolderHashTemp)
                    FolderHash = GetHashMD5(string=FolderHashTemp)
            print('Final:', FolderHash)
            ListFoldersHash[folder] = FolderHash

print(ListFoldersHash)



def main():
    pass

if __name__ == '__main__':
    main()