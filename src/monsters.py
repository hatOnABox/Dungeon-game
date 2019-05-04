class Monster:
    def __init__(self, stats=None):
        self.stats = stats
        self.baseHp = stats['hp']


bat = Monster({'name' : 'bat', 'hp': 8, 'actionsNum': 1, 'actions':{'atk':{'bite': 2, 'claw': 4}}, 'speed': 4})