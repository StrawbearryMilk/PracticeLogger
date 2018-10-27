import time 
import pickle
from datetime import date, timedelta


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
        self[username] = Account(username = username, password = password, points = 0, multiplier = 1, lastDate = date.today())
        return self[username]

    """"Removes account from dictionary"""
    def delAccount(self, username):
        removedAccount = self[username]
        del(self[username])
        return removedAccount
    
    """Updates account information. May add password change feature later, dunno"""
    def updateAccount(self, username, password, points, multiplier, lastDate):
        self[username] = Account(username = username, password = password, points = points, multiplier = multiplier, lastDate = date.today())
        print("Okay " + username + ", you're information has been updated.")    
        return self[username]

class Account: 
    """Object stored in the Account map

    Each account has a username, password, total points accumulated (awarded by working for 
    15 minutes), a multiplier based on consecutive days worked, and the lastDate this account 
    worked. The last date attribute is used to update the multiplier.
    
    """
    def __init__(self, username, password, points = 0, multiplier = 1, lastDate = date.today()):
        self.username = ""; self.password = ""; self.points = 0; self.multiplier = 1
        self.lastDate = date.today()

    """Increment points based on number of days consecutively logged on"""
    def incrementPoints(self, multiplier): #t is amount of time currently spent
        self.points += multiplier

    """Returns username of the account"""
    def getUsername(self, username):
        return self.username

    """Returns password of the account"""
    def getPassword(self):
        return self.password
    
    """Changes password of the account, don't know if I'll actually use this"""
    def changePassword(self, password, newPassword):
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

timeToday = 0 #amount of time in minutes spent on practice today
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
        print("Alright.\n Enter your username: ")
        username = input()
        print("Enter your password: ")
        password = input()
        submission = [username,password]        
        
        if (accountDict.isValidAccount(submission) == False):
            while True:
                print("Invalid log-in information. Please try again.")
                print("Enter your username: ")
                username = input()
                print("Enter your password: ")
                password = input()
                submission = [username,password]
                if accountDict.isValidAccount(submission):
                    account = accountDict[submission[0]]
                    break
            
        print("Welcome,", username)
        account = accountDict[submission[0]]
        print("So far you have", account.getPoints(), "points!")
        account.adjustMultiplier()           

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
    account = Account(username, password)
    accountDict.addAccount(username, password)
    with open('account_storage.pkl', 'wb') as pklf:
        pickle.dump(accountDict, pklf)
print("Welcome. Time for the trial!")
multi = account.getMultiplier()
mins = 0
setMins = 15 #used to adjust the waiting time in minutes
ptsTracker = 0 #when logged time exceeds a new value of 15, we can increment the points
while True:
    time.sleep(60)#*setMins)
    mins += setMins
    print('\a')
    if (mins//15 > ptsTracker):
        ptsTracker += 1
        account.incrementPoints(multi)
        ptsName = "point" if multi == 1 else "points"
        print("You've gained", ptsTracker*multi, ptsName)
        print("You've reached " + str(mins) + " minutes. Do you wish to stop?(y/n)\n")
        choice = input()
        while choice not in ["y","n"]:
            print("y or n only")
            choice = input()
        if choice == "y":
            print("Now saving your data...")
            accountDict[username] = account
            print(account.getPoints)
            #accountDict.updateAccount(username = username, password = password, points = points, multiplier = multi, lastDate = date.today())
            print("Data has been saved. (not really, that's coming in a later version.)")
            with open('account_storage.pkl', 'wb') as pklf:
                pickle.dump(accountDict, pklf)
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
    -same text should pop up after unsuccessful login succeeds
    -Incorporate better notification sound
    -Save user info once they sign out
    -Pop up for username, pw, sign out, desired time
    -Display countdown ? (or stop watch)
    -Implement API to remotely log hours
    -GUI stuff 
    -Share
    -redo in Java or something 
    
'''