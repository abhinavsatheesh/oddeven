import sys,random,os,mysql.connector, time, prettytable
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pylab

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="abhinav07",
  autocommit=True,
  port="3306"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS oddeven")
mycursor.execute("USE oddeven")
mycursor.execute("CREATE TABLE IF NOT EXISTS users(userID int primary key, userNAME varchar(30))")
mycursor.execute("CREATE TABLE IF NOT EXISTS scoreboard(userID int, wins int, losses int, highest_score int, lowest_score int, foreign key(userID) references users(userID))")
mycursor.execute("CREATE TABLE IF NOT EXISTS livematch (MatchID int, UserID1 int, UserID2 int, toss char (7))")
mycursor.execute(f"CREATE TABLE IF NOT EXISTS program_match_data (num int)")
global user_data
user_data = []

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def batting_players(hostOrPlayer, inning, runstobe, matchno):
    print("Choose a number from 1 to 6")
    i=1
    runs = 0
    while True:
        if inning=="second":
            print("You have to chase", runstobe, "runs")
        try:
            num=int(input("You entered: "))
            if num not in [1,2,3,4,5,6]:
                continue
        except:
            num=int(input("You entered: "))
        if hostOrPlayer=="host":
            mycursor.execute(f"INSERT INTO MATCH_{matchno} (last_num_host, Balls, innings, batting) VALUES({num}, {i}, '{inning}', {user_data[0][0]})")
            mydb.commit()
            while True:
                mycursor.execute(f"SELECT last_num_player from match_{matchno} where Balls={i} and last_num_host is NULL and innings='{inning}'")
                myresult = mycursor.fetchall()
                if myresult!=[]:
                    print(f"Player entered: {myresult[0][0]}")
                    i+=1
                    break
        else:
            mycursor.execute(f"INSERT INTO MATCH_{matchno} (last_num_player, Balls, innings, batting) VALUES({num}, {i}, '{inning}', {user_data[0][0]})")
            mydb.commit()
            while True:
                mycursor.execute(f"SELECT last_num_host from match_{matchno} where Balls={i} and last_num_player is NULL and innings='{inning}'")
                myresult = mycursor.fetchall()
                if myresult!=[]:
                    print(f"Host entered: {myresult[0][0]}")
                    i+=1
                    break
        player_num = myresult[0][0]
        if num==player_num:
            mycursor.execute(f"SELECT highest_score, lowest_score from scoreboard where userID={user_data[0][0]}")
            myresult=(mycursor.fetchall())[0]
            if runs<myresult[1]:
                mycursor.execute(f"UPDATE scoreboard set lowest_score={runs} where userID={user_data[0][0]}")
                mydb.commit()
            elif runs>myresult[0]:
                mycursor.execute(f"UPDATE scoreboard set highest_score={runs} where userID={user_data[0][0]}")
                mydb.commit()
            if inning=="second":
                time.sleep(1)
                cls()
                print("You are out")
                print("You lost the match")
                if user_data!=[]:
                    mycursor.execute(f"UPDATE scoreboard set losses=losses+1 where userID={user_data[0][0]}")
                    mydb.commit()
                break
            else:
                print("You scored a total of: ", runs,"runs")
                print("You have to bowl now")
                time.sleep(1)
                cls()
                bowling_players(hostOrPlayer, "second", runs+1, matchno)
                break
        else:
            runs+=num
            time.sleep(1)
            cls()
            print("You scored a total of:", runs, "runs")
            if runstobe!=0:
                runstobe -=num
                if runstobe<=0:
                    time.sleep(1)
                    cls()
                    print("You won the match")
                    if user_data!=[]:
                        mycursor.execute(f"UPDATE scoreboard set wins=wins+1 where userID={user_data[0][0]}")
                        mydb.commit()
                    break

