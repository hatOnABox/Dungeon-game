from random import randint, choice
from os import system, name
import monsters
import items
import traps


openMap = open('map.txt', 'r')
map = list(openMap.read())
openMap.close()
player = {'hp': 10, 'maxHp':10, 'speed':7, 'actionsNum': 1, 'actions':{'atk': {'punch': 5}, 'dodge':True}, 'level':1, 'gold':0, 'currentArmor':{'value':1}, 'currentWeapon':{'value':1}}
inventory = [items.healingPotion_1, items.torch]
floor = 1
light = 50


# Key:
# _ : wall
# | : wall
# - : interactable
# @ : player
# ! : NPC
# # : enemy
# $ : boss
# empty space : nothing
# % : stairs (leads the player up or down a level)
# * : door


def clear(): 
  
    if name == 'nt': 
        system('cls') 
    else: 
        system('clear') 


def interact():
    global inventory
    
    eventGen = randint(1, 6)
    if eventGen == 1:
        fight()
    elif eventGen == 2 or eventGen == 3:
        trap = choice(traps.listOftraps[str(floor)])
        player['hp'] -= trap['dmg']
        input('Out of nowhere ' + trap['name'] + ' attacks you! You take ' + str(trap['dmg']) + ' damage! (Press enter to continue) ')
        if player['hp'] <= 0:
            input('YOU DIED!!! (Press enter to continue) ')
    elif eventGen == 4 or eventGen == 5:
        goldGained = randint(floor, floor*2)
        player['gold'] += goldGained
        input('You find a pot and you gain ' + str(goldGained) + ' gold! (Press enter to continue) ')
    elif eventGen == 6:
        itemGained = choice(items.listOfItemsByPower[str(floor)])
        inventory.append(itemGained)
        input('You found a chest and inside of the chest you found ' + itemGained['name'] + '! (Press enter to continue) ')


def lookInInventory():
    global light
    
    if inventory == []:
        input('You don\'t have any items! (Press enter to continue) ')
    else:
        gotItem = False
        usedItem = False
        for i in inventory:
            print(i['name'])
        itemName = input('Type in an item\'s items name to use it or type in "cancel" (Press enter to continue) ')
        if itemName.lower() != 'cancel':
            for i in inventory:
                if i['name'] == itemName.lower():
                    gotItem = True
                    if i['consumable'] == True:
                        if i['type'] == 'healing':
                            if player['hp'] == player['maxHp']:
                                input('You are already at your max hp! (Press enter to continue) ')
                            else:
                                player['hp'] += i['value']
                                if player['hp'] > player['maxHp']:
                                    player['hp'] = player['maxHp']
                                usedItem = True
                        elif i['type'] == 'light':
                            if light == 200:
                                input('You already have enought light! (Press enter to continue) ')
                            else:
                                light += i['value']
                                if light > 200:
                                    light = 200
                                usedItem = True
                            
                        if usedItem == True:
                            inventory.remove(i)
                            input('You used a ' + i['name'] + '! (Press enter to continue) ')
                    
                    elif i['type'] == 'armor':
                        if i == player['currentArmor']:
                            input('You took of the ' + i['name'] + '. (Press enter to continue) ')
                            player['currentArmor'] = {'value':1}
                        else:
                            player['currentArmor'] = i
                            input ('You equipped ' + i['name'] + '! (Press enter to continue) ')
                    else:
                        input('The item you wanted to use it not a consumable! (Press enter to continue) ')
                    break
            
            if gotItem == False:
                input('You don\'t have that item! (Press enter to continue) ' )




