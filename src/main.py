from random import randint
from os import system, name 


openMap = open('map.txt', 'r')
map = list(openMap.read())
openMap.close()

# Key:
# _ : wall
# | : wall
# - : interactable
# @ : player
# ! : NPC
# # : enemy
# empty space : nothing
# % : stairs (leads the player up or down a level)

def clear(): 
  
    if name == 'nt': 
        system('cls') 
    else: 
        system('clear') 



def loop():
    global map
    
    for i in map:
        print(i, end="")
    print('\n' + str(map.index('@')))
    userInput = input('\nWhat are you going to do? ')
    beforeInput = map.index('@')
    print(len(map))
    
    if userInput.lower() == 'd':
        if map[beforeInput + 1] == '_' or map[beforeInput+1] == '|':
            input('You can\'t go that way! (Press any button to continue) ')
        else:    
            map[beforeInput + 1] = '@'
            map[beforeInput] = ' '
    elif userInput.lower() == 'a':
        if map[beforeInput-1] == '_' or map[beforeInput-1] == '|':
            input('You can\'t go that way! (Press any button to continue) ')
        else:    
            map[beforeInput-1] = '@'
            map[beforeInput] = ' '
    elif userInput.lower() == 'w':
        if map[beforeInput-map.index('\n')-1] == '_' or map[beforeInput-map.index('\n')-1] == '|':
            input('You can\'t go that way! (Press any button to continue) ')
        else:    
            map[beforeInput-map.index('\n')-1] = '@'
            map[beforeInput] = ' '
    elif userInput.lower() == 's':
        if map[beforeInput+map.index('\n')+1] == '_' or map[beforeInput+map.index('\n')+1] == '|':
            input('You can\'t go that way! (Press any button to continue) ')
        else:    
            map[beforeInput+map.index('\n')+1] = '@'
            map[beforeInput] = ' '
    
    
    clear()


while True:
    loop()