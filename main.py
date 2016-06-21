from builtins import print
import csv
import classes
import datetime
import sys ,os,numpy.random as R
numofhotels = 0
import random
import time
import codecs

hotels = [] #List containing all the hotels
hotelid = []
trietree = classes.Trie()
rbtree = classes.rbtree()
savefile = "outdata.csv"
loadfile = "data.csv"


def ordered():
    hotels.sort(key=lambda x: x.id, reverse=True)
   # for it in range(1, len(hotels)):
        #if hotels[it].id < hotels[it1].id:
           # print("NOOOOOPPP")--
    return


def load_csv():
    hotels = []
    surnames = []
    global numofhotels
    ##with open('data.csv', newline="\n",encoding="ISO-8859-1") as csvfile:
    csv_file = csv.reader(open(loadfile, newline="\n",encoding="ISO-8859-1"),delimiter=";") #Opening the csv
    row = next(csv_file) #Getting the first line
    numofhotels = int(row[0])  #Getting the number of hotels //MUST UPDATE WHEN THEY ADD ONE HOTEL
    print(numofhotels)  #Testing
    it = 0
    count = 0 #Counter
    for row in csv_file: #For each hotel
        hotels.append(classes.hotel(str(it),row[1],row[2],row[3],row[0])) #Filling the info about the hotel1
        hotelid.append(it)
        it += 1

        for i in range(4,int((len(row))),3): #Iterating through the reservations
            hotels[count].fillres(row[i],row[i+1],row[i+2],hotels[count].name) #Filling the reservations for each hotel
            #hotels[count].showres()
            surnames.append(row[i])


        count += 1
    ordered()

    trietree = classes.make_trie(hotels)

    print("Creating the Red Black Tree...")

    classes.test_tree(rbtree, hotelid)
    print("Tree creation and assertion complete...")

    return hotels ,surnames,trietree

def save_csv():
    global numofhotels
   # writer = open("outdata.csv", "w",encoding="utf-8",errors='replace')
    writer = codecs.open("outdata.csv", "w", "utf-8")

    row = str(numofhotels) + ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;"
    writer.write(row)
    writer.close()
    writer = open("outdata.csv", "a")
    if 'hotels' in globals() :
        for it in range(0, len(hotels)):
            writer.write("\n")
            line = str(hotels[it].id) + ";" + hotels[it].name + ";" + hotels[it].stars + ";" + hotels[it].nofrooms
            #line = line.decode('unicode-escape')
            for j in range (0,len(hotels[it].reservations)):
                line = line + ";" + hotels[it].reservations[j].name + ";" + hotels[it].reservations[j].checkindate + ";" + hotels[it].reservations[j].staydays

            print (line)
            writer.write(line)

    else :
        print("Database is not loaded")



    #writer.writerows([row])
    return

def add_hotel():
    if hotels:
        print("No hotels loaded")
        id = str(int(hotels[-1].id) + 1)
    else:
        id = 1

    global checkin, numofhotels
    print ("=========== Insert a Hotel============\n")


    #print(id)
    name = input ("Please input the name:  ")
    stars = input("Please input the stars of the hotel: ")
    noofrooms = input("Please input the number of rooms: ")
    hotels.append(classes.hotel(id, name, stars, noofrooms,id))
    hotelid.append(id)
    flag = 0
    numofhotels += 1
    #print(numofhotels)
    while flag == 0 : #Reservations
        print("=========== Insert a Reservation============\n")
        name = input("Please input the name: ")

        while 1: #Date

            checkin = input("Please input the date of the checkin (DD/MM/YYYY): ")
            try:
                datetime.datetime.strptime(checkin, '%d/%m/%Y')
                break
            except ValueError:
                print("Incorrect data format, should be DD/MM/YYYY")

        staydays = input("Please input the desired days: ")

        #Adding the hotel to the list
        hotels[-1].fillres(name,checkin,staydays,hotels[-1].name)

        #Adding the hotel to the Trie tree
        reserv = hotels[-1].reservations[-1]
        surname = hotels[-1].reservations[-1].name
        trietree.insert(surname, reserv)
        #-----------------------------------
        #Adding the hotel to the rb tree
        rbtree.insert_key(int(id))

        while 1:
            anw = input("Do you want to insert another Reservation?(Y/N) ")
            if  anw == "Y" :
                print( "Continue")
                break
            elif anw == "N":
                flag = 1
                break
            else:
                print("Please input Y or N")



    return

def printhotel(it): #Printing a hotel
    print("======Hotel Found======")
    print("Name:   "+ hotels[it].name)
    print("Stars:             " + hotels[it].stars + "*")
    print("Number of rooms:   " + hotels[it].nofrooms)

    return

def s_and_d(id,prt): #Metalica
    calcs = 0
    if id < 1 or id > int(hotels[-1].id) :
        return 0
    for it in range(1,len(hotels)):
        #print(hotels[it].id)
        calcs += 1
        if id == int(hotels[it].id):
            if prt:
                printhotel(it)
            return 1 , calcs

    return -1,calcs

