from random import randint, choice
from os import system, name
import monsters
import items
import traps
import magic

# get the first map
openMap = open('maps/map1.txt', 'r')
map = list(openMap.read())
openMap.close()

# define the player's stats
player = {'class': None, 'armorBonus': 0, 'xp':0, 'healthGain': 0, 'meleeBonus': 0, 'xpGoal': 20, 'rangedBonus': 0, 'hp': 10, 'mana':0, 'maxMana':0, 'maxHp':10, 'speed':7, 'actionsNum': 1, 'actions':{'atk': {'punch':5}, 'dodge':True, 'magic':{}}, 'level':1, 'gold':0, 'currentArmor':{'value':1}, 'currentWeapon':{}}
inventory = [items.healingPotion_1, items.torch] # the player's inventory
used = '(Press enter to continue) ' # this piece of text is used a LOT of times
floor = 1 # the floor that the player is on
light = 50 # the amount of light in the room
sneaking = False # if the player is sneaking
shopInventories = {} # a list of all the inventories of shops


# Key:
# _ : wall
# | : wall
# - : interactable
# @ : player
# $ : shop
# # : enemy
# ! : boss
# empty space : nothing
# % : stairs (leads the player up or down a level)


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
            player['actions']['magic']['magic missel'] = {'name': 'magic missel', 'mana': 10, 'value':10, 'type':'attack', 'reqCombat':'attack'}
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
def shop(location):
    global inventory
    global player
    global shopInventories
    
    # the shopkeepers inventory
    shopInventory = []
    
    if shopInventories[str(location)] == []:
        for i in range(0, floor*2):
            shopInventory.append(choice(items.listOfItemsByPower['1']))
    else:
        shopInventory = shopInventories[str(location)]
    
    while True:
        option = input('Would you like to buy or sell? Or type in "cancel" ')
        if option.lower() == 'sell':
            for i in inventory:
                print(i['name'] + ' cost: ' + str(int(round(i['price'] / 2))))
            
            sellOption = input('Which item would you like to sell? Or type in "cancel" ')
            
            try:
                inventory.remove(i)
                player['gold'] += int(round(i['price'] / 2))
                input('You sold a ' + i['name'] + ' for ' + str(int(round(i['price'] / 2))) + ' gold! ' + used)
                shopInventory.append(i)
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
    shopInventories[str(location)] = shopInventory


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
        player['actions']['magic'][magic.magicByLevel[str(player['level'])]['name']] = magic.magicByLevel[str(player['level'])]
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
                        elif i['type'] == 'mana':
                            if player['class'] == 'mage' and player['mana'] != player['maxMana']:
                                player['mana'] += i['value']
                                if player['mana'] > player['maxMana']:
                                    player['mana'] = player['maxMana']
                                usedItem = True
                            else:
                                input('You don\'t need a mana potion! ' + used)
                            
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
                        if player['actions']['magic'][theSpell]['type'] == 'attack' and player['mana'] >= player['actions']['magic'][theSpell]['mana']:
                            player['mana'] -= player['actions']['magic'][theSpell]['mana']
                            monster.stats['hp'] -= player['actions']['magic'][theSpell]['value']
                            input('You casted a ' + player['actions']['magic'][theSpell]['name'] + ' for ' + str(player['actions']['magic'][theSpell]['mana']) + ' and you did ' + str(player['actions']['magic'][theSpell]['value']) + ' damage! ' + used)
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
                        if player['actions']['magic'][theSpell]['type'] == 'attack' and player['mana'] >= player['actions']['magic'][theSpell]['mana']:
                            player['mana'] -= player['actions']['magic'][theSpell]['mana']
                            monster.stats['hp'] -= player['actions']['magic'][theSpell]['value']
                            input('You casted a ' + player['actions']['magic'][theSpell]['name'] + ' for ' + str(player['actions']['magic'][theSpell]['mana']) + ' and you did ' + str(player['actions']['magic'][theSpell]['value']) + ' damage! ' + used)
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
        
