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
        hash_string = hashlib.md5(string.encode()).hexdigest()
        return hash_string


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


def GetHashFromFoldersList(root_folder):
    dictionary_all_folders_hash = {}
    folders_in_folder = FoldersInFolder(root_folder) # take list of folders in directory
    if folders_in_folder:  # check if list it empty
        for folder in folders_in_folder:  # walk on all folders and take hashes from files inside
            if folder:
                folder_hash_temp = ''
                files = FilesInFolder(folder)
                if files:  # check if have some files in directory or in empty
                    for file in files:
                        file_hash = GetHashMD5(filename=file)
                        folder_hash_temp += file_hash
                        print(folder_hash_temp)
                folder_hash = GetHashMD5(string=folder_hash_temp)
                print('Final folder hash:', folder_hash)
                hash_id_with_flag = CheckSameHashInDictionary(dictionary_all_folders_hash, folder_hash)
                print('hash_id = ', hash_id_with_flag)
                WriteNewFolderHashInDict(dictionary_all_folders_hash, hash_id_with_flag, folder, folder_hash)  #
    print('Final Progrem Return', dictionary_all_folders_hash)
    print('final test :', dictionary_all_folders_hash == {1: ('8f481cede6d2ddc07cb36aa084d9a64d', ['H:\\test_folder\\bar', 'H:\\test_folder\\foo']), 2: ('3dad9cbf9baaa0360c0f2ba372d25716', ['H:\\test_folder\\cda', 'H:\\test_folder\\zfy'])})
def main():
    GetHashFromFoldersList(root_folder)


if __name__ == '__main__':
    main()