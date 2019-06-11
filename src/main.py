from random import randint, choice
from os import system, name
import monsters
import items
import traps


openMap = open('map.txt', 'r')
map = list(openMap.read())
openMap.close()
player = {'class': None, 'armorBonus': 0, 'xp':0, 'healthGain': 0, 'meleeBonus': 0, 'xpGoal': 20, 'rangedBonus': 0, 'hp': 10, 'mana':0, 'maxMana':0, 'maxHp':10, 'speed':7, 'actionsNum': 1, 'actions':{'atk': {'punch':5}, 'dodge':True, 'magic':{}}, 'level':1, 'gold':0, 'currentArmor':{'value':1}, 'currentWeapon':{}}
inventory = [items.healingPotion_1, items.torch]
used = '(Press enter to continue) '
floor = 1
light = 50
sneaking = False


# Key:
# _ : wall
# | : wall
# - : interactable
# @ : player
# $ : NPC
# # : enemy
# ! : boss
# empty space : nothing
# % : stairs (leads the player up or down a level)
# * : door

# clear the screen
def clear(): 
  
    if name == 'nt': 
        system('cls') 
    else: 
        system('clear')

# this function gets ran at the begining of the game. This function allows the player to chose their class
def choseClass():
    global player
    
    while True:
        print('Chose your class: Mage or Fighter or Rouge or Ranger')
        userInput = input('Chose your class... ')
        # once the user chooses their class then their stats get changed
        if userInput.lower() == 'mage':
            player['class'] = 'mage'
            player['actions']['magic']['magic missel'] = {'name': 'magic missel', 'mana': 10, 'dmg':10, 'value':'attack'}
            player['maxHp'] -= 2
            player['maxMana'] = 20
            player['mana'] = 20
            player['healthGain'] = 2
            break
        elif userInput.lower() == 'rouge':
            player['class'] = 'rouge'
            player['actions']['sneak'] = True
            player['healthGain'] = 3
            break
        elif userInput.lower() == 'fighter':
            player['class'] = 'fighter'
            player['maxHp'] += 5
            player['meleeBonus'] = 2
            player['healthgain'] = 5
            player['armorBonus'] = 2
            break
        elif userInput.lower() == 'ranger':
            player['class'] = 'ranger'
            player['maxHp'] += 2
            player['rangedBonus'] = 3
            player['healthGain'] = 2
            player['armorBonus'] = 1
            break
        else:
            # in case of invalid input
            input('That\'s not a class! ' + used)
            clear()
    player['hp'] = player['maxHp']
    clear()

# When the player encounters a shopkeeper
def shop():
    global inventory
    global player
    
    shopInventory = []
    for i in range(0, floor*2):
        shopInventory.append(choice(items.listOfItemsByPower['1']))
    
    while True:
        option = input('Would you like to buy or sell? Or type in "cancel" ')
        if option.lower() == 'sell':
            for i in inventory:
                print(i['name'] + ' cost: ' + str(i['price']))
            
            sellOption = input('Which item would you like to sell? ')
            
            try:
                inventory.remove(i)
                player['gold'] += int(round(i['price'] / 2))
                input('You sold a ' + i['name'] + ' for ' + str(int(round(i['price'] / 2))) + ' gold! ' + used)
            except:
                input('You don\'t have that item! ' + used)
        elif option.lower() == 'buy':
            for i in shopInventory:
                print(i['name'] + ' cost: ' + str(i['price']))
            
            buyOption = input('Which item would you like to buy? ')
            
            x = False
            for i in shopInventory:
                if i['name'] == buyOption.lower() and i['price'] <= player['gold']:
                    player['gold'] -= i['price']
                    inventory.append(i)
                    input('You have bought a ' + i['name'] + ' for ' + i['price'] + '! ' + used)
                    x = True
                    break
                elif i['name'] == buyOption.lower() and i['price'] > player['gold']:
                    input('You don\'t have enough money to buy a ' + i['name'] +'!' + used)
                    x = True
                    break
            
            if x == False:
                input('The vendor does not have that item! ' + used)
            
        elif option.lower() == 'cancel':
            break

