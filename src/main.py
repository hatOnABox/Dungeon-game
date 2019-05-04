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
        print('You are at ' + str(player['hp']) + ' hit points!')
        if monster.stats['speed'] >= player['speed']:
            i = 0
            while i < monster.stats['actionsNum']:  
                runAction = randint(0, actionsNum)
                currentAction = list(monster.stats['actions'])[runAction]
                if currentAction == 'atk':
                    if dodging == True and monster.stats['speed'] > player['speed']:
                        input('You\'re to slow to dodge the ' + monster.stats['name'] + '\'s attack! (Press enter to continue) ')
                    else:    
                        input('You dodge the ' + monster.stats['name'] + '\'s attack! (Press enter to continue) ')
                        dodging = False
                else:
                    runAttack = randint(0, attackNum)
                    currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                    player['hp'] -= monster.stats['actions']['atk'][currentAttack]
                    input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]) + ' damage! (Press enter to continue) ')
                i += 1
            

            if player['hp'] <= 0:
                input('YOU DIED!!! (Press enter to continue) ')
                return False


            action = input('What are you going to do? ')
            
            if action == 'atk':
                for i in list(player['actions']['atk']):
                    print(i)
                theAttack = input('Which attack? ')
                try:
                    monster.stats['hp'] -= player['actions']['atk'][theAttack]
                    input('You attack the ' + monster.stats['name'] + ' for ' + str(player['actions']['atk']['punch']) + ' damage! (Press enter to continue) ')
                except:
                    input('That\'s not an attack! (Press enter to continue) ')
            elif action == 'dodge':
                if checkKey(player['actions'], 'dodge') == True:        
                    dodging = True
                else:
                    input('You don\'t have the dodge action! (Press enter to continue) ')
            else:
                input('That\'s not an action! (Press enter to continue) ')
            
            if monster.stats['hp'] <= 0:
                monster.stats = monster.base
                input('You have defeated the ' + monster.stats['name'] + '! (Press enter to continue) ')
                return True
        else:
            action = input('What are you going to do? ')
            
            if action == 'atk':
                for i in list(player['actions']['atk']):
                    print(i)
                theAttack = input('Which attack? ')
                try:
                    monster.stats['hp'] -= player['actions']['atk'][theAttack]
                    input('You attack the ' + monster.stats['name'] + ' for ' + str(player['actions']['atk']['punch']) + ' damage! (Press enter to continue) ')
                except:
                    input('That\'s not an attack! (Press enter to continue) ')
            elif action == 'dodge':
                if checkKey(player['actions'], 'dodge') == True:        
                    dodging = True
                else:
                    input('You don\'t have the dodge action! (Press enter to continue) ')
            else:
                input('That\'s not an action! (Press enter to continue) ')
                
            
            if monster.stats['hp'] <= 0:
                monster.stats = monster.base
                input('You have defeated the ' + monster.stats['name'] + '! (Press enter to continue) ')
                return True

            i = 0
            while i < monster.stats['actionsNum']:  
                runAction = randint(0, actionsNum)
                currentAction = list(monster.stats['actions'])[runAction]
                if currentAction == 'atk':
                    if dodging == True:
                        if monster.stats['speed'] > player['speed']:
                            input('You\'re to slow to dodge the ' + monster.stats['name'] + '\'s attack! (Press enter to continue) ')
                        else:    
                            input('You dodge the ' + monster.stats['name'] + '\'s attack! (Press enter to continue) ')
                        dodging = False
                    else:
                        runAttack = randint(0, attackNum)
                        currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                        player['hp'] -= monster.stats['actions']['atk'][currentAttack]
                        input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]) + ' damage! (Press enter to continue) ')
                i += 1
            
            if player['hp'] <= 0:
                input('YOU DIED!!! (Press enter to continue) ')
                return False
        

def loop():
    global map
    
    while True:
        for i in map:
            print(i, end="")
        userInput = input('\nWhat are you going to do? ')
        beforeInput = map.index('@')

        
        if userInput.lower() == 'd':
            if map[beforeInput + 1] == '_' or map[beforeInput+1] == '|':
                input('You can\'t go that way! (Press enter to continue) ')
            else:
                if map[beforeInput + 1] == '#':
                    if fight() == False:
                        break
                map[beforeInput + 1] = '@'
                map[beforeInput] = ' '
        elif userInput.lower() == 'a':
            if map[beforeInput-1] == '_' or map[beforeInput-1] == '|':
                input('You can\'t go that way! (Press enter to continue) ')
            else:
                if map[beforeInput - 1] == '#':
                    if fight() == False:
                        break
                
                map[beforeInput-1] = '@'
                map[beforeInput] = ' '
        elif userInput.lower() == 'w':
            if map[beforeInput-map.index('\n')-1] == '_' or map[beforeInput-map.index('\n')-1] == '|':
                input('You can\'t go that way! (Press enter to continue) ')
            else:
                if map[beforeInput-map.index('\n')-1] == '#':
                    if fight() == False:
                        break
                
                map[beforeInput-map.index('\n')-1] = '@'
                map[beforeInput] = ' '
        elif userInput.lower() == 's':
            if map[beforeInput+map.index('\n')+1] == '_' or map[beforeInput+map.index('\n')+1] == '|':
                input('You can\'t go that way! (Press enter to continue) ')
            else:
                if map[beforeInput+map.index('\n')+1] == '#':
                    if fight() == False:
                        break
                map[beforeInput+map.index('\n')+1] = '@'
                map[beforeInput] = ' '
        else:
            input('That is not an option! (Press enter to continue) ')
        
        
        clear()


clear()
loop()