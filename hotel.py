# Hotel Reservation System
# This program allows users to:
# Sign up and log in
# Search rooms by different filters
# Reserve and cancel rooms
# Manage wallet balance
# Data is stored using pickle files.

import datetime
import pickle

class User:
    def __init__(self, username,password , name , balance=200):
        self.__username = username
        self.__password = password
        self.__name = name
        self.__balance = balance

    # Verify username and password during login
    def check_login(self , username , password):
        if(self.__username == username):
            if(self.__password == password):
                return 1
            else:
                return 2
        return 0
    
    #check username
    def check_username(self , username): 
        if(self.__username == username):
            return True
        return False
    def get_balance(self):
        return self.__balance
    
    # Check if the balance is greater than the price
    def can_pay(self , price):
        if price > self.__balance :
            return False
        return True    
    
    # Reduce the balance
    def pay(self , price):
        if price > self.__balance :
            return False
        self.__balance-=price
        print(f"you pay {price} $")
        print(f"new balance : {self.__balance}")
        return True    
    
    # Increase balance
    def deposite(self , money):
        self.__balance += money
        print(f"your balance increased {money}$")
        print(f"new balance : {self.__balance}")
        
class Room:
    def __init__(self, room_number,capacity , price , facilities = None , reserved = None):
        self.__room_number = room_number
        self.__capacity = capacity
        self.__price = price
        
        if reserved is None:
            self.__reserved = []
        else:
            self.__reserved = reserved
        if facilities is None:
            self.__facilities = []
        else:
            self.__facilities = facilities
    
    # facilities in this room
    def check_facilities(self, facilities):
        for i in facilities:
            if self.__facilities.count(i) == 0:
                return False
        return True
    def check_can_reserve(self , dates):
        reserve_dates = []
        for date in dates:
            if(self.__reserved.count(date) > 0):
                reserve_dates.append(date)
        return reserve_dates
    
    def check_reserve_capacity(self , numbers):
        if(self.__capacity >= numbers or self.__capacity==3):
            return True
        return False
    def can_pay(self , balance,dates):
        if balance >= self.__price*len(dates):
            return True
        return False
    
    # Attempt to reserve the room for given dates and number of people
    def reserve_room(self , balance , dates , numbers): 
        if self.can_pay(balance , dates):
            if(self.check_reserve_capacity(numbers)):
                check_result=self.check_can_reserve(dates)
                if len(check_result) == 0:
                    self.__reserved.extend(dates)
                    print("reserve completed")
                    return True
                else:
                    print("--------------------------------------------------")
                    print("this room is reserved by other users in this days")
                    for date in check_result:
                        print(date)
                    print("--------------------------------------------------")
                    return False
            else:
                print("numbers more than capacity")
                return False
        else:
            print("not enough")
            return False
    
    def check_price(self , min_price, max_price):
        if self.__price >= min_price and self.__price <= max_price:
            return True
        return False
    def get_capacity(self):
        return self.__capacity
    def get_room_number(self):
        return self.__room_number
    def show_info(self):
        print("---------------")
        print(f"room number:{self.__room_number}\nroom type: " , end="")
        if self.__capacity == 3:
            print("suite")
        else:
            print(f"{self.__capacity} bed")
        print(f"room price: {self.__price}") 
        print("---------------")
    def get_price(self):
        return self.__price
    
    # Cancel the reservation
    def cancel_reserve(self , dates): 
        for date in dates:
            self.__reserved.remove(date)
