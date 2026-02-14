
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

u1 = User("setayesh" , "1234" , "setayesh")
users = []
reservation_list=[]
room_list=[]
users.append(u1)
a = datetime.date.fromisoformat("2026-02-15")
room1=Room("101" , 3 , 150 , ["TV" , "internet"] )
room2=Room("102" , 1 , 110 , ["internet" , "refrigerator"])
room3=Room("103" , 2 , 90)
room_list.append(room1)
room_list.append(room2)
room_list.append(room3)


with open('users-data.pickle', 'wb') as file:
    pickle.dump(users, file)
with open('rooms-data.pickle', 'wb') as file:
    pickle.dump(room_list, file)
with open('reservation-data.pickle', 'wb') as file:
    pickle.dump(reservation_list, file)