def sursearch(sname,prt):
    first = 1
    calcs = 0
    for it in range(0, len(hotels)):
        for j in range(0, len(hotels[it].reservations)):
            calcs += 1
            if sname == hotels[it].reservations[j].name and prt:
                if first == 1:
                    print("=======Reservations Found:=======")
                    print("For Mr/Ms : " + sname + " :")
                    print("/===================================")
                    first = 0
                print("|  Hotel : " + hotels[it].name)
                print("|  Check in Date : "+ hotels[it].reservations[j].checkindate)
                print("|  Days to stay : " + hotels[it].reservations[j].staydays)
                print("|===================================")
    return calcs


    return

#Stars search
def starsearch(strs):
    count = 0
    calcs = 0
    for it in range(0, len(hotels)):
        calcs += 1
        if  hotels[it].stars == strs:
            if count == 0 :
                print ("========= ",strs," Star Hotels Found=========")
            count += 1
            print ("No "+ str(count) + ": " + hotels[it].name)
            #print ("No of Reservations : " + str(len(hotels[it].reservations)))
            print("Number of Reservations: " ,hotels[it].rescount)


    return calcs

#Reservations Search
def reservsearch(res,hotels):
    count = 0
    for it in range(0,len(hotels)):
        if hotels[it].numofres() == int(res):
            if count == 0:
                print ("=========Hotels Found=========")
            count +=1
            print ("No " + str(count) + ": " + hotels[it].name)
            print ("Stars : " + str(hotels[it].stars) + "\n")
    if count == 0:
        print("No hotels found with this amount of reservations...\n")

    return

def binarySearch(hotelist,id,prt,calcs):

    if len(hotelist) == 0: #If there is no hotel
        return False
    else:
        mid = len(hotelist)//2 #Calculating mid

        if int(hotelist[mid].id) == id:
            calcs+=1
            if prt:
                printhotel(id)
            return calcs
        else:
            if id < int(hotelist[mid].id):
                calcs += 1
                return binarySearch(hotelist[:mid],id,prt,calcs)
            else:

                return binarySearch(hotelist[mid+1:],id,prt,calcs)

def interS(hotelist,id,prt):
    low = 0
    high = len(hotelist)-1
    calcs = 0

    while hotelist[low].id <= id and hotelist[high].id >= id:
        mid = int((low + ((id - hotelist[low].id) * (high - low))
               / (hotelist[high].id - hotelist[low].id)))
        calcs += 1
        if hotelist[mid].id < id:
            low = mid + 1
            calcs += 1
        elif hotelist[mid].id > id:
            high = mid - 1
            calcs += 1
        elif hotelist[mid].id == id:
            if prt:
                printhotel(mid)
            return calcs
        else:
            if prt:
                print("Hotel not found")
            return calcs


    return calcs

def print_results(name,length,microsec,totalcalcs):

    print ("| ", microsec, " Microseconds for ",name," search of 1000 ids")
    print ("| ", microsec / length, " Microseconds median time per search")
    print ("|  Calculations : ", totalcalcs / length, " per search")
    print("--------------------------------------\n")



    return


#Main menu
def menu():
    print("1. Load Hotels and Reservations from file\n"
          "2. Save Hotels and Reservations to file\n"
          "3. Add a Hotel\n"
          "4. Search and Display a Hotel by id\n"
          "5. Display all Hotels of specific stars category and number of reservations\n"
          "6. Display Reservations by surname search\n"
          "7. Interpolation / Binary Search by id\n"
          "8. Red Black Trees search by id\n"
          "9. Digital Tries search by surname\n"
          "10. Τime and calculation test. \n"
          "0. Exit")
    return int(input('Option : '))

#ahotel = classes.hotel(1,'one',4,100)

