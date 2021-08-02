import os
import hashlib
import settings

root_folder = settings.root_folder1


def AbsPath(*args):
    """
    Construct absolute path with adding to root folder arguments:
    folders and files, take any amount of arguments, order matters
    example: AbsPath(dir1, dir2, dir3, filename) ->
    "rootpath\\dir1\\dir2\\dir3\\filename"
    """
    abs_path = os.path.join(root_folder, *args)
    return abs_path


def FoldersInFolder(folder):  # get list of folders from Folder
    objects = os.walk(folder).__next__()
    if objects:
        AbsPathFolders = []
        for folder in objects[1]:
            AbsPathFolders.append(AbsPath(folder))
        return AbsPathFolders


def FilesInFolder(folder):  # get list of files from Folder
    objects = os.walk(folder).__next__()
    if objects:
        AbsPathFiles = []
        for file in objects[2]:
            AbsPathFiles.append(AbsPath(folder, file))
        return AbsPathFiles


def WalkOnStringAndDecode(string):
    step = 10000  # how many chars slice in a single time
    start = 0
    stop = step

    m = hashlib.md5()
    while True:
        part_of_string = string[start:stop]  #take slice of string
        if not part_of_string:
            break
        m.update(part_of_string.encode())  # encode slice and update data to hashlib object

        start += step  # rise start point for next iteration
        stop += step  # rise end point for next iteration
    return m.hexdigest()  # return that md5 hash from taken data


def WalkOnFileAndDecode(file):
    with open(file, 'rb') as f:  # reading blocks from file and take checksum
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def GetHashMD5(filename='', string=''):  # get hash from file of string
    if filename:
        file_hash = WalkOnFileAndDecode(filename)
        return file_hash
    if string:
        hash_string = hashlib.md5(string.encode()).hexdigest()
        return hash_string


def CheckSameHashInDictionary(dict, hash):  # return hash_id and True if it new hash entry, False if this hash is exists
    for item in dict.items():
        if hash in item[1][0]:
            result = (item[1], False)
            print('hashcheck', result)
            return result
        result = (len(dict) + 1, True)
        return result


def WriteNewFolderHashInDict(mydict, hash_id, folder, folder_hash):
    if folder_hash:
        if hash_id[1] == True:
            mydict[hash_id].append((folder_hash, folder))
        else:
            mydict.update([(hash_id, [(folder_hash, folder)])])
    return mydict



def GetHashFromFoldersList(root_folder):
    dictionary_all_folders_hash = {}
    if FoldersInFolder(root_folder):  # take list of folders in directory and check if it empty
        dir_count = 0  # folders counter
        for folder in FoldersInFolder(root_folder):  # walk on all folders and take hashes from files inside
            if folder:
                dir_count += 1
                folder_hash_temp = ''
                files = FilesInFolder(folder)
                if files:  # check if have some files in directory or in empty
                    FileCount = 0
                    for file in files:
                        FileCount += 1
                        FileHash = GetHashMD5(filename=file)
                        folder_hash_temp += FileHash
                        print(folder_hash_temp)
                        folder_hash = GetHashMD5(string=folder_hash_temp)
                print('Final:', folder_hash)
                hash_id = CheckSameHashInDictionary(dictionary_all_folders_hash, folder_hash)
                print('hash_id = ', hash_id)
                WriteNewFolderHashInDict(dictionary_all_folders_hash, hash_id, folder, folder_hash)  #
    print(dictionary_all_folders_hash)




def main():
    GetHashFromFoldersList(root_folder)


if __name__ == '__main__':
    main()
