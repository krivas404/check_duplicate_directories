import settings as sett
import build_dictionary as build
import working_with_dict as work


root_list = sett.root_list
root_list2 = sett.root_list2
disk_save_path = sett.disk_path_where_save_files

def main():
    my_dict = build.main(root_list2)
    work.main(my_dict, disk_save_path)

if __name__ == '__main__':
    main()