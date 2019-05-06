class Monster:
    def __init__(self, stats=None):
        self.stats = stats
        self.baseHp = stats['hp']


bat = Monster({'name' : 'bat', 'hp': 8, 'actionsNum': 1, 'actions':{'atk':{'bite': 2, 'claw': 4}}, 'speed': 4, 'floor':1})
bear = Monster({'name': 'Brown Bear', 'hp':20, 'actionsNum': 1, 'actions':{'atk':{'bite':4, 'claw':6}}, 'speed':6, 'floor':1})
wolf = Monster({'name' : 'Wolf', 'hp': 10, 'actionsNum': 1, 'actions':{'atk':{'bite': 4, 'claw': 4}}, 'speed': 8, 'floor':1})

listOfMonsters = {'1':[bat, wolf]}
listOfBosses = {'1':[bear]}