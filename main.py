import sys,random,os,mysql.connector, time
from prettytable import PrettyTable

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="abhinav07"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS oddeven")
mycursor.execute("USE oddeven")
mycursor.execute("CREATE TABLE IF NOT EXISTS users(userID int primary key, userNAME varchar(30))")
mycursor.execute("CREATE TABLE IF NOT EXISTS scoreboard(userID int, wins int, losses int, highest_score int, lowest_score int, foreign key(userID) references users(userID))")

first = ""
global user_data
user_data = []

print("Welcome to Odd-Even Cricket Game")

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def batting_function(inning, runstobe):
    print("Choose a number from 1 to 6")
    runs = 0
    while True:
        if inning=="second":
            print("You have to chase", runstobe, "runs")
        try:
            num=int(input("You entered: "))
        except:
            num=int(input("You entered: "))
        lst = [1,2,3,4,5,6]
        program_choice = random.choice(lst)
        if num in lst:
            print("Program choose:", program_choice)
            if num==program_choice:
                if user_data!=[]:
                    mycursor.execute(f"SELECT highest_score, lowest_score from scoreboard where userID={user_data[0][0]}")
                    myresult=(mycursor.fetchall())[0]
                    if runs<myresult[1]:
                        mycursor.execute(f"UPDATE scoreboard set lowest_score={runs} where userID={user_data[0][0]}")
                    elif runs>myresult[0]:
                        mycursor.execute(f"UPDATE scoreboard set highest_score={runs} where userID={user_data[0][0]}")
                        mydb.commit()
                if inning=="second":
                    time.sleep(3)
                    cls()
                    print("You are out")
                    print("Program won the match")
                    if user_data!=[]:
                        mycursor.execute(f"UPDATE scoreboard set losses=losses+1 where userID={user_data[0][0]}")
                        mydb.commit()
                    break
                else:
                    print("You scored a total of: ", runs,"runs")
                    print("You have to bowl now")
                    time.sleep(3)
                    cls()
                    bowling_function("second", runs+1)
                    break
            else:
                runs+=num
                time.sleep(3)
                cls()
                print("You scored a total of:", runs, "runs")
                if runstobe!=0:
                    runstobe -=num
                    if runstobe<=0:
                        time.sleep(3)
                        cls()
                        print("You won the match")
                        if user_data!=[]:
                            mycursor.execute(f"UPDATE scoreboard set wins=wins+1 where userID={user_data[0][0]}")
                            mydb.commit()
                        break

def bowling_function(inning, runstobe):
    runs = 0
    print("Choose a number from 1 to 6")
    while True:
        if inning=="second":
            print("Program needs", runstobe, "runs to win")
        try:
            num=int(input("You entered: "))
        except:
            num=int(input("You entered: "))
        lst = [1,2,3,4,5,6]
        program_choice = random.choice(lst)
        if num in lst:
            print("Program choose:", program_choice)
            if num==program_choice:
                   if inning=="second":
                       time.sleep(3)
                       cls()
                       print("Program became out")
                       print("You won the match")
                       if user_data!=[]:
                        mycursor.execute(f"UPDATE scoreboard set wins=wins+1 where userID={user_data[0][0]}")
                        mydb.commit()
                       break
                   else:                   
                       time.sleep(3)
                       cls()  
                       print("Program scored a total of: ", runs,"runs")
                       print("You have to bat now")
                       batting_function("second", runs+1)
                       break
            else:
                runs+=program_choice
                time.sleep(3)
                cls()
                print("Program scored a total of:", runs, "runs")
                if runstobe!=0:
                    runstobe -=program_choice
                    if runstobe<=0:
                        time.sleep(3)
                        cls()
                        print("Program won the match")
                        if user_data!=[]:
                            mycursor.execute(f"UPDATE scoreboard set losses=losses+1 where userID={user_data[0][0]}")
                            mydb.commit()
                        break

cls()
print("Welcome to Odd-Even")


