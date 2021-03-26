# exec(open('main.py').read())
# exec(open('race_game.py').read())

from subprocess import *
import time
Popen('python main.py')
# time.sleep(1)
Popen('python race_game.py')