class Reserve:
    def __init__(self , username , room_number , first_date , last_date , number , price , reservation_number , status="active" ):
            self.__username=username
            self.__room_number=room_number
            self.__first_date=first_date
            self.__last_date=last_date
            self.__number=number
            self.__total_price= price
            self.__status=status
            self.__reservation_number=reservation_number
    def cancel_reserve(self):
        if self.__status=="active":
            self.__status="canceled"
            today = datetime.date.today()
            if (self.__first_date - today).days >= 2:
                return True
            return False
    def check_reservation_number(self , reservation_number ):
        return self.__reservation_number == reservation_number
    
    def get_price( self ):
        return self.__total_price
    def get_room_number( self ):
        return self.__room_number
    def get_dates( self ):
        dates = []
        for i in range((self.__last_date-self.__first_date).days + 1):
            dates.append((self.__first_date + datetime.timedelta(i)))
        return dates
    def check_username( self  , username ):
        return self.__username == username
            
    def complite_reserve(self):
        if self.__status=="active":
            if datetime.date.today() > self.__first_date:
                self.__status="complite"
                return True
        return False
    def show_info(self , username , filter = ""):
        if(filter == "active"):
            if(self.__username==username and self.__status=="active"):
                print("-----------------------------------")
                print(f"reservation number : {self.__reservation_number}\nusername:{self.__username}\nroom number:{self.__room_number}\nfirst date: {self.__first_date}\nlast date: {self.__last_date}\nnumber of people:{self.__number}\ntotal price:{self.__total_price}\nstatus:{self.__status}")
                return True
        else:
            if(self.__username==username):
                print("-----------------------------------")
                print(f"reservation number : {self.__reservation_number}\nusername:{self.__username}\nroom number:{self.__room_number}\nfirst date: {self.__first_date}\nlast date: {self.__last_date}\nnumber of people:{self.__number}\ntotal price:{self.__total_price}\nstatus:{self.__status}")
                return True

# Filter rooms based on selected room type
def search_by_type(room_list): 
    rooms = []
    while True:
        rooms.clear()
        room_type=input("1: one bed\n2: two bed\n3: suite\nback: any other key\nselect: ")
        if room_type=="1":
            for room in room_list:
                if room.get_capacity()==1:
                    rooms.append(room)
        elif room_type=="2":
            for room in room_list:
                if room.get_capacity()==2:
                    rooms.append(room)
        elif room_type=="3":
            for room in room_list:
                if room.get_capacity()==3:
                    rooms.append(room)
                    
        return rooms

# Return available rooms within selected date range
def search_by_date(room_list):  
    rooms = []
    dates=[]
    while True:
        try:
            first_date = datetime.date.fromisoformat(input("date must be YYYY-MM-DD\nstart date : "))
            if(first_date >= datetime.date.today()):
                break
            else:
                print("start date must be after today")
        except:
            print("start date is not valid")

    while True:
        dates = []
        try:
            last_date = datetime.date.fromisoformat(input("date must be YYYY-MM-DD\nlast date : "))
            if not last_date >= datetime.date.today():
                print("last date must be after today")
                continue
            if not last_date>=first_date:
                print("last date must be after first date")
                continue
                
        except:
            print("last date is not valid")
        for i in range((last_date-first_date).days + 1):
            dates.append((first_date + datetime.timedelta(i)))
        break
    for room in room_list:
        check_result = room.check_can_reserve(dates)
        if len(check_result) == 0:
            rooms.append(room)
    return rooms
            
# Filter rooms within a given price range
def search_by_price(room_list): 

    rooms = []
    min_price = 0
    max_price = 0
    while True:
        try:
            min_price = int(input("min price : "))
            if(min_price >= 0):
                break
            else:
                print("minimum price must be greather than 0")
        except:
            print("price is not valid")

    while True:
        try:
            max_price =int(input("max price : "))
            if not max_price >= 0:
                print("maximum price must be greather than 0")
                continue
            if not max_price>=min_price:
                print("max price must be grater than minimum price")
                continue
                
        except:
            print("price is not valid")
        break
    
    for room in room_list:
        if(room.check_price(min_price , max_price)):
            rooms.append(room)
    return rooms

