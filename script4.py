import sys
from geoip import geolite2
import socket
import csv
from datetime import date
FINAL_IP_OBJS = []

class ip_connection:
    def __init__(self,ip,ports):
        self.ports = ports
        self.ip = ip;
        self.count = 1
        self.country = ""
        self.timezone = ""
        self.users = []
    def printIPC(self):
        print("[##: Print Connection Details]:",end=" ")
        s1 = f"(<-->) CONNECTION [{self.ip}] "
        s2 = f"     : count = {self.count}"
        s3 = "     : usernames attempted ="
        s4 = f"     : location = {self.country}, timezone = {self.timezone}"
        if(len(self.ports) > 20):
            s5 = f"     : ports accessed (#) = {len(self.ports)}       # Ports heald in data structure, too large to display"
        else:
            s5 = f"     : ports accessed (#) = {self.ports}"      
        print(s1)
        print(s2)
        print(s3,end='')
        print("   | (In DB): ",end='')
        for each in self.users:
            if '+' in each:
                print(each,end='')
        print("    | (Not in DB): ",end='')
        for each2 in self.users:
            if '-' in each2:
                print(each2,end='')
        print("")
        print(s4)
        print(s5)


def check_if_ip_in_final_obj_list(ip):
    flag = -1
    counter = 0
    for each in FINAL_IP_OBJS:
        if(each.ip == ip):
            flag = counter
        counter +=1
    return flag

def filter_list_to_obj(in_array):

    for each in in_array:
        ports = {}
        each = each.split("for")
        if("Failed password" in each[0]):
            split_info = each[1].split(" ")
            if(split_info[2] == "from"):
               
                ip_exsists = check_if_ip_in_final_obj_list(split_info[3])
                if(ip_exsists == -1):
                    ip = split_info[3]
                    ports = [split_info[5]]
                    user = f" [| + |]:{split_info[1]} "
                    users = [user]
                    new_connection = ip_connection(ip,ports)
                    new_connection.users = users
                    match = geolite2.lookup(ip)
                    if match is not None:
                        new_connection.country = match.country
                        new_connection.timezone = match.timezone
                    FINAL_IP_OBJS.append(new_connection)
                else:
                    port = split_info[5]
                    user = f" [| + |]:{split_info[1]}"

                    FINAL_IP_OBJS[ip_exsists].users.append(user)
                    FINAL_IP_OBJS[ip_exsists].ports.append(port)
                    FINAL_IP_OBJS[ip_exsists].count +=1
                    #FINAL_IP_OBJS[ip_exsists].printIPC()
            else:
                # different string
                ip_exsists = check_if_ip_in_final_obj_list(split_info[5])
                if(ip_exsists == -1):
                    ip = split_info[5]
                    try:
                        socket.inet_aton(ip)
                    except socket.error:
                        print("[ERR : Filter List to obj] invalid ip got from entry: ",ip, "  [SETTING IP TO NULL]")
                        ip= '0.0.0.0'
                    ports = [split_info[7]]
                    user = f" [| - |]:{split_info[3]}"
                    users = [user]
                    new_connection = ip_connection(ip,ports)
                    new_connection.users = users
                    match = geolite2.lookup(ip)
                    if match is not None:
                        new_connection.country = match.country
                        new_connection.timezone = match.timezone
                    FINAL_IP_OBJS.append(new_connection)
                else:
                    port = split_info[7]
                    user = f" [| - |]:{split_info[3]}"

                    FINAL_IP_OBJS[ip_exsists].users.append(user)
                    FINAL_IP_OBJS[ip_exsists].ports.append(port)
                    FINAL_IP_OBJS[ip_exsists].count +=1
                    #FINAL_IP_OBJS[ip_exsists].printIPC()

    for each in FINAL_IP_OBJS:
        each.users = list(set(each.users))
        each.ports = list(set(each.ports))
                
        

def main():
    ## main function to call helpers to parse for object
    if(len(sys.argv) < 2):
        print("[ERR:main]--Please provide a target csv list to search--length given for args=",len(sys.argv)," expected 2+")
        exit(0)
    ports = {"22","44"}
    ip1 = ip_connection("192.168.1.1",ports)
    print("[...:main] Opening CSV...")
    try:
        with open(sys.argv[1],'r') as f:
            rows = f.read().split('\n')
        rows_with_failure = [row for row in rows if 'Failed' in row]
    

    except Exception as e:
        print("[!!!:ERR] Error with opening csv:",e)

    filter_list_to_obj(rows_with_failure)
    FINAL_IP_OBJS.sort(key=lambda x: x.count, reverse=True)
    print("_________________________________________________________________________________________")
    print("[##] Final Connections (only showing those with 10+ count):")
    print("[###] Note: usernames with a + indicate the user account exsists, those with - indicate they do not")
    print("[###] Note: some ports will not show due to large list size, rather size will be printed")
    #only print if larger than 10 failed attempts
    for each in FINAL_IP_OBJS:
        if(each.count > 10):
            each.printIPC()
    print("____________________________________________________________________________")
    print("")
    print("[ -- outputting to csv named out<date>.csv -- ]")
    today = date.today()
    the_date = today.strftime("%b-%d-%Y")
    filename = "output" + the_date + ".csv"
    with open(filename,mode='w+') as csv_file:
        line_writer = csv.writer(csv_file,delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
        line_writer.writerow(["______________________",the_date,'_______________________________'])
        line_writer.writerow(["(key):","count","ip","country","timezone"])
        
        for each in FINAL_IP_OBJS:
            line_writer.writerow([each.count,each.ip,each.country,each.timezone])

main()
