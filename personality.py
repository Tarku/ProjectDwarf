# Personality.py

all_personalities = []

class Personality:
    '''
    The Personality class for the game.\n
    Use the "pe_" suffix for in-code variable identification.
    '''

    name: str

    def __init__(self, name):
        self.name = name

    def Register(self):
        all_personalities.append(self)
        return self


pe_Calm = Personality("personality.calm")
pe_Calm.Register()

pe_Shy = Personality("personality.shy")
pe_Shy.Register()

pe_Outgoing = Personality("personality.outgoing")
pe_Outgoing.Register()

pe_Irritable = Personality("personality.irritable")
pe_Irritable.Register()

