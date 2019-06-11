class monster:
    def __init__(self, stats=None):
        self.stats = stats
        self.baseHp = stats['hp']


bat = monster({'name' : 'bat', 'hp': 8, 'actionsNum': 1, 'actions':{'atk':{'bite': 3, 'claw': 4}}, 'speed': 4, 'floor':1, 'xpGain': 2})
bear = monster({'name': 'Brown Bear', 'hp':20, 'actionsNum': 1, 'actions':{'atk':{'bite':4, 'claw':6}}, 'speed':6, 'floor':1, 'xpGain':4})
wolf = monster({'name' : 'Wolf', 'hp': 10, 'reward':3 , 'actionsNum': 1, 'actions':{'atk':{'bite': 4, 'claw': 4}}, 'speed': 8, 'floor':1, 'xpGain':20})

listOfMonsters = {'1':[bat, wolf]}
listOfBosses = {'1':[bear]}