# if the player comes across an interactable
def interact():
    global inventory
    
    eventGen = randint(1, 6) # use a random number generator to determine what is going to happen to the playyer
    # if the player gets a 1 then they fight
    if eventGen == 1:
        fight()
    # if the player get a 2 or 3 then they get a trap
    elif eventGen == 2 or eventGen == 3:
        trap = choice(traps.listOftraps[str(floor)])
        player['hp'] -= trap['dmg']
        input('Out of nowhere ' + trap['name'] + ' attacks you! You take ' + str(trap['dmg']) + ' damage!  ' + used )
        if player['hp'] <= 0:
            input('YOU DIED!!!  ' + used )
    # if the player gets a 4 or a 5 they get money
    elif eventGen == 4 or eventGen == 5:
        goldGained = randint(floor, floor*2)
        player['gold'] += goldGained
        input('You find a pot and you gain ' + str(goldGained) + ' gold!  ' + used )
    # if the player gets a 6 they get treasure
    elif eventGen == 6:
        itemGained = choice(items.listOfItemsByPower[str(floor)])
        inventory.append(itemGained)
        input('You found a chest and inside of the chest you found ' + itemGained['name'] + '!  ' + used )

# level up the player
def levelUp():
    global player
    
    player['xp'] -= player['xpGoal']
    player['level'] += 1
    player['xpGoal'] += 20
    
    if player['class'] == 'mage':
        player['maxMana'] += 5
        player['mana'] = player['maxMana']
        player['magic'][magic.magicByLevel[str(player['level'])]['name']] = magic.magicByLevel[str(player)]
    elif player['class'] == 'fighter':
        player['meleeBonus'] += 2
        player['armorBonus'] += 2
    elif player['class'] == 'ranger':
        player['rangedBonus'] += 2
        player['armorBonus'] += 1
    elif player['class'] == 'rouge':
        player['speed'] += 2
        
    
    player['maxHp'] = player['maxHp'] + player['healthGain']
    player['hp'] = player['maxHp']


# allows the player to look in their inventory
def lookInInventory():
    global light
    
    if inventory == []:
        input('You don\'t have any items!  ' + used )
    else:
        gotItem = False
        usedItem = False
        for i in inventory:
            print(i['name'])
        itemName = input('Type in an item\'s items name to use it or type in "cancel"  ' + used)
        if itemName.lower() != 'cancel':
            for i in inventory:
                if i['name'] == itemName.lower():
                    gotItem = True
                    if i['consumable'] == True:
                        if i['type'] == 'healing':
                            if player['hp'] == player['maxHp']:
                                input('You are already at your max hp!  ' + used )
                            else:
                                player['hp'] += i['value']
                                if player['hp'] > player['maxHp']:
                                    player['hp'] = player['maxHp']
                                usedItem = True
                        elif i['type'] == 'light':
                            if light == 200:
                                input('You already have enought light!  ' + used )
                            else:
                                light += i['value']
                                if light > 200:
                                    light = 200
                                usedItem = True
                            
                        if usedItem == True:
                            inventory.remove(i)
                            input('You used a ' + i['name'] + '!  ' + used )
                    
                    elif i['type'] == 'armor':
                        if i == player['currentArmor']:
                            input('You took of the ' + i['name'] + '.  ' + used )
                            player['currentArmor'] = {'value':0}
                        else:
                            player['currentArmor'] = i
                            player['currentArmor']['value'] += player['armorBonus']
                            input ('You equipped ' + i['name'] + '!  ' + used )
                    elif i['type'] == 'meleeWeapon' or i['type'] == 'rangedWeapon':
                        if i == player['currentWeapon']:
                            input('You have disarmed yourself  ' + used )
                            player['actions']['atk'].pop(i['name'])
                            player['currentWeapon'] = {}
                        else:
                            player['currentWeapon'] = i
                            input('You have armed yourself with a ' + i['name'] + '  ' + used )
                            if i['type'] == 'meleeWeapon':
                                player['actions']['atk'].update({i['name']: i['value'] + player['meleeBonus']})
                            elif i['type'] == 'rangedWeapon':
                                player['actions']['atk'].update({i['name']: i['value'] + player['rangedBonus']})
                    else:
                        input('The item you wanted to use it not a consumable!  ' + used )
                    break
            
            if gotItem == False:
                input('You don\'t have that item!  ' + used)