while True:
    ch1=input("Menu (Select options by just entering the number)\n1. Login\n2. Signup\n3. Play as a guest\n")
    if ch1=="1":
        login = int(input("Enter your user id"))
        mycursor.execute(f"SELECT userID, userName from users where userID={login}")
        myresult = mycursor.fetchall()
        if myresult==[]:
            print("Invalid User ID. Enter again")
        else:
            user_data = myresult
            break
    elif ch1=="2":
        login = input("Enter your name")
        userno = random.choice(range(10000,99999))
        mycursor.execute(f"SELECT userID from users where userID={userno}")
        myresult = mycursor.fetchall()
        if myresult!=[]:
            userno = random.choice(range(10000,99999))
        mycursor.execute(f"INSERT INTO users values({userno}, '{login}')")
        mycursor.execute(f"INSERT INTO scoreboard values({userno}, 0,0,0,0)")
        mydb.commit()
        print(f"Registered succesfully. Please remember your User ID:-\n{userno}")
    elif ch1=="3":
        break
    else:
        cls()
        continue
cls()
if user_data!=[]:
    print(f"Welcome back, {user_data[0][1]}")

while True:
    ch=input("Menu (Select options by just entering the number)\n1. Start a new game\n2. Rules\n3. View your data\n4. View leaderboard\n5. Delete your data\n6. Exit\n")
    if ch=="1":
        cls()
        toss = input("Do you wish to (Just enter the number):-\n1. Bat first\n2. Bowl first")
        if toss=="1":
            first = "batting"
            cls()
            batting_function("first",0)
        else:
            first = "bowling"
            cls()
            bowling_function("first",0)
    elif ch=="2":
        cls()
        print("The rules for the game is:\n1. You can select whether to bat first or bowl first.\n2. Depending on what you chose, you can type in numbers from 1 to 6 only.\n3. If you and the program chooses the same number you will be out. \n4. A win will fetch you 3 points, while losing a game will deduct 1 point from you. Ties won't affect your score.\nAll the best.\n\n")
        continue
    elif ch=="3":
        cls()
        if user_data==[]:
            print("You are logged in as a guest. Signup or login to view your data in Odd-Even!")
        else:
            print("Fetching your data from Odd-Even's database")
            mycursor.execute(f"SELECT * FROM scoreboard where userID={user_data[0][0]}")
            try:
                myresult = (mycursor.fetchall())[0]
                print("Wins: ", myresult[1])
                print("Losses: ", myresult[2])
                print("Highest Score: ", myresult[3])
                print("Lowest Score: ", myresult[4])
            except:
                print("No data available. Play a game to get data!")
    elif ch=="5":
        cls()
        confirm = input("Menu (Select options by just entering the number)\n1. Delete your game data\n2. Delete your profile\n3. Go back")
        if confirm=="1":
            mycursor.execute(f"DELETE FROM scoreboard where userID={user_data[0][0]}")
            mydb.commit()
            print("Deleted data successfully")
            time.sleep(2)
            cls()
            continue
        elif confirm=="2":
            mycursor.execute(f"DELETE FROM scoreboard where userID={user_data[0][0]}")
            mycursor.execute(f"DELETE FROM users where userID={user_data[0][0]}")
            mydb.commit()
            print("Deleted data successfully. The program will now exit.")
            time.sleep(2)
            exit()
        else:
            cls()
            continue
    elif ch=="4":
        cls()
        print("Fetching leaderboard")
        mycursor.execute('''SELECT wins, losses, userID from scoreboard order by wins desc, losses, highest_score desc''')
        myresult=mycursor.fetchall()
        t = PrettyTable(['Rank', 'Player', "Matches", "Wins", "Losses",'Points'])
        i = 1
        for wins, losses, userID in myresult:
            mycursor.execute(f"SELECT userName from users where userID={userID}")
            userName = mycursor.fetchall()[0][0]
            t.add_row([i, userName, wins+losses, wins, losses, wins*3-losses*1])
            i+=1
        print(t)

    elif ch=="6":
        sys.exit()
    else:
        cls()
        continue
