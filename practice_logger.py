import time 
import pickle
from datetime import date, datetime, timedelta
import sys

class Account: 
    """Object stored in the Account map

    Each account has a username, password, total points accumulated (awarded by working for 
    15 minutes), a multiplier based on consecutive days worked, and the lastDate this account 
    worked. The last date attribute is used to update the multiplier.
    
    """
    def __init__(self, username, password, points = 0, multiplier = 1, lastDate = date.today()):
        self.username = username; self.password = password; self.points = points; 
        self.multiplier = multiplier; self.lastDate = date.today()

    """Increment points based on number of days consecutively logged on"""
    def incrementPoints(self, multiplier):
        self.points += multiplier

    """Returns username of the account"""
    def getUsername(self):
        return self.username

    """Returns password of the account"""
    def getPassword(self):
        return self.password
    
    """Changes password of the account, don't know if I'll actually use this"""
    def changePassword(self, newPassword):
        self.password = newPassword
        return newPassword

    """Returns points the user has"""
    def getPoints(self):
        return self.points
    
    """Returns the multiplier value"""
    def getMultiplier(self):
        return self.multiplier
    
    """Adjusts the multiplier based on when the user last logged on"""
    def adjustMultiplier(self):
        if self.lastDate == date.today() - timedelta(days = 1): #logged on yesterday, keep boosting multiplier
            self.multiplier += 1
        elif self.lastDate != date.today():
            self.multiplier = 1 #no consecutive days, restart multiplier
        else:
            print("Nothing to change today!")

    def __repr__(self):
        params = [self.username, self.password, self.points, 
            self.multiplier, self.lastDate]
        s = ", ".join(map(str, params))
        s = "Account(%s)" % ( s)#, #self.__class__.__name__, s)
        return s

    def __str__(self):
        ptsTerm = 'point' if self.points == 1 else 'points'
        return self.username + ' has ' + str(self.points) + ' ' + ptsTerm + ' with a multiplier of ' + str(self.multiplier) + ' and last played on ' + str(self.lastDate) + '.'

class AccountMap(dict):
    """Dictionary class to manage saved user Accounts"""
    def __init__(self, *arg, **kwargs): 
        super(AccountMap, self).__init__(*arg, **kwargs)
    """Check to see if account username and password are correct"""
    def isValidAccount(self, login):
        if login[0] in self:
            if self[login[0]].getPassword() == login[1]:
                return True
        else:
            return False

    """"Checks to see if a user can claim this username"""
    def isUsernameAvailable(self, username):
        return username not in self

    """Adds account to the dictionary"""
    def addAccount(self, username, password):
        self[username] = Account(username = username, password = password)

    """"Removes account from dictionary"""
    def delAccount(self, username):
        removedAccount = self[username]
        del(self[username])
        return removedAccount
    
    """Updates account information. May add password change feature later, dunno"""
    def updateAccount(self, username, password, points, multiplier, lastDate):
        self[username] = Account(username = username, password = password, points = points, multiplier = multiplier, lastDate = date.today())
        print("Okay " + username + ", you're information has been updated.")    

newUser = False #False if there is no pickle file or if you wish to make a new account
try:
    with open('account_storage.pkl', 'rb') as pklf:
        accountDict = pickle.load(pklf)
except:
    newUser = True
    accountDict = AccountMap()
    print("Welcome! Let's create an account for you.")

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
        while True:
            print("Enter your username: ", end = "")
            username = input()
            print("Enter your password: ", end = "")
            password = input()
            submission = [username,password]
            if accountDict.isValidAccount(submission):
                account = accountDict[submission[0]]
                break
            else:
                print("Invalid account information. Please try again.")

        #print(account)
        print("Welcome,", username)
        ptsName = "point." if account.points == 1 else "points!"
        print("So far you have", account.getPoints(), ptsName)
        #print(account.lastDate)
        #account.lastDate = date.today() - timedelta(days = 1)
        account.adjustMultiplier()           

    elif choice == "n":
        newUser = True
                       
if newUser == True: 
    print("Enter your desired username: ", end = "")
    username = input()
    print("Enter a password (just pressing Return is fine too): ", end = "")
    password = input()
    if password == "":
        print("You're gonna get hacked... not that anyone is using this...\n")
        print("Or that anyone will even want to get in your account... or that there's anything of value...")
        print("Time to re-evaluate my life goals...")
    print("Now let's create a save file for your account set.")
    accountDict.addAccount(username, password)
    account = accountDict[username]
    with open('account_storage.pkl', 'wb') as pklf:
        pickle.dump(accountDict, pklf)

print("Time to get busy!")
multi = account.getMultiplier()
minsToAdd = 0; minsRemaining = 0; minsTotal = 0
setMins = 15 #used to adjust the waiting time in minutes
ptsTracker = 0 #when logged time exceeds a new value of 15, we can increment the points
while True:
    time.sleep(setMins)
    minsTotal += (setMins + minsRemaining)
    minsRemaining += setMins%15
    minsToAdd = minsTotal//15
    print('\a')
    if (minsToAdd >= 1): #If 1+ points are gained, increment by points * multi
        account.incrementPoints(multi*minsToAdd)
        ptsName = "point." if minsToAdd*multi == 1 else "points."
        print("You've gained", minsToAdd*multi, ptsName)
        minsTotal = minsRemaining
        minsRemaining = 0
    print("You've reached your goal of " + str(setMins) + " minutes.")
    
    choice = input("Do you wish to stop: ")
    while choice not in ["y","n"]:
        print("y or n only")
        choice = input()
    if choice == "y":
        print("Now saving your data...")
        accountDict.updateAccount(username, 
            password, account.points, multi, date.today())
        with open('account_storage.pkl', 'wb') as pklf:
            pickle.dump(accountDict, pklf)

        print("Data has been saved.")
        break

    else:
        print("Okay, let's keep going!")
        choice = int(input("How many more minutes until I bother you again?\n"))
        while not isinstance(choice, int):
            print("No, give me a number in minutes.")
            choice = int(input())
        setMins = choice
        print("Okay, let's go for", setMins, "minutes!")
        
print("Ciao ciao!")
sys.exit()