import os
import hashlib


all_folders_hash_dict = {}

class MD5(Exception):
    print("Функция  GetHashMD5() не сработала")

def EmptyCheck(string):  # False if string = 'empty'
    if not string == 'empty':
        return True
    if string == 'empty':
        return False
    return True

def AbsPath(*args):
    """
    Construct absolute path with adding to root folder arguments:
    folders and files, take any amount of arguments, order matters
    example: AbsPath(dir1, dir2, dir3, filename) ->
    "rootpath\\dir1\\dir2\\dir3\\filename"
    """
    abs_path = os.path.join(*args)
    return abs_path


def TakeFoldersListFromFolder(my_dir):  # get list of folders from Folder
    objects = os.walk(my_dir).__next__()
    if objects:
        AbsPathFolders = []
        for folder in objects[1]:
            AbsPathFolders.append(AbsPath(my_dir, folder))
        return AbsPathFolders


def TakeFilesListFromFolder(folder):  # get list of files from Folder
    objects = os.walk(folder).__next__()
    if objects:
        AbsPathFiles = []
        for file in objects[2]:
            AbsPathFiles.append(AbsPath(folder, file))
        return AbsPathFiles


def TakeHashFromString(string):
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


def TakeHashFromFile(file):
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
        file_hash = TakeHashFromFile(filename)
        return file_hash
    if string:
        hash_string = TakeHashFromString(string)
        return hash_string
    return 'empty'  # flag about is entry value is empty (it means about folder has no files and no folders, directory is empty)


def CheckSameHashInDictionary(dict, hash):  # return hash_id and True if it new hash entry, False if this hash is exists
    for item in dict.items():
        if hash in item[1][0]:
            result = (item[0], False)
            print('hashcheck', result)
            return result
    result = (len(dict) + 1, True)
    return result


def WriteNewFolderHashInDict(mydict, hash_id_with_flag, folder, folder_hash):
    if folder_hash:
        if hash_id_with_flag[1] == False:   #if hash and key exists in dict
            mydict[hash_id_with_flag[0]][1].append(folder) # на доработку
            print('mydict =', mydict)
            return mydict
        mydict.update({hash_id_with_flag[0]: (folder_hash, [folder])})  # if it new hash and key for dict
        print('mydict =', mydict)
    return mydict


def WriteDirHash(my_dict, my_dir, dir_hash):
    hash_id_with_flag = CheckSameHashInDictionary(my_dict, dir_hash)
    WriteNewFolderHashInDict(my_dict, hash_id_with_flag, my_dir, dir_hash)


def TakeHashFromFoldersInDirectory(parent_folder):
    folders_list = TakeFoldersListFromFolder(parent_folder)
    folders_hash_temp = ''
    if folders_list:
        for folder in folders_list:
            folder_hash = BuildDictionaryFromDirectoryHash(folder)
            if EmptyCheck(folder_hash):
                folders_hash_temp += folder_hash
                print('Folder - folder_hash_temp =', folders_hash_temp)
        if folders_hash_temp:
            folders_hash = GetHashMD5(string=folders_hash_temp)
            print('Folder Folders hash:', folders_hash)
            return folders_hash
    return ''


def TakeHashFromFilesInDirectory(directory):
    folder_hash_temp = ''
    files_list = TakeFilesListFromFolder(directory)
    if files_list:  # check if have some files in directory or in empty
        print('folder :', directory)
        for file in files_list:
            file_hash = GetHashMD5(filename=file)
            if EmptyCheck(file_hash):
                folder_hash_temp += file_hash
        folder_files_hash = GetHashMD5(string=folder_hash_temp)
        print('Folder Files hash:', folder_files_hash)
        return folder_files_hash
    return ''


def TakeAllHashFromDirectory(directory):
    files_hash = TakeHashFromFilesInDirectory(directory)
    folders_hash = TakeHashFromFoldersInDirectory(directory)
    directory_hash_temp = files_hash + folders_hash
    directory_hash = GetHashMD5(string=directory_hash_temp)
    return directory_hash


def BuildDictionaryFromDirectoryHash(my_dir, my_dict=all_folders_hash_dict):
    dir_hash = TakeAllHashFromDirectory(my_dir)
    WriteDirHash(my_dict, my_dir, dir_hash)
    return dir_hash


def DictPrint():
    print('Starting print dict')
    for value in all_folders_hash_dict.values():
        print(value)
    print('Ending print dict')


def main(root_folder):
    BuildDictionaryFromDirectoryHash(root_folder)
    DictPrint()
    return all_folders_hash_dict

if __name__ == '__main__':
    main()