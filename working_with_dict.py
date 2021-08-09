import os.path

count_del = 0
count_save = 0

def SameDirsListFromDict(my_dict):
    dirs_list = []
    count = 0
    for item in my_dict.values():
        count += len(item)
        dirs_list.append(item[1])
    print('dirs list : ', dirs_list)
    print('dirs count =', count)
    return dirs_list


def DeleteNoneSavePathDir(dirs, disk_save_path):
    global count_del
    global count_save
    if dirs:
        for folder in dirs:
            check = CheckIfSavePathInDir(folder, disk_save_path)
            if check:  # build list without disk_save_path and _delete
                count_save += 1
                print('folder.NotDelete =', folder)
            if not check:
                count_del += 1
                print("folder.Delete =", folder)


def CheckIfSavePathInDir(folder, save_path_disk):
    """return True if disk_save_path in dir, else False"""
    folder_disk_letter = os.path.splitdrive(folder)[0]
    save_path_disk_letter = os.path.splitdrive(save_path_disk)[0]
    if len(save_path_disk_letter) == 2 and save_path_disk_letter[1] == ':':
        if folder_disk_letter == save_path_disk_letter:
            return True
        return False
    raise Exception('save_path_disk bad value')


def main(my_dict, disk_save_path):
    dirs_list = SameDirsListFromDict(my_dict)
    if dirs_list:
        for dirs in dirs_list:
            DeleteNoneSavePathDir(dirs, disk_save_path)
            print('main.dirs_list iteration Complete')
    print('count_del =', count_del, '\ncount_save =', count_save)
    print('Finsh')


if __name__ == '__main__':
    main()
