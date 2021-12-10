import curses 
import time
from random import randint
import os
from IPython.display import clear_output
from colorama import init
from colorama import Fore, Back, Style
import sqlite3

WINDOW_WIDTH = 120  # defining screen size
WINDOW_HEIGHT = 30 

def start():

    conn= sqlite3.connect('Highscore.db')  #create database and connect to it
    c= conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS highscores (
            player_score integer
            )""")

    c.execute("INSERT INTO highscores VALUES (:player_score)",
             {
                 'player_score': 0
           })

    c.execute("SELECT * FROM highscores")
    items= c.fetchall()
    highscore= items[0][0]
    conn.commit()
    conn.close()

    # check if snake touches border
    def checkBorder(y, x):
        if y == 0:
            return(True)
        if y == WINDOW_HEIGHT-1:
            return(True)
        if x == 0:
            return(True)
        if x == WINDOW_WIDTH -1:
            return(True)


    # allowing snake to pass through border and come out on the other side
    def powerBorder(y,x):
        if y == 0:
            snake.insert(0, (WINDOW_HEIGHT-2, x))
        if y == WINDOW_HEIGHT-1:
            snake.insert(0, (1, x))
        if x == 0:
            snake.insert(0, (y, WINDOW_WIDTH-2))
        if x == WINDOW_WIDTH -1:
            snake.insert(0, (y, 1))


    curses.initscr()
    win = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1)

    start= time.time()
    powers= False
    snake = [(4,5), (4, 4), (4, 3), (4, 2), (4,1)]
    food = (randint(1,WINDOW_HEIGHT-2), randint(1,WINDOW_WIDTH -2))
    pfood = ()

    win.addch(food[0], food[1], '#')

    score = 0

    ESC = 27
    key = curses.KEY_RIGHT
    while key != ESC:
        win.addstr(0, 2, 'SCORE ' + str(score) + ' ')
        win.addstr(0, 20, 'HIGHSCORE ' + str(highscore) + ' ')
        win.timeout(150 - (len(snake)) // 5 + len(snake)//10 % 120) # increase speed

        prev_key = key
        event = win.getch()
        key = event if event != -1 else prev_key

        if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
            key = prev_key
        else:
            key= key
        # calculate the next coordinates
        y = snake[0][0]
        x = snake[0][1]

        if key == curses.KEY_DOWN:
            y += 1
        if key == curses.KEY_UP:
            y -= 1
        if key == curses.KEY_LEFT:
            x -= 1
        if key == curses.KEY_RIGHT:
            x += 1

        snake.insert(0, (y, x))

        # check if powers are activated
        if powers == True:
            win.addstr(0, 70, ' POWERS ACTIVATED'+ ' ',curses.A_BOLD)
            end= time.time()
            powerBorder(y,x)
            if end - start > 40: #powers last for 40 seconds
                win.border(0)
                win.addstr(0, 70, '                 ')
                win.addstr(0, 70, '    NO POWERS' + ' ',curses.A_BOLD)
                powers = False

        else:
            check= checkBorder(y, x)
            if check == True:
                break

        # if snake runs over itself
        if snake[0] in snake[1:]: break

        if snake[0] == food:
            # eat the food
            score += 1
            food = ()
            while food == ():
                food = (randint(1,WINDOW_HEIGHT-3), randint(1,WINDOW_WIDTH -3))
                if food in snake:
                    food = ()
            win.addch(food[0], food[1], '#')

        elif snake[0] == pfood:
            # eat the pfood
            score +=2
            start= time.time()
            powers= True
            pfood = ()

        else:
            # move snake
            last = snake.pop()
            win.addch(last[0], last[1], ' ')

        if powers == True:
            win.addch(snake[0][0], snake[0][1], 'O',curses.A_BOLD)
        else:
            win.addch(snake[0][0], snake[0][1], 'O')

        if score%10==0 and score>1:
            while pfood == ():
                pfood = (randint(2,WINDOW_HEIGHT-3), randint(2,WINDOW_WIDTH -3))
                if pfood in snake:
                    pfood = ()
            win.addch(pfood[0], pfood[1], '@',curses.A_BOLD)
    curses.endwin()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + f"\n\n\n\n\n\n\t\t\t\t\t\t\t   Highscore = {highscore}")
    print(Fore.CYAN + f"\n\n\t\t\t\t\t\t\t  Final score = {score}")

    if score>highscore:
        conn= sqlite3.connect('Highscore.db')
        c= conn.cursor()
        c.execute("""DELETE FROM highscores """)
        c.execute("INSERT INTO highscores VALUES (:player_score)",
             {
                 'player_score': score
           })
        conn.commit()
        conn.close()

def main():
    init(autoreset=True)
    game= True
    while(game):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.BLUE + "\n\n\n\n\t\t\t\t\t\tWould you like to play SNEK BOI?")
        print(Fore.GREEN + "\n\t\t\t\t\t\t\t   YES" + Fore.BLUE + " OR" + Fore.RED + " NO")
        play= input()
        if play.lower() =='no':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.GREEN + "\n\n\n\n\n\t\t\t\t\t\t\tGoodbye!!!")
            game= False
        elif play.lower()== 'yes':
            start()
            print(Fore.GREEN + "\n\n\n\t\t\t\t\t\t\tThanks for playing\n")
            time.sleep(5)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.RED + '\n\n\n\n\n\t\t\t\t\t\tInvalid input! please try again\n')
            time.sleep(3)

if __name__ == "__main__":
    main()