# when the player gets in a fight
def fight(boss=False):
    global player
    global sneaking
    
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
        input('A ' + monster.stats['name'] + ' attacks you!  ' + used )
    else:
        input('Something attacks you!  ' + used )

    while True:
        clear()
        print('You are at ' + str(player['hp']) + ' hit points!')
        
        if player['class'] == 'mage':
            print('You have ' + str(player['mana']) + ' mana!')
        if monster.stats['speed'] >= player['speed'] or light == 0:
            i = 0
            while i < monster.stats['actionsNum']:  
                runAction = randint(0, actionsNum)
                currentAction = list(monster.stats['actions'])[runAction]
                if currentAction == 'atk':
                    if dodging == True:
                        if dodging == True and monster.stats['speed'] > player['speed'] and dodgedLastTurn == False:
                            if light != 0:
                                input('You\'re to slow to dodge the ' + monster.stats['name'] + '\'s attack!  ' + used )
                            else:
                                input('You\'re to slow to dodge the monster\'s attack!  ' + used )
                            dodgedLastTurn = True
                            runAttack = randint(1, attackNum)
                            currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                            player['hp'] -= monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']
                            if light != 0:
                                input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]-player['value']) + ' damage!  ' + used )
                            else:
                                input('The monster makes a ' + currentAttack + ' attack and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']) + ' damage!  ' + used )
                        elif dodgedLastTurn == True:
                            input('You already dodged last turn! (Press enter to contimue) ')
                            dodgedLastTurn = False
                            runAttack = randint(1, attackNum)
                            currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                            player['hp'] -= monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']
                            if light != 0:    
                                input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' attack and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']) + ' damage!  ' + used )
                            else:
                                input('The monster makes a ' + currentAttack + ' attack and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']) + ' damage!  ' + used )
                        else:
                            if light != 0:
                                input('You dodge the ' + monster.stats['name'] + '\'s attack!  ' + used )
                            else:
                                input('You dodge the monster\'s attack!  ' + used )
                            dodgedLastTurn = True
                        dodging = False
                    else:
                        runAttack = randint(1, attackNum)
                        currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                        player['hp'] -=  monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']
                        if light != 0:
                            input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' attack and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']) + ' damage!  ' + used )
                        else:
                            input('The monster make a ' + currentAttack + ' attack and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']) + ' damage!  ' + used )
                i += 1
            

            if player['hp'] <= 0:
                input('YOU DIED!!!  ' + used )
                return False


            action = input('What are you going to do? ')
            
            if action.lower() == 'atk':
                
                for i in list(player['actions']['atk']):
                    print(i)
                theAttack = input('Which attack? ')
                try:
                    if sneaking == True and light != 0:
                        monster.stats['hp'] -= player['actions']['atk'][theAttack] * 2
                        input('Your sneak attack did ' + str(player['actions']['atk'][theAttack] * 2) + ' to the ' + monster.stats['name'] + '! ' + used)
                    elif light != 0:
                        monster.stats['hp'] -= player['actions']['atk'][theAttack]
                        input('You attack the ' + monster.stats['name'] + ' for ' + str(player['actions']['atk'][str(theAttack)]) + ' damage!  ' + used )   
                    else:
                        if randint(0, 1) == 1:
                            if sneaking == True:
                                monster.stats['hp'] -= player['actions']['atk'][theAttack] * 2
                                input('You sneak attack the monster for ' + str(player['actions']['atk'][str(theAttack)]) + ' damage! ' + used )
                            else:
                                monster.stats['hp'] -= player['actions']['atk'][theAttack]
                                input('You attack the monster for ' + str(player['actions']['atk'][str(theAttack)]) + ' damage! ' + used)    
                        else:
                            input('You attack helplessly in the dark! ' + used)
                except:
                    input('That\'s not an attack! ' + used)
                sneaking = False
            elif action.lower() == 'magic':
                if player['class'] == 'mage':
                    for i in player['actions']['magic']:
                        print(i)
                    
                    theSpell = input('Which spell? ')
                    
                    try:
                        if player['actions']['magic'][theSpell]['value'] == 'attack' and player['mana'] >= player['actions']['magic'][theSpell]['mana']:
                            player['mana'] -= player['actions']['magic'][theSpell]['mana']
                            monster.stats['hp'] -= player['actions']['magic'][theSpell]['dmg']
                            input('You casted a ' + player['actions']['magic'][theSpell]['name'] + ' for ' + str(player['actions']['magic'][theSpell]['mana']) + ' and you did ' + str(player['actions']['magic'][theSpell]['dmg']) + ' damage! ' + used)
                        else:
                            input('You either don\'t have enough mana to cast that spell or that spell can\'t be used right now! ' + used)
                    except:
                        input('That isn\'t a spell you know! ' + used)
                else:
                    input('You do not know any magic! ' + used)
            elif action.lower() == 'dodge':
                if 'dodge' in player['actions']:
                    dodging = True
                else:
                    input('You don\'t have the dodge action!  ' + used )
                    dodgedLastTurn = False
            elif action.lower() == 'items':
                lookInInventory()
            elif action.lower() == 'run':
                if player['speed'] > monster.stats['speed']:
                    input('You run away!  ' + used )
                    break
                elif boss == True:
                    input('You can\'t run away from a boss!  ' + used )
                else:
                    input('You\'re to slow to run away!  ' + used )
            else:
                input('That is not an option!  ' + used )
            
            if monster.stats['hp'] <= 0:
                input('You have defeated the ' + monster.stats['name'] + '!  ' + used )
                return True
        else:
            action = input('What are you going to do? ')
            
            if action.lower() == 'atk':
                for i in list(player['actions']['atk']):
                    print(i)
                theAttack = input('Which attack? ')
                try:
                    if sneaking == True and light != 0:
                        monster.stats['hp'] -= player['actions']['atk'][theAttack] * 2
                        input('Your sneak attack did ' + str(player['actions']['atk'][theAttack] * 2) + ' to the ' + monster.stats['name'] + '! ' + used)
                    elif light != 0:
                        monster.stats['hp'] -= player['actions']['atk'][theAttack]
                        input('You attack the ' + monster.stats['name'] + ' for ' + str(player['actions']['atk'][str(theAttack)]) + ' damage!  ' + used )    
                    else:
                        if randint(0, 1) == 1:
                            if sneaking == True:
                                monster.stats['hp'] -= player['actions']['atk'][theAttack] * 2
                                input('You sneak attack the monster for ' + str(player['actions']['atk'][str(theAttack)]) + ' damage! ' + used )
                            else:
                                monster.stats['hp'] -= player['actions']['atk'][theAttack]
                                input('You attack the monster for ' + str(player['actions']['atk'][str(theAttack)]) + ' damage! ' + used)      
                        else:
                            input('You attack helplessly in the dark! ' + used)
                except:
                    input('That\'s not an attack!  ' + used )
                sneaking = False
            elif action.lower() == 'dodge':
                if 'dodge' in player['actions']:     
                    dodging = True
                else:
                    input('You don\'t have the dodge action!  ' + used )
            elif action.lower() == 'run':
                if player['speed'] > monster.stats['speed']:
                    input('You run away!  ' + used )
                    break
                elif boss == True:
                    input('You can\'t run away from a boss!  ' + used )
                else:
                    input('You\'re to slow to run away!  ' + used )
            elif action.lower() == 'items':
                lookInInventory()
            elif action.lower() == 'magic':
                if player['class'] == 'mage':
                    for i in player['actions']['magic']:
                        print(i)
                    
                    theSpell = input('Which spell? ')
                    
                    try:
                        if player['actions']['magic'][theSpell]['value'] == 'attack' and player['mana'] >= player['actions']['magic'][theSpell]['mana']:
                            player['mana'] -= player['actions']['magic'][theSpell]['mana']
                            monster.stats['hp'] -= player['actions']['magic'][theSpell]['dmg']
                            input('You casted a ' + player['actions']['magic'][theSpell]['name'] + ' for ' + str(player['actions']['magic'][theSpell]['mana']) + ' and you did ' + str(player['actions']['magic'][theSpell]['dmg']) + ' damage! ' + used)
                        else:
                            input('You either don\'t have enough mana to cast that spell or that spell can\'t be used right now! ' + used)
                    except:
                        input('That isn\'t a spell you know! ' + used)   
                            
                else:
                    input('You do not know any magic! ' + used)
            else:
                input('That is not an option!  ' + used )
            
            if monster.stats['hp'] <= 0:
                input('You have defeated the ' + monster.stats['name'] + '!  ' + used )
                return True

            i = 0
            while i < monster.stats['actionsNum']:  
                runAction = randint(0, actionsNum)
                currentAction = list(monster.stats['actions'])[runAction]
                if currentAction == 'atk':
                    if dodging == True:
                        if dodging == True and monster.stats['speed'] > player['speed'] and dodgedLastTurn == False:
                            input('You\'re to slow to dodge the ' + monster.stats['name'] + '\'s attack!  ' + used )
                            dodgedLastTurn = True
                            runAttack = randint(1, attackNum)
                            currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                            monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']
                            input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']) + ' damage!  ' + used )
                        elif dodgedLastTurn == True:
                            input('You already dodged last turn! (Press enter to contimue) ')
                            dodgedLastTurn = False
                            runAttack = randint(1, attackNum)
                            currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                            player['hp'] -= monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']
                            input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']) + ' damage!  ' + used )
                        else:   
                            input('You dodge the ' + monster.stats['name'] + '\'s attack!  ' + used )
                            dodgedLastTurn = True
                        dodging = False
                    else:
                        runAttack = randint(1, attackNum)
                        currentAttack = list(monster.stats['actions']['atk'])[runAttack]
                        player['hp'] -= monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']
                        input('The ' + monster.stats['name'] + ' makes a ' + currentAttack + ' attack and hits you for ' + str(monster.stats['actions']['atk'][currentAttack]-player['currentArmor']['value']) + ' damage!  ' + used )
                i += 1
            
            if player['hp'] <= 0:
                input('YOU DIED!!!  ' + used )
                return False
        

