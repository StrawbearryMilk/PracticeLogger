import time 
import pickle

class AccountMap:
    def __init__(self): 
        self.map = {}
    
    def addAccount(self, username, password):
        if (username not in self.map):
            self.map[username] = Account(username = username, password = password, points = 0, multiplier = 0, consecutiveDays = 0)
        else:
            print("That username already exists!")
    
    def delAccount(self, username):
        del(self.map[username])
    
    def updateAccount(self, username, password, points, multiplier, consecutiveDays):
        self.map[str(username)] = Account(username = username, password = password, points = points, multiplier = multiplier, consecutiveDays = consecutiveDays)
            print("Okay " + username + ", you're information has been updated.")    


class Account: 
    #each account has username, password, total points (awarded by working), multiplier based on consecutive days worked
    def __init__(self, username, password, points, multiplier, consecutiveDays):
        self.username = ""; self.password = ""; self.points = 0; self.multiplier = 0; self.consecutiveDays = 0
    
    def incrementPoints(self, t, consecutiveDays, points): #t is amount of time currently spent
        value = self.multiplier if self.consecutiveDays > 0 else 1
        if t % 15 == 0:
            points += value
    #method to check validity of login info. will update this when dicts are implemented
    def isUsername(self, username, submission):
        submission == self.username

    def isPassword(self, password, submission):
        submission == self.password

    def getUsername(self, username):
        return self.username

    def getPassword(self, password):
        return self.password

timeToday = 0 #amount of time in minutes spent on practice today
totalTime = 0 #total time spent training, 0 if user does not already have account

print("Hello, do you have an account? (y/n)")
choice = input()

choice_count = 0
while choice not in ["y", "n"]:
    choice_count += 1
    if choice_count == 10:
        print("You're hopeless...\n\n\n bye bye")
        exit()

    print("That wasn't an option.\n Now, do you have an account? (y/n)")
    choice = input()

if choice == "y":
    print("Alright.\n Enter your username: ")
    username = input()
    print("Enter your password: ")
    password = input()
elif choice == "n":
    print("Okay, what is your desired username? ")
    username = input()
    print("And password? Just press Enter if you don't want to have one!")
    password = input()
    if password == "":
        print("You're gonna get hacked... not that anyone is using this...\n")
        print("Or that anyone will even want to get in your account... or that there's anything of value...")
        print("Time to re-evaluate my life goals...")
    account = Account(username, password, 0,0,0)

print("Welcome. Time for the trial!")
mins = 0
setMins = 15 #used to adjust the waiting time in minutes
while True:
    time.sleep(60*setMins)
    mins += setMins
    
    if (mins % 1 == 0):
        print('\a')
        print("You've reached " + str(mins) + " minutes. Do you wish to stop?(y/n)\n")
        choice = input()
        while choice not in ["y","n"]:
            print("y or n only")
            choice = input()
        if choice == "y":
            print("Now saving your data...\n...\nData has been saved. (not really, that's coming in a later version.)")
            break
        else:
            print("Okay, let's keep going!")
            choice = int(input("How many more minutes until I bother you again?\n"))
            while not isinstance(choice, int):
                print("No, give me a number in minutes.")
                choice = int(input())
            setMins = choice
            print("Okay, let's go for", setMins, "minutes!")
            continue
print("Ciao ciao!")

'''
Future ideas
    -Incorporate notification sound
    -Define a hashmap to store user info
    -Use pickles to save the above hashmap (will have multiple users)
    -Statement for log and save completion
    -Save user info once they sign out
    -Detect existence of pickle 
    -Implement consecutive day counter
        -after sign in, show consec days and multiplier
        -will be updated once you successfully sign out
        -use datetime to verify consecutiveness
    -Pop up for username, pw, sign out, desired time
    -Display countdown ? (or stop watch)
    -Implement API to remotely log hours
    -GUI stuff 
    -Share
    -redo in Java or something 
    
'''