# Filter rooms that contain selected facilities
def search_by_facilities(room_list): 
    rooms = []
    facilities = []
    while True:
        facility = input("1: TV\n2: internet\n3: refrigerator\nany other key: exit input\nselect: ")
        if(facility == "1"):
            if facilities.count("TV") == 0:
                facilities.append("TV")
        elif(facility == "2"):
            if facilities.count("internet") == 0:
                facilities.append("internet")
        elif(facility == "3"):
            if facilities.count("refrigerator") == 0:
                facilities.append("refrigerator")
        else:
            break
    
    for room in room_list:
        if(room.check_facilities(facilities)):
            rooms.append(room)
    return rooms



def reserve_room(users, room_list , reservation_list , login_username):
    dates=[]
    room_number = input("room number :")
    count=0
    for room in room_list:
        if room.get_room_number()!= room_number:
            count+=1
        else:
            break
    if count==len(room_list):
        print("room number is not exist")
        return users , room_list , reservation_list
    try:
        number_of_people = int(input("number of people : "))
    except:
        print("number of people must be a number !!!")
        return users , room_list , reservation_list
        

    while True:
        try:
            first_date = datetime.date.fromisoformat(input("date must be YYYY-MM-DD\nstart date : "))
            if(first_date >= datetime.date.today()):
                break
            else:
                print("start date must be after today")
        except:
            print("start date is not valid")

    while True:
        try:
            last_date = datetime.date.fromisoformat(input("date must be YYYY-MM-DD\nlast date : "))
            if(last_date >= datetime.date.today()):
                break
            if not last_date>=first_date:
                break
            else:
                print("last date must be after today")
        except:
            print("last date is not valid")
        
    for i in range((last_date-first_date).days + 1):
        dates.append((first_date + datetime.timedelta(i)))

    user_index = -1
    for index in range(len(users)):
        if users[index].check_username(login_username):
            user_index = index
            break
    
    for room in room_list:
        if room.get_room_number() == room_number:
            price=room.get_price() * len(dates)
            if users[user_index].can_pay(price):
                if room.reserve_room(users[user_index].get_balance() , dates , number_of_people):
                    reserve1=Reserve(login_username , room_number , first_date , last_date , number_of_people , price , str(len(reservation_list)))
                    reservation_list.append(reserve1)
                    users[user_index].pay(price)
                    try:
                        with open('users-data.pickle', 'wb') as file:
                            pickle.dump(users, file)
                    except:
                        print("can not write in file")
                    try:
                        with open('rooms-data.pickle', 'wb') as file:
                            pickle.dump(room_list, file)
                    except:
                        print("can not write in file")
                    try:
                        with open('reservation-data.pickle', 'wb') as file:
                            pickle.dump(reservation_list, file)
                    except:
                        print("can not write in file")
                    
                    
                    print("reservation complite")
                    break
            else:
                print("not enough money!!!")
    return users , room_list , reservation_list



users = []
reservation_list=[]
room_list=[]
login_username = ""


try:
    with open('users-data.pickle', 'rb') as file:
        users = pickle.load(file)
except:
    users = []

try:
    with open('rooms-data.pickle', 'rb') as file:
        room_list = pickle.load(file)
except:
    room_list = []

try:
    with open('reservation-data.pickle', 'rb') as file:
        reservation_list = pickle.load(file)
except:
    reservation_list = []
    
is_complite = False
for reserve in reservation_list:
    if reserve.complite_reserve():
        is_complite = True
if is_complite:
    try:
        with open('reservation-data.pickle', 'wb') as file:
            pickle.dump(reservation_list, file)
    except:
        print("can not write in file")