def loop():
    global map
    global light
    global sneaking
    
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
        print('Gold: ' + str(player['gold']))
        userInput = input('What are you going to do? ')

        
        if player['xp'] >= player['xpGoal']:
            levelUp()
        elif userInput.lower() == 'd':
            if map[beforeInput + 1] == '_' or map[beforeInput+1] == '|':
                input('You can\'t go that way!  ' + used )
            else:
                if map[beforeInput+1] == '#':
                    if fight() == False:
                        break
                elif map[beforeInput-1] == '!':
                    if fight(boss=True)==False:
                        break
                elif map[beforeInput+1] == '-':
                    interact()
                    
                elif map[beforeInput+1] == '$':
                    shop()
                
                if map[beforeInput+1] != '$':
                    map[beforeInput+1] = '@'
                    map[beforeInput] = ' '
        elif userInput.lower() == 'a':
            if map[beforeInput-1] == '_' or map[beforeInput-1] == '|':
                input('You can\'t go that way!  ' + used )
            else:
                if map[beforeInput-1] == '#':
                    if fight() == False:
                        break
                elif map[beforeInput-1] == '!':
                    if fight(boss=True)==False:
                        break
                elif map[beforeInput-1] == '-':
                    interact()
                    
                elif map[beforeInput-1] == '$':
                    shop()
                
                if map[beforeInput-1] != '$':
                    map[beforeInput-1] = '@'
                    map[beforeInput] = ' '
        elif userInput.lower() == 'w':
            if map[beforeInput-map.index('\n')-1] == '_' or map[beforeInput-map.index('\n')-1] == '|':
                input('You can\'t go that way!  ' + used )
            else:
                if map[beforeInput-map.index('\n')-1] == '#':
                    if fight() == False:
                        break
                elif map[beforeInput-map.index('\n')-1] == '!':
                    if fight(boss=True)==False:
                        break
                elif map[beforeInput-map.index('\n')-1] == '-':
                    interact()
                
                elif map[beforeInput+map.index('\n')-1] == '$':
                    shop()
                
                if map[beforeInput-map.index('\n')-1] != '$':
                    map[beforeInput-map.index('\n')-1] = '@'
                    map[beforeInput] = ' '
        elif userInput.lower() == 's':
            if map[beforeInput+map.index('\n')+1] == '_' or map[beforeInput+map.index('\n')+1] == '|':
                input('You can\'t go that way!  ' + used )
            else:
                if map[beforeInput+map.index('\n')+1] == '#':
                    if fight() == False:
                        break
                elif map[beforeInput+map.index('\n')+1] == '!':
                    if fight(boss=True)==False:
                        break
                elif map[beforeInput+map.index('\n')+1] == '-':
                    interact()
                elif map[beforeInput+map.index('\n')+1] == '$':
                    shop()
                
                if map[beforeInput+map.index('\n')+1] != '$':
                    map[beforeInput+map.index('\n')+1] = '@'
                    map[beforeInput] = ' '
        elif userInput.lower() == 'exit':
            break
        elif userInput.lower() == 'items':
            lookInInventory()
        elif userInput.lower() == 'sneak':
            if player['class'] == 'rouge':
                input('You are now sneaking! ' + used)
                sneaking = True
            else:
                input('You are not stealthy enough to be able to sneak!' + used)
        else:
            input('That is not an option! ' + used)


        if light != 0:
            if userInput.lower() != 'items':
                light -= 1
        
        
        if player['hp'] <= 0:
            break
        clear()


if __name__ == '__main__':
    try:
        clear()
        choseClass()
        clear()
        loop()
        clear()
    except KeyboardInterrupt:
        clear()