def bowling_players(hostOrPlayer, inning, runstobe, matchno):
    print("Choose a number from 1 to 6")
    runs = 0
    i=1
    while True:
        if inning=="second":
            if hostOrPlayer=="host":
                print(f"Player needs", runstobe, "runs to win")
            else:
                print(f"Host needs", runstobe, "runs to win")
        try:
            num=int(input("You entered: "))
            if num not in [1,2,3,4,5,6]:
                continue
        except:
            num=int(input("You entered: "))
        if hostOrPlayer=="host":
            mycursor.execute(f"INSERT INTO MATCH_{matchno} (last_num_host, Balls, innings, bowling) VALUES({num}, {i}, '{inning}', {user_data[0][0]})")
            mydb.commit()
            while True:
                mycursor.execute(f"SELECT last_num_player from match_{matchno} where Balls={i} and last_num_host is NULL and innings='{inning}'")
                myresult = mycursor.fetchall()
                if myresult!=[]:
                    print(f"Player entered: {myresult[0][0]}")
                    i+=1
                    break
        else:
            mycursor.execute(f"INSERT INTO MATCH_{matchno} (last_num_player, Balls, innings, bowling) VALUES({num}, {i}, '{inning}', {user_data[0][0]})")
            mydb.commit()
            while True:
                mycursor.execute(f"SELECT last_num_host from match_{matchno} where Balls={i} and last_num_player is NULL and innings='{inning}'")
                myresult = mycursor.fetchall()
                if myresult!=[]:
                    print(f"Host entered: {myresult[0][0]}")
                    i+=1
                    break
        player_num = myresult[0][0]
        if num==player_num:
            if inning=="second":
                time.sleep(1)
                cls()
                print("You won the match")
                if user_data!=[]:
                    mycursor.execute(f"UPDATE scoreboard set wins=wins+1 where userID={user_data[0][0]}")
                    mycursor.execute(f"DELETE from livematch where matchid={matchno}")
                    mydb.commit()
                    break
            else:                   
                time.sleep(1)
                cls()  
                if hostOrPlayer=="player":
                    print(f"Host scored a total of:", runs, "runs")
                else:
                    print(f"Player scored a total of:", runs, "runs")
                print("You have to bat now")
                batting_players(hostOrPlayer, "second", runs+1, matchno)
                break
        else:
            runs+=player_num
            time.sleep(1)
            cls()
            if hostOrPlayer=="player":
                print(f"Host scored a total of:", runs, "runs")
            else:
                print(f"Player scored a total of:", runs, "runs")
            if runstobe!=0:
                runstobe -=player_num
                if runstobe<=0:
                    time.sleep(1)
                    cls()
                    print("You lost the match")
                    if user_data!=[]:
                        mycursor.execute(f"UPDATE scoreboard set losses=losses+1 where userID={user_data[0][0]}")
                        mycursor.execute(f"DELETE from livematch where matchid={matchno}")
                        mydb.commit()
                    break

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
            print("Program chose:", program_choice)
            if num==program_choice:
                if user_data!=[]:
                    mycursor.execute(f"SELECT highest_score, lowest_score from scoreboard where userID={user_data[0][0]}")
                    myresult=(mycursor.fetchall())[0]
                    if runs<myresult[1]:
                        mycursor.execute(f"UPDATE scoreboard set lowest_score={runs} where userID={user_data[0][0]}")
                    elif runs>myresult[0]:
                        mycursor.execute(f"UPDATE scoreboard set highest_score={runs} where userID={user_data[0][0]}")
                if inning=="second":
                    time.sleep(1)
                    cls()
                    print("You are out")
                    print("You lost the match")
                    if user_data!=[]:
                        mycursor.execute(f"UPDATE scoreboard set losses=losses+1 where userID={user_data[0][0]}")
                        mycursor.execute(f"INSERT INTO program_match_data values({num})")
                        mydb.commit()
                    break
                else:
                    print("You scored a total of: ", runs,"runs")
                    print("You have to bowl now")
                    time.sleep(1)
                    mycursor.execute(f"INSERT INTO program_match_data values({num})")
                    mydb.commit()
                    cls()
                    bowling_function("second", runs+1)
                    break
            else:
                runs+=num
                time.sleep(1)
                cls()
                print("You scored a total of:", runs, "runs")
                if runstobe!=0:
                    runstobe -=num
                    if runstobe<=0:
                        time.sleep(1)
                        cls()
                        print("You won the match")
                        if user_data!=[]:
                            mycursor.execute(f"UPDATE scoreboard set wins=wins+1 where userID={user_data[0][0]}")
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
            print("Program chose:", program_choice)
            if num==program_choice:
                   if inning=="second":
                       time.sleep(1)
                       cls()
                       print("Program became out")
                       print("You won the match")
                       if user_data!=[]:
                        mycursor.execute(f"UPDATE scoreboard set wins=wins+1 where userID={user_data[0][0]}")
                       break
                   else:                   
                       time.sleep(1)
                       cls()  
                       print("Program scored a total of: ", runs,"runs")
                       print("You have to bat now")
                       batting_function("second", runs+1)
                       break
            else:
                runs+=program_choice
                time.sleep(1)
                cls()
                print("Program scored a total of:", runs, "runs")
                if runstobe!=0:
                    runstobe -=program_choice
                    if runstobe<=0:
                        time.sleep(1)
                        cls()
                        print("Program won the match")
                        if user_data!=[]:
                            mycursor.execute(f"UPDATE scoreboard set losses=losses+1 where userID={user_data[0][0]}")
                        break

