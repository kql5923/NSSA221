import os
import subprocess
import getpass

def get_home():
    user = getpass.getuser()
    home_path = "/home/"+user+"/Desktop/"
    return home_path
def list_links():
    print("----------------------------")
    path = os.getcwd()
    print("[##] Summary of ",path)
    linked_dirs = {}
    arr = os.listdir()
    total_links = 0
    print("[##] Linked Objects in Path:")
    for each in arr:
        if os.path.islink(each):
            total_links += 1
            print("[", total_links, "]: FILE=",each," Linked to= ",os.readlink(each) )
    print("[##] Total Links:",total_links)
def create_link(file_location):
    print("[##] Moving To Desktop Dirrectory...")
    try:
        os.chdir(get_home())
        path = os.getcwd()
        print("[DONE] Sucessfully moved to user's desktop: ",path)
    except Exception as e:
        print("[ERR] Unable to move: ",e)
        print("[###] WILL NOT BE ABLE TO SHOW LINKS FOR DESKTOP, JUST CURRENT DIRRECTORY!")
    print("[##] Creating System Link on Desktop for file ",file_location)
    split_location = file_location.split("/")
    full_file_name = split_location[len(split_location)-1]
    split_for_symlink = full_file_name.split(".")
    dest = ""
    if(len(split_for_symlink) == 1):
        dest = path + "/" +split_for_symlink[0] + "(symlink)"
    else:
        dest = path + "/" +split_for_symlink[0] + "(symlink)." + split_for_symlink[1]
    try:
        os.symlink(file_location,dest)
    except Exception as e:
        print("[ERR] UNABLE TO LINK!")
def main():
    flag = True
    while(flag == True):
        path = os.getcwd()
        print("[##] Please provide the location for the file you would like to link on the Desktop")
        print("[##] or type 'quit' to quit")
        user_file_to_link = path
        file = input("[>]:")
        if(file == "quit"):
            quit()
        if(os.path.isfile(file) == True):
            print("[+] Valid Dirrectory Given... Continuing...")
            user_file_to_link += file
        else:
            arr = file.split("/")
            print("arr :",arr)
            print("[-] Could not find file with path given. Searching entire filesystem...")
            command_string = "find / -name " + arr[len(arr)-1]
            print(command_string)
            get_file_location = subprocess.Popen(command_string,shell = True, stdout=subprocess.PIPE).stdout
            read_file_location = get_file_location.read()
            read_file_location = read_file_location.decode()
            split_file_location = read_file_location.split("\n")
            if(len(split_file_location) >1):
                print("[##] Multuple Locations found, Please Specify with number selection")
                counter = 0
                for each in split_file_location:
                    
                    print("OPTION " , counter , " : " ,each)
                    counter +=1
                selection = int(input("[>]:"))
                if(selection > len(split_file_location)):
                    print("[ERR] INVALID SELECTION. EXITING!")
                    exit(0)
                else:
                    user_file_to_link = split_file_location[selection]
            else:
                user_file_to_link = split_file_location[0]
        print("[##] File Path Selected: ", user_file_to_link)
        create_link(user_file_to_link)
        list_links()
main()