# User authentication section (login or signup)
while(True):
    sucsses = False
    login_or_signup = input("1:login\n2:signup\nselect : ")
    if(login_or_signup == "1"):
        while(True):
            username = input("username : ")
            password = input("password : ")
            
            turn = 0
            sucsses =  False
            for user in users:
                if(user.check_login(username, password) == 1):
                    
                    sucsses = True
                    break
                elif(user.check_login(username, password) == 2):
                    print("password incorrect")
                    continue
                turn+=1
            if(turn == len(users)):
                print("username does not exist") 
            if(sucsses):
                login_username  = username
                break
    if(sucsses):
        break   
    elif(login_or_signup == "2"):
        while (True):
            username = input("username : ")
            turn=0
            for user in users:
                if(not user.check_username(username)):
                    turn+=1
            if(turn == len(users)):
                login_username = username
                break
            print("username is exist !!!")
            
        password = input("password : ")
        name = input("name : ")
        user = User(username, password, name)
        users.append(user)
        try:
            with open('users-data.pickle', 'wb') as file:
                pickle.dump(users, file)
        except:
            print("can not write in file")
        break
while(True):
    select = input("1: increase balance\n2 :search rooms\n3 :reserve room\n4 :watch reserve list\nexit: any other key\nselect : ")
    if(select == "1"):
        while(True):
            try:
                money = int(input("how much $ do you want to add to your wallet? "))
                if(money > 0):
                    break
                else:
                    print("the amount of money must be greater than 0")
            except:
                print("just write a number")
        for user in users:
            if(user.check_username(login_username)):
                user.deposite(money)
                try:
                    with open('users-data.pickle', 'wb') as file:
                        pickle.dump(users, file)
                except:
                    print("can not write in file")

    # search by filter
    elif(select=="2"):
        while True:
            search=input("1:search by type\n2:search by date\n3:search by price\n4:search by facilities\nback:any other key\nselect: ")
            rooms_search_result = []
            if search=="1":
                rooms_search_result = search_by_type(room_list)
            elif search=="2":
                rooms_search_result = search_by_date(room_list)
            elif search == "3":
                rooms_search_result = search_by_price(room_list)
            elif search == "4":
                rooms_search_result = search_by_facilities(room_list)
            else:
                break
            
            for room in rooms_search_result:
                room.show_info()
        
    elif select=="3":
        users , room_list , reservation_list = reserve_room(users , room_list , reservation_list , login_username)
    elif select == "4":
        reserve_number = 0
        filtered_reserve = input("active reservation : 1\nall reservations : any other key")
        if(filtered_reserve=="1"):
            filtered_reserve = "active"
        else:
            filtered_reserve=""
        for resereve in reservation_list:
            if resereve.show_info(login_username , filtered_reserve):
                reserve_number += 1
        if reserve_number == 0:
            print("-----------------------------------")
            print("you have no reservation")
            print("-----------------------------------")
        else:
            print("-----------------------------------")
            cancel = input("do you want to cancel your reservation ? \nYES : 1\nNO: any other key\nselect : ")
            if(cancel == "1"):
                cancel_number = input("enter reservation number you want to cancel")
                done = False
                dates=None
                for reserve in reservation_list:
                    if(reserve.check_reservation_number(cancel_number)):
                        dates = resereve.get_dates()
                        price = reserve.get_price()
                        cancel_room = resereve.get_room_number()
                        if(reserve.check_username(login_username)):
                            for user in users:
                                if user.check_username(login_username) :
                                    if reserve.cancel_reserve():
                                        user.deposite(price)
                                    else:
                                        user.deposite(price / 2)
                                    done = True
                                    break
                    if(done):
                        break
                if(not done):
                    print("wrong reservation number")
                else:
                    for room in room_list:
                        if(room.get_room_number() == cancel_room):
                            room.cancel_reserve(dates)
                    try:
                        with open('users-data.pickle', 'wb') as file:
                            pickle.dump(users, file)
                    except:
                        print("can not write in file")
                    try:
                        with open('rooms-data.pickle', 'wb') as file:
                            pickle.dump(room_list, file)
                    except:
                        print("can not write in file")
                    try:
                        with open('reservation-data.pickle', 'wb') as file:
                            pickle.dump(reservation_list, file)
                    except:
                        print("can not write in file")
    else:
        break