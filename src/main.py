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
player = {'class': None, 'armorBonus': 0, 'xp':0, 'healthGain': 0, 'meleeBonus': 0, 'xpGoal': 20, 'rangedBonus': 0, 'hp': 10, 'mana':0, 'maxMana':0, 'maxHp':10, 'speed':7, 'actionsNum': 1, 'actions':{'atk':{'punch':5}, 'dodge':True, 'magic':{}}, 'level':1, 'gold':0, 'currentArmor':{'name':'unarmored', 'value':0}, 'currentWeapon':{'name':'none', 'value':0, 'type':'fist'}}
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
            inventory.append(items.manaPotion_1)
            break
        elif userInput.lower() == 'rouge':
            player['class'] = 'rouge'
            player['actions']['sneak'] = True
            player['healthGain'] = 2
            player['speed'] += 2
            player['maxHp'] += 1
            break
        elif userInput.lower() == 'fighter':
            player['class'] = 'fighter'
            player['maxHp'] += 5
            player['meleeBonus'] = 2
            player['healthgain'] = 5
            player['armorBonus'] = 1
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
    
    # if there is no saved data about the shop ...
    if shopInventories[str(location)] == []:
        # ... then add random items to the shop
        for i in range(0, floor*2):
            shopInventory.append(choice(items.listOfItemsByPower[str(floor)]))
    # otherwise ...
    else:
        # ... get the shop's inventory
        shopInventory = shopInventories[str(location)]
    
    while True:
        # ask the user what they would like to do
        option = input('Would you like to buy or sell? Or type in "cancel" ')
        
        # if the user types in 'sell' ...
        if option.lower() == 'sell':
            # ... then list out all the items in the player's inventory
            for i in inventory:
                print(i['name'] + ' cost: ' + str(int(round(i['price'] / 2))))
            
            # ... ask the user which items they would like to sell
            sellOption = input('Which item would you like to sell? ')
            
            itemToSell = {}
            
            # ... get every item in the player's inventory again
            for i in inventory:
                # ... if i's name is equals to the sellOption variable ...
                if i['name'] == sellOption:
                    # ... then assign itemToSell to i
                    itemToSell = i
            
            # ... if itemToSell is not equals to an empty dict ...
            if itemToSell != {}:
                # ... then remove the item from the player's inventory, give the player the correct 
                # amount of gold, and add the item to the shopkeepers inventory
                inventory.remove(itemToSell)
                player['gold'] += int(round(itemToSell['price'] / 2))
                input('You sold a ' + itemToSell['name'] + ' for ' + str(int(round(itemToSell['price'] / 2))) + ' gold! ' + used)
                shopInventory.append(itemToSell)
            # ... otherwise ...
            else:
                # ... inform the player that they don't have the item they typed in
                input('You don\'t have that item! ' + used)
        # if the player types in 'buy' ...
        elif option.lower() == 'buy':
            # ... print out the shop's inventory
            for i in shopInventory:
                print(i['name'] + ' cost: ' + str(i['price']))
            
            # ... ask the user which items they would like to buy
            buyOption = input('Which item would you like to buy? ')
            
            x = False # used to determine if the item that the player is looking for is in the shop
            
            # ... loop through the entire shop's inventory
            for i in shopInventory:
                # ... if the item's name is equal to the buyOption var and the player has enough
                # gold to buy said item ...
                if i['name'] == buyOption.lower() and i['price'] <= player['gold']:
                    # ... then add the item to the player's inventory and subtract the player's gold 
                    # by the price of the item
                    player['gold'] -= i['price']
                    inventory.append(i)
                    input('You have bought a ' + i['name'] + ' for ' + i['price'] + '! ' + used)
                    x = True
                # ... if the player doesn't have enough gold to buy the item but the vendor does 
                # have the item they are looking for...
                elif i['name'] == buyOption.lower() and i['price'] > player['gold']:
                    # ... inform the player they do not have enough money to buy the item they 
                    # are looking for
                    input('You don\'t have enough money to buy a ' + i['name'] +'!' + used)
                    x = True
            
            # ... if the item doesn't exist ...
            if x == False:
                # ... inform the player that the shopkeeper doesn't have the item they are 
                # looking for
                input('The vendor does not have that item! ' + used)
            clear()
        
        # if the user types in cancel ...    
        elif option.lower() == 'cancel':
            # ... then exit the shop
            break
    shopInventories[str(location)] = shopInventory # store the shop's inventory


