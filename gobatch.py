import os
import sys
import signal
import time



# while True:
# do
#     pid = fork();
#
#     if(pid == 1):
#
#
#     else
#
#
#
# done

def readFile():
    with open("fbatch.txt", "r") as f:
        array = []
        for line in f:
            line = line.rstrip()
            array.append(line.split(' '))

        return array


for commande in readFile():
    print(commande);