# the main game loop
def loop():
    global map
    global light
    global sneaking
    global shopInventories
    
    
    t = 0 # counter variable
    
    # while t is less then the amount of characters in the map ...
    while t < len(map):
        # ... then check for all of the '$' in the map ...
        if map[t] == '$':
            # ... for each '$' in the map make a inventory for them
            shopInventories[str(t)] = []
        t += 1 # increase t
    
    del t # delete t
    
    while True:
        beforeInput = map.index('@')
        
        # if light is not equal to 0...
        if light != 0:
            # then load the map and reveal what is near by to the player
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
        # otherwise...
        else:
            # load the map without revealing what is near to the player
            y = 0
            while y < len(map):
                if map[y] == '\n':
                    print('\n', end='')
                elif map[y] != '@':
                    print('.', end='')
                else:
                    print('@', end='')
                y+=1
        
        # load important player stats
        print('\nHP: ' +  str(player['hp']) + '/' + str(player['maxHp']))
        print('Light level: ' + str(light))
        print('Gold: ' + str(player['gold']))
        
        if player['class'] == 'mage':
            print('Mana: ' + str(player['mana']) + '/' + str(player['maxMana']))
        
        # if the player's xp is equal to or greater than to the player's xp goal then...
        if player['xp'] >= player['xpGoal']:
            # ... level up the player
            levelUp()
            input('You are now level ' + str(player['level']) + '! ' + used)
        
        userInput = input('What are you going to do? ') # ask the player what are the going to do
        
        # if the user input equals to 'd' then move the player right
        if userInput.lower() == 'd':
            # if there is a wall in the way
            if map[beforeInput + 1] == '_' or map[beforeInput+1] == '|':
                # don't allow the player to move
                input('You can\'t go that way!  ' + used )
            # otherwise...
            else:
                # if there is a fight in the space that the player wants to move to...
                if map[beforeInput+1] == '#':
                    # then fight...
                    if fight() == False:
                        # if the player dies then break the while true loop
                        break
                # if there is a boss in the way...
                elif map[beforeInput+1] == '!':
                    # then boss fight...
                    if fight(boss=True)==False:
                        # if the player dies then break the while true loop
                        break
                # if there is a interactable in the way...
                elif map[beforeInput+1] == '-':
                    # ... then interact with the object
                    interact()
                # if there is a shopkeeper in the way...
                elif map[beforeInput+1] == '$':
                    # then shop with the shop keeper...
                    shop(beforeInput+1)
            
            # if the space that the player tried to move to didn't have a shop keeper in it...
                if map[beforeInput+1] != '$':
                    # then move the player to the space they wanted to move to
                    map[beforeInput+1] = '@'
                    map[beforeInput] = ' '
        # if the user input equals 'a' then move the player left
        elif userInput.lower() == 'a':
            # if there is a wall in the way
            if map[beforeInput-1] == '_' or map[beforeInput-1] == '|':
                # don't allow the player to move
                input('You can\'t go that way!  ' + used )
            # otherwise...
            else:
                # if there is a fight in the space that the player wants to move to...
                if map[beforeInput-1] == '#':
                    # then fight...
                    if fight() == False:
                        # if the player dies then break the while true loop
                        break
                # if there is a boss in the way...
                elif map[beforeInput-1] == '!':
                    # then boss fight...
                    if fight(boss=True)==False:
                        # if the player dies then break the while true loop
                        break
                # if there is a interactable in the way...
                elif map[beforeInput-1] == '-':
                    # ... then interact with the object
                    interact()
            # if there is a shopkeeper in the way...
                elif map[beforeInput-1] == '$':
                    # then shop with the shop keeper...
                    shop(beforeInput-1)
                
                # if the space that the player tried to move to didn't have a shop keeper in it...
                if map[beforeInput-1] != '$':
                    # then move the player to the space they wanted to move to
                    map[beforeInput-1] = '@'
                    map[beforeInput] = ' '
        # if the user input equals 'w' then move the player up
        elif userInput.lower() == 'w':
            # if there is a wall in the way
            if map[beforeInput-map.index('\n')-1] == '_' or map[beforeInput-map.index('\n')-1] == '|':
                # don't allow the player to move
                input('You can\'t go that way!  ' + used )
            # otherwise...
            else:
                # if there is a fight in the space that the player wants to move to...
                if map[beforeInput-map.index('\n')-1] == '#':
                    # then fight...
                    if fight() == False:
                        # if the player dies then break the while true loop
                        break
                # if there is a boss in the way...
                elif map[beforeInput-map.index('\n')-1] == '!':
                    # then boss fight...
                    if fight(boss=True)==False:
                        # if the player dies then break the while true loop
                        break
                # if there is a interactable in the way...
                elif map[beforeInput-map.index('\n')-1] == '-':
                    # ... then interact with the object
                    interact()
                # if there is a shopkeeper in the way...
                elif map[beforeInput+map.index('\n')-1] == '$':
                    # then shop with the shop keeper...
                    shop(beforeInput+map.index('\n')-1)
                
                # if the space that the player tried to move to didn't have a shop keeper in it...
                if map[beforeInput-map.index('\n')-1] != '$':
                    # then move the player to the space they wanted to move to
                    map[beforeInput-map.index('\n')-1] = '@'
                    map[beforeInput] = ' '
        # if the user input equals 's' then...
        elif userInput.lower() == 's':
            # if there is a wall in the way
            if map[beforeInput+map.index('\n')+1] == '_' or map[beforeInput+map.index('\n')+1] == '|':
                # don't allow the player to move
                input('You can\'t go that way!  ' + used )
            # otherwise...
            else:
                # if there is a fight in the space that the player wants to move to...
                if map[beforeInput+map.index('\n')+1] == '#':
                    # then fight...
                    if fight() == False:
                        # if the player dies then break the while true loop
                        break
                # if there is a boss in the way...
                elif map[beforeInput+map.index('\n')+1] == '!':
                    # then boss fight...
                    if fight(boss=True)==False:
                        # if the player dies then break the while true loop
                        break
                # if there is a interactable in the way...
                elif map[beforeInput+map.index('\n')+1] == '-':
                    # ... then interact with the object
                    interact()
                # if there is a shopkeeper in the way...
                elif map[beforeInput+map.index('\n')+1] == '$':
                    # then shop with the shop keeper...
                    shop(beforeInput+map.index('\n')+1)
                
                # if the space that the player tried to move to didn't have a shop keeper in it...
                if map[beforeInput+map.index('\n')+1] != '$':
                    # then move the player to the space they wanted to move to
                    map[beforeInput+map.index('\n')+1] = '@'
                    map[beforeInput] = ' '
        # if the user input equals to 'exit' then exit the game
        elif userInput.lower() == 'exit':
            break
        # if the user input equals 'items' then look through the player's items
        elif userInput.lower() == 'items':
            lookInInventory()
        # if the user input equals 'sneak' then...
        elif userInput.lower() == 'sneak':
            # if the player's class is equal to a rouge...
            if player['class'] == 'rouge':
                # then allow the player to sneak
                input('You are now sneaking! ' + used)
                sneaking = True
            # otherwise...
            else:
                # prevent the player from sneaking
                input('You are not stealthy enough to be able to sneak!' + used)
        # if the user input is equal to 'magic' ...
        elif userInput.lower() == 'magic':
            # if the player's class is equal to mage...
            if player['class'] == 'mage':
                # ... then allow the player to cast magic
                for i in player['actions']['magic']:
                        print(player['actions']['magic'][i]['name'])
             
                userInput = input('Which spell would you like to cast? ')
                
                # try to cast a spell
                try:
                    if player['actions']['magic'][str(userInput)]['reqCombat'] == True:
                        input('You can\'t use that spell here! ' + used)
                    elif player['actions']['magic'][str(userInput)]['type'] == 'light':
                        light += player['actions']['magic'][str(userInput)]['value']
                        input('You casted a light spell and increased your light levels by ' + str(player['actions']['magic'][str(userInput)]['value']) + '! ' + used)
                # if the user input is invalid or is equals to a spell the user doesn't know
                except:
                    input('That isn\'t a spell you know! ' + used)
            # otherwise ...
            else:
                # ... inform the user that they can't cast magic
                input('You don\'t know how to cast magic! ' + used)
        # otherwise ...
        else:
            # tell the user that their input is invalid
            input('That is not an option! ' + used)

        
        # if the light is not equals to 0...
        if light != 0:
            # ... then lower the light level if the user wasn't looking through their items
            if userInput.lower() != 'items':
                light -= 1
        
        # if the user's health is lower than zero...
        if player['hp'] <= 0:
            # ... then break the game
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
