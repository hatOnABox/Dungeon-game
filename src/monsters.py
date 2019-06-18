class monster:
    def __init__(self, stats=None):
        self.stats = stats
        self.baseHp = stats['hp']


bat = monster({'name' : 'bat', 'hp': 7, 'actionsNum': 1, 'actions':{'atk':{'bite': 3, 'claw': 4}}, 'speed': 4, 'xpGain': 2})
bear = monster({'name': 'Brown Bear', 'hp':15, 'actionsNum': 1, 'actions':{'atk':{'bite':4, 'claw':6}}, 'speed':6,'xpGain':20})
wolf = monster({'name' : 'Wolf', 'hp': 10, 'actionsNum': 1, 'actions':{'atk':{'bite': 4, 'claw': 4}}, 'speed': 8, 'xpGain':4})

skeleton = monster({'name': 'skeleton', 'hp': 12, 'actionsNum':1, 'actions':{'atk':{'sword':5}}, 'speed':5, 'xpGain':5})
giantRat = monster({'name': 'giantRat', 'hp':10, 'actionsNum': 1, 'actions':{'atk':{'bite':5, 'claw':6}}, 'speed':7, 'xpGain':5})

noviceNecromancer = monster({'name': 'novice necromancer', 'hp': 20, 'actionsNum': 2, 'actions':{'atk':{'ice spike': 5, 'undead hand': 5}}, 'speed':4, 'xpGain': 25})


listOfMonsters = {'1':[bat, wolf], '2':[skeleton, giantRat]}
listOfBosses = {'1':[bear], '2':[noviceNecromancer]}