# if the player comes across an interactable
def interact():
    global inventory
    
    eventGen = randint(1, 6) # use a random number generator to determine what is going to happen to the playyer
    # if the player gets a 1 then they fight
    if eventGen == 1:
        newFight = fight()
        if newFight == 'ran':
            return 'ran'
    # if the player get a 2 or 3 then they get a trap
    elif eventGen == 2 or eventGen == 3:
        trap = choice(traps.listOftraps[str(floor)])
        player['hp'] -= (trap['dmg'] - player['currentArmor']['value'])
        input('Out of nowhere ' + trap['name'] + ' attacks you! You take ' + str(trap['dmg'] - player['currentArmor']['value']) + ' damage!  ' + used )
        if player['hp'] <= 0:
            input('YOU DIED!!!  ' + used )
    # if the player gets a 4 or a 5 they get money
    elif eventGen == 4 or eventGen == 5:
        goldGained = randint(floor, floor*2)
        player['gold'] += goldGained
        input('You find a pot and you gain ' + str(goldGained) + ' gold!  ' + used )
    # if the player gets a 6 they get treasure
    elif eventGen == 6:
        if floor != 1:
            itemGained = choice(items.listOfItemsByPower[str(randint(floor-1, floor))])
        else:
            itemGained = choice(items.listOfItemsByPower['1'])
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
        player['meleeBonus'] += 1
        
    
    player['maxHp'] = player['maxHp'] + player['healthGain']
    player['hp'] = player['maxHp']