def fight(boss=False):
    global player
    
    boss = False
    
    dodging = False
    if boss == True:
        boss = True
        monster=choice(monsters.listOfBosses[str(floor)])
    else:
        monster = choice(monsters.listOfMonsters[str(floor)])
    
    monster.stats['hp'] = randint(monster.baseHp, 2 * (floor + monster.baseHp))
    actionsNum = len(list(monster.stats['actions'])) - 1
    attackNum = len(list(monster.stats['actions']['atk'])) - 1
    dodgedLastTurn = False
    
    if light != 0:
        input('A ' + monster.stats['name'] + ' attacks you! (press enter to continue) ')
    else:
        input('Something attacks you! (Press enter to continue) ')

    while True:
        clear()
        print('You are at ' + str(player['hp']) + ' hit points!')
        if monster.stats['speed'] >= player['speed'] or light == 0:
            i = 0
            while i < monster.stats['actionsNum']:  
                runAction = randint(0, actionsNum)
                currentAction = list(monster.stats['actions'])[runAction]
                if currentAction == 'atk':
                    if dodging == True:
                        if dodging == True and monster.stats['speed'] > player['speed'] and dodgedLastTurn == False:
                            if light != 0:
                                input('You\'re to slow to dodge the ' + monster.stats['name'] + '\'s attack! (Press enter to continue) ')
                            else:
                                input('You\'re to slow to dodge the monster\'s attack! (Press enter to continue) ')
                            dodgedLastTurn = True
                            runAttack = randint(1, attackNum)
                            currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                            player['hp'] -= monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']
                            if light != 0:
                                input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]/player['value']) + ' damage! (Press enter to continue) ')
                            else:
                                input('The monster makes a ' + currentAttack + ' attack and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']) + ' damage! (Press enter to continue) ')
                        elif dodgedLastTurn == True:
                            input('You already dodged last turn! (Press enter to contimue) ')
                            dodgedLastTurn = False
                            runAttack = randint(1, attackNum)
                            currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                            player['hp'] -= monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']
                            if light != 0:    
                                input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' attack and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']) + ' damage! (Press enter to continue) ')
                            else:
                                input('The monster makes a ' + currentAttack + ' attack and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']) + ' damage! (Press enter to continue) ')
                        else:
                            if light != 0:
                                input('You dodge the ' + monster.stats['name'] + '\'s attack! (Press enter to continue) ')
                            else:
                                input('You dodge the monster\'s attack! (Press enter to continue) ')
                            dodgedLastTurn = True
                        dodging = False
                    else:
                        runAttack = randint(1, attackNum)
                        currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                        player['hp'] -=  monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']
                        if light != 0:
                            input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' attack and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']) + ' damage! (Press enter to continue) ')
                        else:
                            input('The monster make a ' + currentAttack + ' attack and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']) + ' damage! (Press enter to continue) ')
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
                    if light != 0:
                        input('You attack the ' + monster.stats['name'] + ' for ' + str(player['actions']['atk']['punch']) + ' damage! (Press enter to continue) ')
                    else:
                        if randint(0, 1) == 1:
                            input('You attack the monster for ' + str(player['actions']['atk']['punch']) + ' damage! (Press enter to continue) ')
                        else:
                            input('You attack helplessly in the dark! (Press enter to continue) ')
                except:
                    input('That\'s not an attack! (Press enter to continue) ')
            elif action == 'dodge':
                if 'dodge' in player['actions']:
                    dodging = True
                else:
                    input('You don\'t have the dodge action! (Press enter to continue) ')
                    dodgedLastTurn = False
            elif action == 'items':
                lookInInventory()
            elif action == 'run':
                if player['speed'] > monster.stats['speed']:
                    input('You run away! (Press enter to continue) ')
                    break
                elif boss == True:
                    input('You can\'t run away from a boss! (Press enter to continue) ')
                else:
                    input('You\'re to slow to run away! (Press enter to continue) ')
            else:
                input('That is not an option! (Press enter to continue) ')
            
            if monster.stats['hp'] <= 0:
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
                    if light != 0:
                        input('You attack the ' + monster.stats['name'] + ' for ' + str(player['actions']['atk']['punch']) + ' damage! (Press enter to continue) ')
                    else:
                        if randint(0, 1) == 1:
                            input('You attack the monster for ' + str(player['actions']['atk']['punch']) + ' damage! (Press enter to continue) ')
                        else:
                            input('You attack helplessly in the dark! (Press enter to continue) ')
                except:
                    input('That\'s not an attack! (Press enter to continue) ')
            elif action == 'dodge':
                if 'dodge' in player['actions']:     
                    dodging = True
                else:
                    input('You don\'t have the dodge action! (Press enter to continue) ')
            elif action == 'run':
                if player['speed'] > monster.stats['speed']:
                    input('You run away! (Press enter to continue) ')
                    break
                elif boss == True:
                    input('You can\'t run away from a boss! (Press enter to continue) ')
                else:
                    input('You\'re to slow to run away! (Press enter to continue) ')
            elif action == 'items':
                lookInInventory()
            else:
                input('That is not an option! (Press enter to continue) ')
            
            if monster.stats['hp'] <= 0:
                input('You have defeated the ' + monster.stats['name'] + '! (Press enter to continue) ')
                return True

            i = 0
            while i < monster.stats['actionsNum']:  
                runAction = randint(0, actionsNum)
                currentAction = list(monster.stats['actions'])[runAction]
                if currentAction == 'atk':
                    if dodging == True:
                        if dodging == True and monster.stats['speed'] > player['speed'] and dodgedLastTurn == False:
                            input('You\'re to slow to dodge the ' + monster.stats['name'] + '\'s attack! (Press enter to continue) ')
                            dodgedLastTurn = True
                            runAttack = randint(1, attackNum)
                            currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                            monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']
                            input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']) + ' damage! (Press enter to continue) ')
                        elif dodgedLastTurn == True:
                            input('You already dodged last turn! (Press enter to contimue) ')
                            dodgedLastTurn = False
                            runAttack = randint(1, attackNum)
                            currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                            player['hp'] -= monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']
                            input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']) + ' damage! (Press enter to continue) ')
                        else:   
                            input('You dodge the ' + monster.stats['name'] + '\'s attack! (Press enter to continue) ')
                            dodgedLastTurn = True
                        dodging = False
                    else:
                        runAttack = randint(1, attackNum)
                        currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                        player['hp'] -= monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']
                        input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' attack and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]/player['currentArmor']['value']) + ' damage! (Press enter to continue) ')
                i += 1
            
            if player['hp'] <= 0:
                input('YOU DIED!!! (Press enter to continue) ')
                return False
        

