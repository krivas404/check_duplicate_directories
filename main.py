import settings as sett
import build_dictionary as build
import working_with_dict as work

"""Directory=parent_folder, folder=child folder from Directory"""


root_folder1 = sett.root_folder1
root_folder3 = sett.root_folder3
disk_save_path = sett.disk_path_where_save_files

def main():
    my_dict = build.main(root_folder1)
    work.main(my_dict, disk_save_path)

if __name__ == '__main__':
    main()