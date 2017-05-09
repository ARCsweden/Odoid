#!/usr/bin/env python3
import subprocess
import simplejson as json
Odroid_mac_scan=[]
Odroid_usres=[]
Odroid_nrUsers=0

def remove_element(list_,index_):
    clipboard = []
    for i in range(len(list_)):
        if i is not index_:
            clipboard.append(list_[i])
    return clipboard


def scanElementToList():
    command = 'sudo arp-scan -I enp0s25 -l | grep WIBRAIN'
    #command = 'sudo arp-scan -I wlp1s0 -l | grep Unknown'
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    rows = output.stdout.split("\n")
    counter = 0
    for i in rows:
        #print(str(counter) + " '" + i + "'")
        counter += 1
        r = i.split("\t")
        if len(r) > 1:
            #print(r)
            row = []
            row.append(r[0])
            row.append(r[1])
            row.append(r[2])
            #print(row)
            Odroid_mac_scan.append(row)
    #for i in Odroid_mac_scan:
        #print(i)

def printOdroidList():
    '''This function saves the list to disk'''
    print("Start saveOdroidList")
    print(json.dumps(Odroid_mac_scan, sort_keys=True, indent=4 * ' '))

def print_conections():
    '''Prints the connectino between odroid and user'''
    print("Start printing list\n")
    for u in Odroid_usres:
        for o in Odroid_mac_scan:
            if(u[1] == o[1]):
                print(u[0] + "\t" + o[1] + "\t" + o[0])
    print("End of list")

def user_print():
    '''Prints the userd data base'''
    print(" ")
    print("Nr of users is " + str(Odroid_nrUsers))
    print("-------List users----------")
    print("ID  \tUser    \t\tMAC")
    nr = 0
    for i in Odroid_usres:
#        print(str(nr) +"  \t"+ U: +  " + i[0] + "\tM: " + i[1]")
        print(str(nr) + " \t" + i[0] + "\t\t" + i[1] )
        nr += 1
    print("\n\n")


def write_readme():
    '''Writes the names and ip to REDME.md '''
    fp = open("README.md" , "w")
    fp.write("#Odroid\nHere are the Odroid ip and owners\n")
    for u in Odroid_usres:
        for o in Odroid_mac_scan:
            if(u[1] == o[1]):
                fp.write(" * " + u[0] + "\t" + "\t" + o[0] + "\n")
    fp.close()

def user_add(Name):
    '''Adds a user to Odroid_usres stack'''
    global Odroid_nrUsers
    user = []
    user.append(Name)
    user.append('[NAT]')
    Odroid_usres.append(user)
    Odroid_nrUsers += 1

def user_config():
    '''The configuration for a user that is going to be stored in the user dat file'''
    global Odroid_nrUsers
    print("What do you want to do?")
    print("1 List users in configfile")
    print("2 Add user to file")
    print("3 Remove user")
    print("0 Return to main")
    choise = int(input("Enter option >>>>  "))
    if choise == 1:
        print("Users in list is")
        user_print()
    elif choise == 2:
        user=[]
        user.append(input("Enter name= "))
        user.append('NOT')
        Odroid_usres.append(user)
        Odroid_nrUsers = Odroid_nrUsers + 1
    elif choise == 3:
        user_print()
        print("Remove by id")
        removeID = int(input("Enter ID to be romeved form list: "))
        if(removeID >= 0 and removeID <= Odroid_nrUsers):
            del Odroid_usres[removeID]
        write_user_to_file()
        #remove_element(Odroid_usres, removeID)
        #Odroid_usres.pop(input("Enter id to remove: "))

def user_atatch():
    '''Atatch a user to a odroid MAC addres'''
    print("\nSelect an Odroid to pair with user\n")
    temp = []
    if(len(Odroid_mac_scan) == 0):
        print("No Odroids in the list run scanner first")
        return 0;
    for u in Odroid_usres:
        for o in Odroid_mac_scan:
            if(u[1] != o[1]):
                temp.append(str(o[1]))
    count = 0
    print("Pleace select one of the folowing odroid cards")
    print("ID\t\tMAC")
    for od in temp:
        print(str(count) + "\t" + str(od))
        count += 1
    mac = int(input("Select odroid [-1] to exit: "))
    if (mac== -1):
        return -1;
    if(mac >= 0 and mac <= count):
        print("Select user")
        user_print()
        use = int(input("Select user [-1] to exit: "))
        if(use >= 0 and use <= Odroid_nrUsers):
            print("Adding " + str(temp[mac]) + " to " + str(Odroid_usres[use][0]))
            Odroid_usres[use][1]=str(temp[mac])
            write_user_to_file()
        else:
            print("-- Exit user achatch --")
            return -1
def file_operations():
    print("1 save users.dat")
    print("2 read users.dat")
    print("3 save README.md")
    print("4 Clear README.md")
    print("5 EXIT")
    ch = int(input("Select operation"))
    if (ch == 1):
        write_user_to_file()
    elif (ch == 2):
        read_usr_from_file()
    elif (ch == 3):
        write_readme()
    elif (ch == 4):
        print("Clears the READMD.me file")
        fp = open("README.md", "w")
        fp.write("#Odrid\nNo project is going on now")
        fp.close()
    else:
        print("exti")
        return 0

def menu():
    running = True
    while running:
        print("1 scan conected odroids")
        print("2 Shaw result of scan")
        print("3 List users")
        print("4 Config user")
        print("5 Atach Odroid ot user")
        print("6 Show IP config for all OdroidS")
        print("9 FileOperations")
        print("0 EXIT")
        choise = int(input("Enter option $$ "))
        if choise == 1:
            scanElementToList()
        elif choise == 2:
            printOdroidList()
        elif choise == 3:
            user_print()
        elif choise == 4:
            user_config()
        elif choise == 5:
            print("Atach user to Odroid")
            user_atatch()
        elif choise == 6:
            print_conections()
        elif choise == 9:
            file_operations()
        elif choise == 0:
            running = False
            write_readme()
        else:
            print("No choise enterd")

def read_usr_from_file():
    '''Read ds the user data form file'''
    global Odroid_usres
    global Odroid_nrUsers
    fp = open("users.dat" ,"r")
    text = fp.read()
    #print(json.loads(text))
    Odroid_usres = json.loads(text)
    print("nr of users on disk " + str(len(Odroid_usres)) + "st")

    Odroid_nrUsers = len(Odroid_usres) - 1
    fp.close()

def write_user_to_file():
    '''Writes the user data to file'''
    fp = open("users.dat" ,"w")
    fp.write(json.dumps(Odroid_usres))

def main():
    print("Odroid scanner by Magnus Sörensen")
    #user_add("Hampus")
    #user_add("Magnus")
    #user_add("Marie")
    #write_user_to_file()
    read_usr_from_file()
    menu()
    #scanElementToList()
    #printOdroidList()
    #print(json.dumps(Odroid_mac_scan[0][1], sort_keys=True, indent=4*''))



if __name__ == '__main__':
    main()