# allows the player to look in their inventory
def lookInInventory():
    global light
    
    # if the player's inventory is empty ...
    if inventory == []:
        # ... then inform the player that they don't have any items
        input('You don\'t have any items!  ' + used )
    # otherwise ...
    else:
        # create variables that are used for conditional statements later on
        gotItem = False
        usedItem = False
        
        # loop through the player's inventory and print the name of each item they have
        for i in inventory:
            print(i['name'])
        
        # ask the user what item would they like to use
        itemName = input('Type in an item\'s items name to use it or type in "cancel"  ' + used)
        
        # if the user input is not equals to 'cancel' ...
        if itemName.lower() != 'cancel':
            # ... loop through the player's inventory
            for i in inventory:
                # ... if i's 'name' attribute is equals to the user input ...
                if i['name'] == itemName.lower():
                    gotItem = True # ... this is telling the program that the player got the item
                    
                    # ... if the item is a consumable ...
                    if i['consumable'] == True:
                        
                        # ... if the item is a healing item...
                        if i['type'] == 'healing':
                            # ... if the player is as full health ...
                            if player['hp'] == player['maxHp']:
                                # ... tell the player that they are full on health and prevent them
                                # from using an item
                                input('You are already at your max hp!  ' + used )
                            # ... otherwise...
                            else:
                                # ... increase the player's health by the healing value of the item
                                player['hp'] += i['value']
                                
                                # ... if the player's health is greater than their max health ...
                                if player['hp'] > player['maxHp']:
                                    # ... then change the player's health so that it is equals to
                                    # player's max health
                                    player['hp'] = player['maxHp']

                                usedItem = True # ... tells the program that the player used an item
                        # ... if the item is a light item ...
                        elif i['type'] == 'light':
                            # ... if the light level is already at it's max ...
                            if light == 200:
                                # ... then inform the player that they are already at max light
                                input('You already have enought light!  ' + used )
                            # ... otherwise ...
                            else:
                                # ... increase the player's light level
                                light += i['value']
                                
                                # ... if the light level is greater than 200 ...
                                if light > 200:
                                    # ... then lower it back to 200
                                    light = 200
                                usedItem = True # ... tells program that the player used an item
                        # ... if the item is a mana item ...
                        elif i['type'] == 'mana':
                            # ... if the player is a mage ...
                            if player['class'] == 'mage' and player['mana'] != player['maxMana']:
                                # ... then increase the player's mana
                                player['mana'] += i['value']
                                # ... if the player's mana is greater than the player's max mana ...
                                if player['mana'] > player['maxMana']:
                                    # ... then lower the player's mana back to it's max
                                    player['mana'] = player['maxMana']
                                usedItem = True # ... tells program that the player used an item
                            # ... otherwise ...
                            else:
                                # ... inform the player that they don't need to use a mana 
                                # restoring item
                                input('You don\'t that item! ' + used)
                        
                        # ... if the player used an item ...
                        if usedItem == True:
                            # ... then remove the item from the player's inventory ...
                            inventory.remove(i)
                            input('You used a ' + i['name'] + '!  ' + used )
                    
                    # ... if the item is a piece of armor ...
                    elif i['type'] == 'armor':
                        # ... if the item is the player's current armor
                        if i == player['currentArmor']:
                            # ... then dequip the item
                            input('You took of the ' + i['name'] + '.  ' + used )
                            player['currentArmor'] = {'armor': 'unarmored', 'value':0}
                        # ... otherwise ...
                        else:
                            # ... equip the piece of armor
                            player['currentArmor'] = i
                            player['currentArmor']['value'] += player['armorBonus']
                            input('You equipped ' + i['name'] + '!  ' + used )
                    # ... if the item is a weapon ...
                    elif i['type'] == 'meleeWeapon' or i['type'] == 'rangedWeapon':
                        # ... if the item is the current item that the player is wearing ...
                        if i == player['currentWeapon']:
                            # ... then dequip the item
                            input('You have disarmed yourself  ' + used )
                            player['actions']['atk'].pop(i['name'])
                            player['currentWeapon'] = {}
                        # ... otherwise ...
                        else:
                            # ... equip the item
                            player['currentWeapon'] = i
                            input('You have armed yourself with a ' + i['name'] + '! ' + used )
                            
                            # ... apply ranged and melee weapon bonuses
                            if i['type'] == 'meleeWeapon':
                                player['actions']['atk'].update({i['name']: i['value'] + player['meleeBonus']})
                            elif i['type'] == 'rangedWeapon':
                                player['actions']['atk'].update({i['name']: i['value'] + player['rangedBonus']})
                    # ... if the item is a staff ...
                    elif i['type'] == 'staff':
                        # ... if the item is the current item that the player is wearing ...
                        if i == player['currentWeapon']:
                            # ... then dequip the item
                            input('You have disarmed yourself  ' + used )
                            player['actions']['atk'].pop(i['name'])
                            player['currentWeapon'] = {}
                        # ... otherwise ...
                        else:
                            # ... equip the item
                            player['currentWeapon'] = i
                            input('You have armed yourself with a ' + i['name'] + '! ' + used )
                            
                    # ... otherwise ...
                    else:
                        # ... inform the player that they item they typed in isn't a consumable
                        input('The item you wanted to use it not a consumable!  ' + used )
                    break
            # ... if the player doesn't have the item they typed in ...
            if gotItem == False:
                # ... inform the player they don't have it ...
                input('You don\'t have that item!  ' + used)



