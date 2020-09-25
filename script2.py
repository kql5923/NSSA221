import os
import sys
import subprocess
try:
    import pandas as pd
    print("[MAIN] pandas installed")
except ModuleNotFoundError:
    print("[MAIN] FAILED DUE TO PANDAS PACKAGE MISSING! Beginning install of PANDAS!")
    os.system("sudo apt-get install python3-pandas")
import grp

ALL_USERS = []
class User:
    def __init__(self,id,lastname,firstname, office,phone,department,group):
        self.eid = id
        self.lastname = lastname
        self.firstname = firstname
        self.office = office
        self.phone = phone
        self.department = department
        self.group = group
        self.username = ""
        self.password = ""
    def get_formatted_useradd(self):
        homelocation = ''
        shell = ''
        department = self.department
        fname = self.firstname
        lname = self.lastname
        uname = self.username
        homelocation = '%s/%s' %(self.department,self.username)
        if(self.group == "office"):
            shell = 'csh'
        else:
            shell = 'bash'
        
        useradd_string = 'useradd -m -d /home/%s -s /bin/%s -g %s -c "%s %s" %s' %(homelocation,shell,department,fname,lname,uname)
        return useradd_string
    def get_formatted_passwdStdin(self):
        psswdstdinString = 'passwd --stdin %s' %(self.password)
        return psswdstdinString
    def get_formatted_passwdExp(self):
        psswdexpString = 'passwd -e %s' %(self.password)
        return psswdexpString

def run_command(cmd):
    proc = subprocess.Popen(cmd,shell = True, stdin = subprocess.PIPE,stdout=subprocess.PIPE)
    out,err = proc.communicate()
    print("[RunCommand : OUTPUT]:",out)
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
def in_list_already(list,uname):
    for each in list:
        if(each == None):
            return False
        elif(each.username == uname):
            return True
    return False


def valid_user(user):
    if(user.eid == "nan" or user.eid == " nan" or user.eid == "nan " or user.eid == " nan " or is_int(user.eid) == False):
        print("[Valid User Check] BAD USER [eid] FOR EID = ",user.eid)
        return False
    if(user.firstname == "nan" or user.firstname == " nan" or user.firstname == "nan " or user.firstname == " nan "):
        print("[Valid User Check] BAD USER [firstname] FOR EID = ",user.eid)
        return False
    if(user.lastname == "nan" or user.lastname == " nan" or user.lastname == "nan " or user.lastname == " nan "):
        print("[Valid User Check] BAD USER [lastname] FOR EID = ",user.eid)
        return False
    if(user.department == "nan" or user.department == " nan" or user.department == "nan " or user.department == " nan "):
        print("[Valid User Check] BAD USER [department] FOR EID = ",user.eid)
        return False
    if(user.group == "nan" or user.group == " nan" or user.group == "nan " or user.group == " nan "):
        print("[Valid User Check] BAD USER [group] FOR EID = ",user.eid)
        return False

def print_user_objs(list):
    for each in list:
        print("[user obj] -----------------------------------------------")
        print("USERID =",each.eid,end=' | ')
        print("Lastname =",each.lastname,end=' | ')
        print("Fristname =",each.firstname,end=' | ')
        print("Office =",each.office,end =' | ')
        print("Phone =",each.phone,end = ' | ')
        print("Department =",each.department,end=' | ')
        print("Group =",each.group,end= ' | ')
        print("Username =",each.username,end = ' | ')
        print("Generated pass (will expire) =",each.password, end = ' |\n')
        
        
def parse_users_file(userfile):
    parsed_user_objects = []
    users_csv_file = pd.read_csv(userfile)
    print("[User File Parser] File Contents:")
    print(users_csv_file)
    print("[User File Parser] creating user objects...")
    for i,j in users_csv_file.iterrows():
        print("[User File Parser] creating user ",i)
        uid = ""
        lname = ""
        fname = ""
        office = ""
        phone = ""
        dept = ""
        group = ""
        uname = ""
        for index,val in j.iteritems():
            if(index == "EmployeeID"):
                uid = str(val)
            elif(index == "LastName"):
                lname = str(val)
            elif(index == "FirstName"):
                fname = str(val)
            elif(index == "Office"):
                office = str(val)
            elif(index == "Phone"):
                phone = str(val)
            elif(index == "Department"):
                dept = str(val)
            elif(index == "Group"):
                group = str(val)
        uname = fname[0] + lname
        while(in_list_already(parsed_user_objects, uname) == True):
            uname = uname + "1"
        newuser = User(uid,lname,fname,office,phone,dept,group)
        newuser.username = uname
        newuser.password = uname
        parsed_user_objects.append(newuser)
    counter = 0
    flagged_user_objs = []
    for each in parsed_user_objects:
        res = valid_user(each)
        if(res == False):
            flagged_user_objs.append(each)
    completed_parse = [item for item in parsed_user_objects if item not in flagged_user_objs]

    
    return completed_parse

def main():
    infile = str(input("Input File (press enter for default)>"))
    if(infile == ""):
        infile = 'Lab02_Users.csv'
    users = parse_users_file(infile)
    print("\n")
    print("==============================================================")
    print("[main] user objects created:")
    print_user_objs(users)
    print("==============================================================")

    for each in users:
        try:
            grp.getgrnam(each.department)
        except KeyError:
            addGroup_cmd = 'groupadd -f %s' %(each.department)
            #run_command(addGroup_cmd)
            print(addGroup_cmd)
        # run_command(each.get_formatted_useradd())
        # run_command(each.get_formatted_passwdStdin())
        # run_command(each.get_formatted_passwdExp())
        print(each.get_formatted_useradd())
        print(each.get_formatted_passwdStdin())
        print(each.get_formatted_passwdExp())
    
    
main()