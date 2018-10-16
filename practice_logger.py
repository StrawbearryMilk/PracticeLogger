import time 
import pickle
from datetime import date

class AccountMap:
    """Dictionary class to manage saved user Accounts"""
    def __init__(self): 
        self.map = {}

    def isValidAccount(self, submission):
        if submission[0] in self.map:
            username = submission[0]
            if str(submission[1]) == self.map[username].getPassword():
                return True
        return False

    def isUsernameAvailable(self, username):
        return username not in self.map

    def addAccount(self, username, password):
        self.map[username] = Account(username = username, password = password, points = 0, multiplier = 0, lastDate = date.today())
        return self.map[username]

    def delAccount(self, username):
        removedAccount = self.map[username]
        del(self.map[username])
        return removedAccount
    
    def updateAccount(self, username, password, points, multiplier, consecutiveDays):
        self.map[username] = Account(username = username, password = password, points = points, multiplier = multiplier, lastDate = date.today())
        print("Okay " + username + ", you're information has been updated.")    
        return self.map[username]

class Account: 
    """Object stored in the Account map

    Each account has a username, password, total points accumulated (awarded by working for 
    15 minutes), a multiplier based on consecutive days worked, and the lastDate this account 
    worked. The last date attribute is used to update the multiplier.
    
    """
    
    def __init__(self, username, password, points, multiplier, lastDate):
        self.username = ""; self.password = ""; self.points = 0; self.multiplier = 0
        self.lastDate = date.today()

    def updateMultiplierAndLastDate(self, multiplier, lastDate):
        diff = date.today() - self.lastDate
        if (diff != 1):
            self.multiplier = 1
        else: #last date played was yesterday
            self.multiplier += 1
        self.lastDate = 1 #No need to store previous date

    def incrementPoints(self, points, multiplier): #t is amount of time currently spent
        self.points += multiplier

    def getUsername(self, username):
        return self.username

    def getPassword(self):
        return self.password
    
    def changePassword(self, password, newPassword):
        self.password = newPassword
        return newPassword

    def getPoints(self):
        return self.points

timeToday = 0 #amount of time in minutes spent on practice today
#totalTime = 0 #total time spent training, 0 if user does not already have account
newUser = False
try:
    with open('account_storage.pkl', 'rb') as pklf:
        accountDict = pickle.load(pklf)
except:
    newUser = True
    accountDict = AccountMap()
    print("Welcome! Let's create an account for you.")
print(accountDict.isUsernameAvailable("name"))
if newUser == False:
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
        submission = [username,password]
        if accountDict.isValidAccount(submission):
            print("Welcome,", username)
            account = accountDict[submission[0]]
            print("So far you have", account.getPoints())
        else:
            print("kys")
    elif choice == "n":
        newUser = True #I need a way to make this occur when a pkl exists, 
                       #and when I just want a new account made
                       #I'm sure there's a more efficient way to do this...
                       #But that's what comes to mind at the moment
if newUser == True: 
    print("Okay, what is your desired username? ")
    username = input()
    print("And password? Just press Enter if you don't want to have one!")
    password = input()
    if password == "":
        print("You're gonna get hacked... not that anyone is using this...\n")
        print("Or that anyone will even want to get in your account... or that there's anything of value...")
        print("Time to re-evaluate my life goals...")
    print("Now let's create a save file for your account set.")
    account = Account(username, password, 0,0,0)
    accountDict.addAccount(username, password)
    with open('account_storage.pkl', 'wb') as pklf:
        pickle.dump(accountDict, pklf)
print("Welcome. Time for the trial!")
mins = 0
setMins = 15 #used to adjust the waiting time in minutes
ptsTracker = 0 #when logged time exceeds a new value of 15, we can increment the points
lastDate = date.today()
while True:
    time.sleep(60*setMins)
    mins += setMins
    print('\a')
    if (mins//15 > ptsTracker):
        account.incrementPoints(ptsTracker, lastDate)
        ptsName = "point" if ptsTracker == 1 else "points"
        print("You've gained", account.getPoints(), ptsName)
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
    -write statement for attempting to sign in with non-existing username
        -will loop back to original question
    -Save the dictionary at the end
    -Use pickles to save the above hashmap (will have multiple users)
    -Statement for log and save completion
    -Save user info once they sign out
    -Detect existence of pickle 
    -Implement consecutive day counter
        -after sign in, show consec days and multiplier
        -will be updated once you successfully sign out
        -use datetime to verify consecutiveness
    -password verification
    -Pop up for username, pw, sign out, desired time
    -Display countdown ? (or stop watch)
    -Implement API to remotely log hours
    -GUI stuff 
    -Share
    -redo in Java or something 
    
'''