def loop():
    global map
    global light
    
    while True:
        beforeInput = map.index('@')
        
        if light != 0:
            y = 0
            while y < len(map):
                if y == beforeInput + 1 or y == beforeInput - 1 or y == beforeInput-map.index('\n')-1 or y == beforeInput+map.index('\n')+1 or y == beforeInput+map.index('\n') or y == beforeInput+map.index('\n')+2 or y == beforeInput-map.index('\n') or y == beforeInput-map.index('\n')-2:
                    print(map[y], end='')
                elif map[y] == '\n':
                    print('\n', end='')
                elif map[y] == '@':
                    print('@', end='')
                else:
                    print('.', end='')
                y+=1
        else:
            y = 0
            while y < len(map):
                if map[y] == '\n':
                    print('\n', end='')
                elif map[y] != '@':
                    print('.', end='')
                else:
                    print('@', end='')
                y+=1
        
        print('\nHP: ' + str(player['hp']))
        print('Light level: ' + str(light))
        userInput = input('What are you going to do? ')

        
        if userInput.lower() == 'd':
            if map[beforeInput + 1] == '_' or map[beforeInput+1] == '|':
                input('You can\'t go that way! (Press enter to continue) ')
            else:
                if map[beforeInput+1] == '#':
                    if fight() == False:
                        break
                elif map[beforeInput-1] == '$':
                    if fight(boss=True)==False:
                        break
                elif map[beforeInput+1] == '-':
                    interact()
                    
                map[beforeInput + 1] = '@'
                map[beforeInput] = ' '
        elif userInput.lower() == 'a':
            if map[beforeInput-1] == '_' or map[beforeInput-1] == '|':
                input('You can\'t go that way! (Press enter to continue) ')
            else:
                if map[beforeInput-1] == '#':
                    if fight() == False:
                        break
                elif map[beforeInput-1] == '$':
                    if fight(boss=True)==False:
                        break
                elif map[beforeInput-1] == '-':
                    interact()
                    
                map[beforeInput-1] = '@'
                map[beforeInput] = ' '
        elif userInput.lower() == 'w':
            if map[beforeInput-map.index('\n')-1] == '_' or map[beforeInput-map.index('\n')-1] == '|':
                input('You can\'t go that way! (Press enter to continue) ')
            else:
                if map[beforeInput-map.index('\n')-1] == '#':
                    if fight() == False:
                        break
                elif map[beforeInput-map.index('\n')-1] == '$':
                    if fight(boss=True)==False:
                        break
                elif map[beforeInput-map.index('\n')-1] == '-':
                    interact()
                
                map[beforeInput-map.index('\n')-1] = '@'
                map[beforeInput] = ' '
        elif userInput.lower() == 's':
            if map[beforeInput+map.index('\n')+1] == '_' or map[beforeInput+map.index('\n')+1] == '|':
                input('You can\'t go that way! (Press enter to continue) ')
            else:
                if map[beforeInput+map.index('\n')+1] == '#':
                    if fight() == False:
                        break
                elif map[beforeInput+map.index('\n')+1] == '$':
                    if fight(boss=True)==False:
                        break
                elif map[beforeInput+map.index('\n')+1] == '-':
                    interact()
                
                map[beforeInput+map.index('\n')+1] = '@'
                map[beforeInput] = ' '
        elif userInput.lower() == 'exit':
            break
        elif userInput.lower() == 'items':
            lookInInventory()
        # elif userInput.lower() == 'equip':
        #     for 
        else:
            input('That is not an option! (Press enter to continue) ')


        if light != 0:
            if userInput.lower() != 'items':
                light -= 1
        
        
        if player['hp'] <= 0:
            break
        clear()


clear()
loop()
clear()