cls()
print("Welcome to Odd-Even")

while True:
    try:
        ch1=input("Menu (Select options by just entering the number)\n1. Login\n2. Signup\n3. Play as a guest\n4. Exit\n")
        if ch1=="1":
            cls()
            login = int(input("Enter your user id"))
            mycursor.execute(f"SELECT userID, userName from users where userID={login}")
            myresult = mycursor.fetchall()
            if myresult==[]:
                cls()
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
            print(f"Registered succesfully. Please remember your User ID:-\n{userno}")
        elif ch1=="3":
            break
        elif ch1=="4":
            cls()
            exit()
        else:
            cls()
            continue
    except:
        exit()
cls()
if user_data!=[]:
    print(f"Welcome back, {user_data[0][1]}")

while True:
    try:
        ch=input("Menu (Select options by just entering the number)\n1. Start a new game\n2. Rules\n3. View your data\n4. View leaderboard\n5. Delete your data\n6. Exit\n")
        if ch=="1":
            cls()
            while True:
                ques = input("Start a game with:-\n1. The program\n2. With other players")
                if ques=="1":
                    cls()
                    while True:
                        toss = input("Do you wish to (Just enter the number):-\n1. Bat first\n2. Bowl first")
                        if toss=="1":
                            first = "batting"
                            cls()
                            batting_function("first",0)
                            break
                        elif toss=="2":
                            first = "bowling"
                            cls()
                            bowling_function("first",0)
                            break
                        else:
                            cls()
                            continue
                    break
                elif ques=="2":
                    cls()
                    if user_data==[]:
                        print("You are logged in as a guest. Signup or login to play with other players in Odd-Even!")
                    else:
                        while True:
                            q = input("Do you wish to:-\n1. Create a match\n2. Join match created by other players")
                            if q=="1":
                                matchno = random.randint(10000,99999)
                                print(f"Created match no. {matchno}")
                                print("Publishing to Database")
                                mycursor.execute(f"INSERT INTO livematch VALUES({matchno}, {user_data[0][0]}, NULL, NULL)")
                                mycursor.execute(f"CREATE TABLE MATCH_{matchno} (last_num_host int, last_num_player int, Balls int, innings varchar(7), batting int, bowling int)")
                                print("Searching for players....\nIf at any point, you wish to quit, press CTRL+C")
                                while True:
                                    try:
                                        mycursor.execute(f"SELECT userID2 from livematch where userID1={user_data[0][0]} and userID2 is Null")
                                        myresult = mycursor.fetchall()
                                        if myresult!=[(None,)]:
                                            break
                                    except KeyboardInterrupt:
                                        mycursor.execute(f"DELETE FROM livematch where userID1={user_data[0][0]}")
                                        break
                                cls()
                                print("A player has been found!")
                                print(f"Joining match {matchno}")
                                print("As the host, you decide the toss")
                                while True:
                                    toss = input("Toss! Do you wish to:-\n1. Bat first\n2. Bowl first")
                                    if toss=="1":
                                        first = "batting"
                                        cls()
                                        print(f"You chose {first}")
                                        print("Remember, for this match, you are the host")
                                        mycursor.execute(f"UPDATE livematch set toss='batting' where userID1={user_data[0][0]}")
                                        batting_players("host", "first",0, matchno)
                                        break
                                    elif toss=="2":
                                        first = "bowling"
                                        cls()
                                        print(f"You chose {first}")
                                        print("Remember, for this match, you are the host")
                                        mycursor.execute(f"UPDATE livematch set toss='bowling' where userID1={user_data[0][0]}")
                                        bowling_players("host", "first",0, matchno)
                                        break
                                    else:
                                        cls()
                                        print("As the host, you decide the toss")
                                        continue
                                break   
                            elif q=="2":
                                print("Looking for matches")
                                mycursor.execute("SELECT matchID from livematch where userID2 is NULL")
                                myresult = mycursor.fetchall()
                                if myresult==[]:
                                    print("No matches available currently")
                                else:
                                    cls()
                                    print("A match has been found!")
                                    mycursor.execute(f"UPDATE livematch set userID2={user_data[0][0]} where userID2 is NULL LIMIT 1;")
                                    mycursor.execute(f"SELECT matchID from livematch where userID2={user_data[0][0]}")
                                    myresult=mycursor.fetchall()
                                    matchno=myresult[0][0]
                                    print(f"Joining match {matchno}")
                                    print("Please wait, while the host decides the toss")
                                    while True:
                                        mycursor.execute(f"SELECT toss from livematch where userID2={user_data[0][0]}")
                                        myresult = mycursor.fetchall()[0][0]
                                        if myresult!=None:
                                            break
                                    mycursor.execute(f"SELECT toss from livematch where userID2={user_data[0][0]}")
                                    myresult = mycursor.fetchall()[0][0]
                                    if myresult=="batting":
                                        first = 'bowling'
                                        cls()
                                        print(f"You have to bowl")
                                        print("Remember, for this match, you are the player")
                                        bowling_players("player", "first",0, matchno)
                                    else:
                                        first = 'batting'
                                        cls()
                                        print(f"You have to bat")
                                        print("Remember, for this match, you are the player")
                                        batting_players("player", "first",0, matchno)
                                break
                            else:
                                cls()
                                continue
                        break
                else:
                    cls()
                    continue
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
                mycursor.execute("SHOW TABLES")
                live_matches = []
                myresult=mycursor.fetchall()
                matching_strings = [t for s in myresult if s[0].startswith("match_") for t in s]
                results1, results2 = [], []
                if matching_strings!=[]:
                    for match in matching_strings:
                        try:
                            mycursor.execute(f"select innings from {match} where batting={user_data[0][0]}")
                            myresult=mycursor.fetchall()
                            innings = myresult[0][0]
                            if myresult!=[]:
                                for i in range(len(myresult)):
                                    mycursor.execute(f"select last_num_host from {match} where Balls={i+1} and innings='{innings}' and last_num_host is not null")
                                    myresult1=((mycursor.fetchall())[0])[0]
                                    mycursor.execute(f"select last_num_player from {match} where Balls={i+1} and innings='{innings}' and last_num_player is not null")
                                    myresult2=((mycursor.fetchall())[0])[0]
                                    if myresult1==myresult2:
                                        results1.append(myresult1)
                            mycursor.execute(f"select innings from {match} where bowling={user_data[0][0]}")
                            myresult=mycursor.fetchall()
                            innings = myresult[0][0]
                            if myresult!=[]:
                                for i in range(len(myresult)):
                                    mycursor.execute(f"select last_num_host from {match} where Balls={i+1} and innings='{innings}' and last_num_host is not null")
                                    myresult1=((mycursor.fetchall())[0])[0]
                                    mycursor.execute(f"select last_num_player from {match} where Balls={i+1} and innings='{innings}' and last_num_player is not null")
                                    myresult2=((mycursor.fetchall())[0])[0]
                                    if myresult1==myresult2:
                                        results2.append(myresult1)
                        except:
                            continue
                mycursor.execute("SELECT num from program_match_data")
                myresult = mycursor.fetchall()
                for num in myresult:
                    results1.append(num[0])
                results_1 = {}
                results_2 = {}
                for el in results1:
                    results_1[el]=results1.count(el)
                for el in results2:
                    results_2[el]=results2.count(el)
                del results1, results2
                all_keys = list(results_1.keys()) + list(results_2.keys())
                unique_keys = list(set(all_keys))
                values1 = [results_1.get(key, 0) for key in unique_keys]
                values2 = [results_2.get(key, 0) for key in unique_keys]
                bar_width = 0.5
                index = np.arange(len(unique_keys))

                plt.bar(index, values1, width=bar_width, label='Your dismissals')
                plt.bar(index + bar_width, values2, width=bar_width, label='Opponents dismissals')
                plt.xlabel('Number')
                plt.ylabel('No. of times')
                plt.title('How you got out and how you dismissed others')
                fig = pylab.gcf()
                fig.canvas.manager.set_window_title('Graphical comparison of dismissals')
                plt.xticks(index + bar_width/2, unique_keys)
                plt.legend()
                plt.tight_layout()
                plt.show()

        elif ch=="5":
            cls()
            if user_data==[]:
                print("You are logged in as a guest. Signup or login to delete your data in Odd-Even!")
            else:
                confirm = input("Menu (Select options by just entering the number)\n1. Delete your game data\n2. Delete your profile\n3. Go back")
                if confirm=="1":
                    mycursor.execute(f"DELETE FROM scoreboard where userID={user_data[0][0]}")
                    print("Deleted data successfully")
                    time.sleep(2)
                    cls()
                    continue
                elif confirm=="2":
                    mycursor.execute(f"DELETE FROM scoreboard where userID={user_data[0][0]}")
                    mycursor.execute(f"DELETE FROM users where userID={user_data[0][0]}")
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
            t = prettytable.PrettyTable(['Rank', 'Player', "Matches", "Wins", "Losses",'Points'])
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
    except:
        exit()