# when the player gets in a fight
def fight(boss=False):
    global player
    global sneaking
    global light
    
    
    dodging = False
    monsterDodging = False
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
        if monster.stats['speed'] >= player['speed'] or light == 0:
            i = 0
            while i < monster.stats['actionsNum']:  
                runAction = randint(0, actionsNum)
                currentAction = list(monster.stats['actions'])[runAction]
                if currentAction == 'atk':
                    if dodging == True or sneaking == True:
                        if dodging == True and monster.stats['speed'] > player['speed'] and dodgedLastTurn == False and sneaking == False:
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
                elif currentAction == 'dodge':
                    monsterDodging = True
                    dodging = False
                i += 1
            

            if player['hp'] <= 0:
                input('YOU DIED!!!  ' + used )
                return False

            print('You are at ' + str(player['hp']) + ' hit points!')
            
            if player['class'] == 'mage':
                print('You have ' + str(player['mana']) + ' mana!')
            
            action = input('What are you going to do? ')
            
            if action.lower() == 'atk':
                if monsterDodging != True or monster.stats['speed'] > player['speed']:
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
                else:
                    input('The monster dodged your attack! ' + used)
                    sneaking = False
                    monsterDodging = False
            elif action.lower() == 'magic':
                if player['class'] == 'mage':
                    for i in player['actions']['magic']:
                        print(i)
                    
                    theSpell = input('Which spell? ')
                    
                    try:
                        if player['currentWeapon']['type'] == 'staff':
                            if player['mana'] >= player['actions']['magic'][theSpell]['mana'] - player['currentWeapon']['manaReduced']:
                                player['mana'] -= (player['actions']['magic'][theSpell]['mana'] - player['currentWeapon']['manaReduced'])
                                
                                if player['actions']['magic'][theSpell]['type'] == 'light':
                                    light += player['actions']['magic'][theSpell]['value']
                                    if light > 200:
                                        light = 200
                                    input('You casted a light spell and increased the light level by ' + str(player['actions']['magic'][theSpell]['value']) + '! ' + used)
                                elif player['actions']['magic'][theSpell]['type'] == 'attack':
                                    monster.stats['hp'] -= player['actions']['magic'][theSpell]['value']
                                    input('You casted a ' + player['actions']['magic'][theSpell]['name'] + ' for ' + str(player['actions']['magic'][theSpell]['mana'] - player['currentWeapon']['manaReduced']) + ' and you did ' + str(player['actions']['magic'][theSpell]['value']) + ' damage! ' + used)
                            else:
                                input('You don\'t have enough mana to cast that spell! ' + used)
                        else:
                            if player['mana'] >= player['actions']['magic'][theSpell]['mana']:
                                player['mana'] -= player['actions']['magic'][theSpell]['mana']
                                
                                if player['actions']['magic'][theSpell]['type'] == 'light':
                                    light += player['actions']['magic'][theSpell]['value']
                                    if light > 200:
                                        light = 200
                                    input('You casted a light spell and increased the light level by ' + str(player['actions']['magic'][theSpell]['value']) + '! ' + used)
                                elif player['actions']['magic'][theSpell]['type'] == 'attack':
                                    monster.stats['hp'] -= player['actions']['magic'][theSpell]['value']
                                    input('You casted a ' + player['actions']['magic'][theSpell]['name'] + ' for ' + str(player['actions']['magic'][theSpell]['mana']) + ' and you did ' + str(player['actions']['magic'][theSpell]['value']) + ' damage! ' + used)
                            else:
                                input('You don\'t have enough mana to cast that spell! ' + used)
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
                    return 'ran'
                elif boss == True:
                    input('You can\'t run away from a boss!  ' + used )
                else:
                    input('You\'re to slow to run away!  ' + used )
            else:
                input('That is not an option!  ' + used )
            
            if monster.stats['hp'] <= 0:
                input('You have defeated the ' + monster.stats['name'] + '!  ' + used )
                player['xp'] += monster.stats['xpGain']
                return True
        else:
            print('You are at ' + str(player['hp']) + ' hit points!')
            
            if player['class'] == 'mage':
                print('You have ' + str(player['mana']) + ' mana!')
            
            action = input('What are you going to do? ')
            
            if action.lower() == 'atk':
                if monsterDodging != True or monster.stats['speed'] > player['speed']:
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
                else:
                    input('The monster dodged your attack! ' + used)
                    sneaking = False
                    monsterDodging = False
            elif action.lower() == 'dodge':
                if 'dodge' in player['actions']:     
                    dodging = True
                else:
                    input('You don\'t have the dodge action!  ' + used )
            elif action.lower() == 'run':
                if player['speed'] > monster.stats['speed']:
                    input('You run away! ' + used )
                    return 'ran'
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
                        if player['currentWeapon']['type'] == 'staff':
                            if player['mana'] >= player['actions']['magic'][theSpell]['mana'] - player['currentWeapon']['manaReduced']:
                                player['mana'] -= (player['actions']['magic'][theSpell]['mana'] - player['currentWeapon']['manaReduced'])
                                
                                if player['actions']['magic'][theSpell]['type'] == 'light':
                                    light += player['actions']['magic'][theSpell]['value']
                                    if light > 200:
                                        light = 200
                                    input('You casted a light spell and increased the light level by ' + str(player['actions']['magic'][theSpell]['value']) + '! ' + used)
                                elif player['actions']['magic'][theSpell]['type'] == 'attack':
                                    monster.stats['hp'] -= player['actions']['magic'][theSpell]['value']
                                    input('You casted a ' + player['actions']['magic'][theSpell]['name'] + ' for ' + str(player['actions']['magic'][theSpell]['mana'] - player['currentWeapon']['manaReduced']) + ' and you did ' + str(player['actions']['magic'][theSpell]['value']) + ' damage! ' + used)
                            else:
                                input('You don\'t have enough mana to cast that spell! ' + used)
                        else:
                            if player['mana'] >= player['actions']['magic'][theSpell]['mana']:
                                player['mana'] -= player['actions']['magic'][theSpell]['mana']
                                
                                if player['actions']['magic'][theSpell]['type'] == 'light':
                                    light += player['actions']['magic'][theSpell]['value']
                                    if light > 200:
                                        light = 200
                                    input('You casted a light spell and increased the light level by ' + str(player['actions']['magic'][theSpell]['value']) + '! ' + used)
                                elif player['actions']['magic'][theSpell]['type'] == 'attack':
                                    monster.stats['hp'] -= player['actions']['magic'][theSpell]['value']
                                    input('You casted a ' + player['actions']['magic'][theSpell]['name'] + ' for ' + str(player['actions']['magic'][theSpell]['mana']) + ' and you did ' + str(player['actions']['magic'][theSpell]['value']) + ' damage! ' + used)
                            else:
                                input('You don\'t have enough mana to cast that spell! ' + used)
                    except:
                        input('That isn\'t a spell you know! ' + used)    
                else:
                    input('You do not know any magic! ' + used)
            else:
                input('That is not an option!  ' + used )
            
            if monster.stats['hp'] <= 0:
                input('You have defeated the ' + monster.stats['name'] + '!  ' + used )
                player['xp'] += monster.stats['xpGain']
                return True

            i = 0
            while i < monster.stats['actionsNum']:  
                runAction = randint(0, actionsNum)
                currentAction = list(monster.stats['actions'])[runAction]
                if currentAction == 'atk':
                    if dodging == True or sneaking == True:
                        if dodging == True and monster.stats['speed'] > player['speed'] and dodgedLastTurn == False and sneaking == False:
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
                elif currentAction == 'dodging':
                    monsterDodging = True
                    dodging = False
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
    global floor
    global openMap
    
    
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
        ranAway = False
        newMap = False
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
        print('\nFloor: ' + str(floor))
        print('HP: ' +  str(player['hp']) + '/' + str(player['maxHp']))
        if player['class'] == 'mage':
            print('Mana: ' + str(player['mana']) + '/' + str(player['maxMana']))
        print('Light level: ' + str(light))
        print('Gold: ' + str(player['gold']))
        print('Armor: ' + player['currentArmor']['name'])
        print('Weapon: ' + player['currentWeapon']['name'])
    
        
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
                    # ... then fight
                    newFight = fight()
                    
                    # ... if the player dies ...
                    if newFight == False:
                        # ... then break the game
                        break
                    # ... if plaer runs away
                    elif newFight == 'ran':
                        # ... set the ranAway variable to true
                        ranAway = True
                # if there is a boss in the way...
                elif map[beforeInput+1] == '!':
                    # then boss fight...
                    if fight(boss=True)==False:
                        # if the player dies then break the while true loop
                        break
                # if there is a interactable in the way...
                elif map[beforeInput+1] == '-':
                    # ... then interact with the object
                    newInteract = interact()
                    
                    if newInteract == 'ran':
                        ranAway = True
                # if there is a shopkeeper in the way...
                elif map[beforeInput+1] == '$':
                    # ...then shop with the shop keeper
                    shop(beforeInput+1)
                # if there are stairs in the way...
                elif map[beforeInput+1] == '%':
                    # ...then edit variables and get a new map
                    floor += 1
                    
                    openMap = open('maps/map' + str(floor) + '.txt', 'r')
                    map = list(openMap.read())
                    openMap.close()
                    
                    shopInventories = {}
                    
                    t = 0 # counter variable
                    
                    # while t is less then the amount of characters in the map ...
                    while t < len(map):
                        # ... then check for all of the '$' in the map ...
                        if map[t] == '$':
                            # ... for each '$' in the map make a inventory for them
                            shopInventories[str(t)] = []
                        t += 1 # increase t
                    
                    del t # delete t
                    
                    newMap = True
                    
                    input('You are now going to floor ' + str(floor) + '! ' + used)
            # if the space that the player tried to move didn't have stairs or the player didn't run away from a fight...
            if newMap == False and ranAway == False:   
                # ... if the space that the player tried to move to didn't have a shop keeper in it...
                if map[beforeInput+1] != '$':
                    # ... then move the player to the space they wanted to move to
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
                    # ... then fight
                    newFight = fight()
                    
                    # ... if the player dies ...
                    if newFight == False:
                        # ... then break the game
                        break
                    # ... if plaer runs away
                    elif newFight == 'ran':
                        # ... set the ranAway variable to true
                        ranAway = True
                # if there is a boss in the way...
                elif map[beforeInput-1] == '!':
                    # then boss fight...
                    if fight(boss=True)==False:
                        # if the player dies then break the while true loop
                        break
                # if there is a interactable in the way...
                elif map[beforeInput-1] == '-':
                    # ... then interact with the object
                    newInteract = interact()
                    
                    if newInteract == 'ran':
                        ranAway = True
                # if there is a shopkeeper in the way...
                elif map[beforeInput-1] == '$':
                    # ...then shop with the shop keeper
                    shop(beforeInput-1)
                # if there are stairs in the way ...
                elif map[beforeInput-1] == '%':
                    # ...then edit variables and get a new map
                    floor += 1
                    
                    openMap = open('maps/map' + str(floor) + '.txt', 'r')
                    map = list(openMap.read())
                    openMap.close()
                    
                    shopInventories = {}
                    
                    t = 0 # counter variable
                    
                    # while t is less then the amount of characters in the map ...
                    while t < len(map):
                        # ... then check for all of the '$' in the map ...
                        if map[t] == '$':
                            # ... for each '$' in the map make a inventory for them
                            shopInventories[str(t)] = []
                        t += 1 # increase t
                    
                    del t # delete t
                    
                    input('You are now going to floor ' + str(floor) + '! ' + used)
                    newMap = True
                
                # if the space that the player tried to move didn't have stairs or the player didn't run away from a fight...
                if newMap == False and ranAway == False:   
                    # ... if the space that the player tried to move to didn't have a shop keeper in it...
                    if map[beforeInput-1] != '$':
                        # ... then move the player to the space they wanted to move to
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
                    # ... then fight
                    newFight = fight()
                    
                    # ... if the player dies ...
                    if newFight == False:
                        # ... then break the game
                        break
                    # ... if player runs away
                    elif newFight == 'ran':
                        # ... set the ranAway variable to true
                        ranAway = True
                # if there is a boss in the way...
                elif map[beforeInput-map.index('\n')-1] == '!':
                    # then boss fight...
                    if fight(boss=True)==False:
                        # if the player dies then break the while true loop
                        break
                # if there is a interactable in the way...
                elif map[beforeInput-map.index('\n')-1] == '-':
                    # ... then interact with the object
                    newInteract = interact()
                    
                    if newInteract == 'ran':
                        ranAway = True
                # if there is a shopkeeper in the way...
                elif map[beforeInput-map.index('\n')-1] == '$':
                    # ...then shop with the shop keeper
                    shop(beforeInput-map.index('\n')-1)
                # if there are stairs in the way...
                elif map[beforeInput-map.index('\n')-1] == '%':
                    # ...then edit variables and get a new map
                    floor += 1
                    
                    openMap = open('maps/map' + str(floor) + '.txt', 'r')
                    map = list(openMap.read())
                    openMap.close()
                    
                    shopInventories = {}
                    
                    t = 0 # counter variable
                    
                    # while t is less then the amount of characters in the map ...
                    while t < len(map):
                        # ... then check for all of the '$' in the map ...
                        if map[t] == '$':
                            # ... for each '$' in the map make a inventory for them
                            shopInventories[str(t)] = []
                        t += 1 # increase t
                    
                    del t # delete t
                    
                    input('You are now going to floor ' + str(floor) + '! ' + used)
                    newMap = True
                
                # if the space that the player tried to move didn't have stairs or the player didn't run away from a fight...
                if newMap == False and ranAway == False: 
                    # ... if the space that the player tried to move to didn't have a shop keeper in it...
                    if map[beforeInput-map.index('\n')-1] != '$':
                        # ... then move the player to the space they wanted to move to
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
                    # ... then fight
                    newFight = fight()
                    
                    # ... if the player dies ...
                    if newFight == False:
                        # ... then break the game
                        break
                    # ... if plaer runs away
                    elif newFight == 'ran':
                        # ... set the ranAway variable to true
                        ranAway = True
                # if there is a boss in the way...
                elif map[beforeInput+map.index('\n')+1] == '!':
                    # then boss fight...
                    if fight(boss=True)==False:
                        # if the player dies then break the while true loop
                        break
                # if there is a interactable in the way...
                elif map[beforeInput+map.index('\n')+1] == '-':
                    # ... then interact with the object
                    newInteract = interact()
                    
                    if newInteract == 'ran':
                        ranAway = True
                # if there is a shopkeeper in the way...
                elif map[beforeInput+map.index('\n')+1] == '$':
                    # ...then shop with the shop keeper
                    shop(beforeInput+map.index('\n')+1)
                # if there are stairs in the way...
                elif map[beforeInput+map.index('\n')+1] == '%':
                    # ...then edit variables and get a new map
                    floor += 1
                    
                    openMap = open('maps/map' + str(floor) + '.txt', 'r')
                    map = list(openMap.read())
                    openMap.close()
                    
                    shopInventories = {}
                    
                    t = 0 # counter variable
                    
                    # while t is less then the amount of characters in the map ...
                    while t < len(map):
                        # ... then check for all of the '$' in the map ...
                        if map[t] == '$':
                            # ... for each '$' in the map make a inventory for them
                            shopInventories[str(t)] = []
                        t += 1 # increase t
                    
                    del t # delete t
                    
                    input('You are now going to floor ' + str(floor) + '! ' + used)
                    newMap = True
                
                # if the space that the player tried to move didn't have stairs or the player didn't run away from a fight...
                if newMap == False and ranAway == False: 
                    # ... if the space that the player tried to move to didn't have a shop keeper in it...
                    if map[beforeInput+map.index('\n')+1] != '$':
                        # ... then move the player to the space they wanted to move to
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
                        
                        if light > 200:
                            light = 200
                        
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

# if the file is being ran directly
if __name__ == '__main__':
    # ... then run the game
    try:
        clear()
        choseClass()
        clear()
        loop()
        clear()
    except KeyboardInterrupt:
        clear()
