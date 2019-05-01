from random import randint
from os import system, name
import monsters


openMap = open('map.txt', 'r')
map = list(openMap.read())
openMap.close()
player = {'hp': 10, 'speed':5, 'actionsNum': 1, 'actions':{'atk': {'punch': 5}, 'dodge':True, 'run':5}, 'level':1}

# Key:
# _ : wall
# | : wall
# - : interactable
# @ : player
# ! : NPC
# # : enemy
# empty space : nothing
# % : stairs (leads the player up or down a level)
# * : door


def clear(): 
  
    if name == 'nt': 
        system('cls') 
    else: 
        system('clear') 


def fight():
    global player
    
    dodging = False
    monster = monsters.bat
    actionsNum = len(list(monster.stats['actions'])) - 1
    attackNum = len(list(monster.stats['actions']['atk'])) - 1
    
    input('A ' + monster.stats['name'] + ' attacks you! (press enter to continue) ')

    while True:
        clear()
        print(monster.stats['hp'])
        
        if monster.stats['speed'] >= player['speed']:
            i = 0
            while i < monster.stats['actionsNum']:  
                runAction = randint(0, actionsNum)
                currentAction = list(monster.stats['actions'])[runAction]
                if currentAction == 'atk':
                    runAttack = randint(0, attackNum)
                    currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                    player['hp'] -= monster.stats['actions']['atk'][currentAttack]
                    input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]) + ' damage! (Press enter to continue) ')
                i += 1
            dodging = False


            action = input('What are you going to do? ')
            
            if action == 'atk':
                monster.stats['hp'] -= player['actions']['atk']['punch']
            elif action == 'dodge':
                dodging = True
            
            if monster.stats['hp'] <= 0:
                monster.stats = monster.base
                return True
            elif player['hp'] <= 0:
                return False
        else:
            action = input('What are you going to do? ')
            
            if action == 'atk':
                monster.stats['hp'] -= player['actions']['atk']['punch']
            elif action == 'dodge':
                dodging = True
            
            if monster.stats['hp'] <= 0:
                monster.stats = monster.base
                return True
            elif player['hp'] <= 0:
                return False
            
            i = 0
            while i < monster.stats['actionsNum']:  
                runAction = randint(0, actionsNum)
                currentAction = list(monster.stats['actions'])[runAction]
                if currentAction == 'atk':
                    runAttack = randint(0, attackNum)
                    currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                    player['hp'] -= monster.stats['actions']['atk'][currentAttack]
                    input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]) + ' damage! (Press enter to continue) ')
                i += 1
            dodging = False
        
        
    


def loop():
    global map
    
    while True:
        for i in map:
            print(i, end="")
        userInput = input('\nWhat are you going to do? ')
        beforeInput = map.index('@')

        
        if userInput.lower() == 'd':
            if map[beforeInput + 1] == '_' or map[beforeInput+1] == '|':
                input('You can\'t go that way! (Press any button to continue) ')
            else:
                if map[beforeInput + 1] == '#':
                    if fight() == False:
                        break
                map[beforeInput + 1] = '@'
                map[beforeInput] = ' '
        elif userInput.lower() == 'a':
            if map[beforeInput-1] == '_' or map[beforeInput-1] == '|':
                input('You can\'t go that way! (Press any button to continue) ')
            else:
                if map[beforeInput - 1] == '#':
                    if fight() == False:
                        break
                
                map[beforeInput-1] = '@'
                map[beforeInput] = ' '
        elif userInput.lower() == 'w':
            if map[beforeInput-map.index('\n')-1] == '_' or map[beforeInput-map.index('\n')-1] == '|':
                input('You can\'t go that way! (Press any button to continue) ')
            else:
                if map[beforeInput-map.index('\n')-1] == '#':
                    if fight() == False:
                        break
                
                map[beforeInput-map.index('\n')-1] = '@'
                map[beforeInput] = ' '
        elif userInput.lower() == 's':
            if map[beforeInput+map.index('\n')+1] == '_' or map[beforeInput+map.index('\n')+1] == '|':
                input('You can\'t go that way! (Press any button to continue) ')
            else:
                if map[beforeInput+map.index('\n')+1] == '#':
                    if fight() == False:
                        break
                map[beforeInput+map.index('\n')+1] = '@'
                map[beforeInput] = ' '
        
        
        clear()


loop()