loop = 1
choice = 0
#Checking the choice
while loop == 1:
    choice = menu() #Calling the menu

    if choice == 1:    #Done
        hotels,surnames,trietree = load_csv()
    elif choice == 2:  #Done
        save_csv()

    elif choice == 3:  #Done
        add_hotel()

    elif choice == 4:  #Done
        #promting for id
        id = int(input("Pleade input a Hotel id between 1 and " +str(hotels[-1].id) + " to search: "))
        f,calcs = s_and_d(id,1)
        while 1:
            if f == 0:
                id = int(input("Please input an id between 1 and " +  hotels[-1].id +": "))
                f,calcs = int(s_and_d(id,1))
            elif f == -1:
                print("The hotel was not found...")
                break
            else :
                break

    elif choice == 5: #Done

        out = 1
        while out:
            pik = int(input("Press 1 for Stars search or 2 for Reservations search\n"))
            if pik == 1 or pik == 2:
                out = 0
            else:
                print("Incorect input... please choose 1 or 2\n")

        if pik ==1:
            loop1 = 1
            stars = 0
            while loop1 == 1:
                stars = input("Please input the number of stars(1 to 5): ")
                if int(stars) < 1 or int(stars) > 5:
                    print("Incorect entry...\n")
                else:
                    loop1 = 0
            calcs = starsearch(stars)
        else:
            loop2 = 1
            reserv = 0
            while loop2 == 1:
                reserv = int(input("Please input the number of reservations :\n"))
                if int(reserv) <= 0 :
                    print("Please input a positive number...\n")
                else:
                    loop2 = 0
            reservsearch(reserv,hotels)

    elif choice == 6: #Done

        sur = input("Please input a surname to search: ")
        cacls = sursearch(sur,1)
    elif choice == 7:
        print("Please input a id to search: ")
        id = int(input())
        print("Binary search result: \n")
        calcs = binarySearch(hotels, id,1,0)
        print("Interpolation search result: \n")
        calcs = interS(hotels, id,1)
    elif choice == 8: #RB tree

        loopi = 1
        while loopi:

            print("Please Enter a hotel id between ",hotelid[0]," and ",hotelid[-1])
            id = int(input())
            if id < hotelid[0] or id > hotelid[-1]:
                print("Please input a correct id")
            else:

                result,calcs = rbtree.search(id,0)
                print("Id : " ,result.key, " found!")
                printhotel(result.key)

                oopi = 1
                while oopi:
                    answ = input("Would you like to search for another one? (Y/N)")
                    if answ == "N" :
                        loopi = 0
                        oopi = 0
                    elif answ =="Y":
                        print("Doing another one")
                        oopi = 0
                    else:
                        print("Please input Y or N")

    elif choice == 9: #Trie

        if trietree:
            print("======Trie implementation surname search======\n")
            sur = input("Please input a surname to search: ")
            answ = trietree.search(str(sur),1)
            print(trietree.calcs)

        else:
            print("No trie...Plz load a csv")


    elif choice == 10: #Testing and calculating time and calculations per search

        if hotels: #If there is a loaded database
            print("Comencing time and calculation test\n")
            #Making random id's and surnames
            rids = random.sample(range(1,int(hotels[-1].id)),1000)
            rsur = random.sample(range(0, len(surnames)), 1000)
            test = 0
            total = 0
            #Running the tests=========================================================
            print("Testing Linear search in id and surnames")
            print("_________________________________________")
            if surnames:
                a = datetime.datetime.now()
                for it in range (0,len(rids)):
                    f,calcs = s_and_d(rids[it],0)

                    total += calcs
                b = datetime.datetime.now()
                c = b - a
                print ("/IDs ")
                # printing the results for the test
                print_results("Linear", len(rids), c.microseconds, total)

                total = 0
                a = datetime.datetime.now()
                for it in range (0,len(rsur)):
                    calcs = sursearch(surnames[rsur[it]],0)
                    total += calcs
                b = datetime.datetime.now()
                c = b - a
                print ("/Surnames")
                # printing the results for the test
                print_results("Linear", len(rsur), c.microseconds, total)

            else:
                print("No surnames loaded")

            print("Testing Binary search in id")
            print("_________________________________________")
            total = 0
            a = datetime.datetime.now()
            for it in range(0, len(rids)):
                calcs = binarySearch(hotels,rids[it], 0,0)
                total += calcs

            b = datetime.datetime.now()
            c = b - a
            # printing the results for the test
            print_results("Binary",len(rids),c.microseconds,total)


            print("Testing Interpolation search in id")
            print("_________________________________________")
            total = 0
            a = datetime.datetime.now()
            for it in range(0, len(rids)):
                calcs = interS(hotels, rids[it], 0)
                total += calcs
                #print(total)

            b = datetime.datetime.now()
            c = b - a
            # printing the results for the test
            print_results("Interpolation",len(rsur),c.microseconds,total)


            print("Testing Rb tree  search in id ")
            print("_________________________________________")
            total = 0
            a = datetime.datetime.now()
            for it in range(0, len(rids)):
                calcs = 0

                x,calcs = rbtree.search(int(rids[it]),calcs)

                total += calcs
            b = datetime.datetime.now()
            c = b - a

            # printing the results for the test
            print_results("RB Tree",len(rids),c.microseconds,total)
            #------------------------------------------------------
            #Meros A epilogi 5
            print("Testing Linear surname tree  search in id ")
            print("_________________________________________")
            rstars = [random.randint(0,5) for r in range(0,1000)]
            total = 0
            a = datetime.datetime.now()
            for it in range(0,len(rstars)):
                calcs = 0
                calcs = starsearch(rstars[it])
                total += calcs
            b = datetime.datetime.now()
            c = b - a
            print_results("Linear Surname",len(rstars),c.microseconds,total)




            print("Testing  Trie tree search in surname")
            print("_________________________________________")
            total = 0
            a = datetime.datetime.now()
            for it in range(0, len(rsur)):

                answ = trietree.search(surnames[rsur[it]],0)
                total += trietree.calcs
            b = datetime.datetime.now()
            c = b - a

            # printing the results for the test
            print_results("Trie Tree",len(rsur),c.microseconds,total)

        else: #If no hotels are loaded
            print("No hotels loaded   ")

    elif choice == 0: #Exiting the program
        print("Exiting...")
        loop = 0





