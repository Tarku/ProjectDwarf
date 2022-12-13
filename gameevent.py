# GameEvent.py

from random import randint
from colony import *
from person import *
from eventtype import *
from itempair import *

class GameEvent:

    '''
    The GameEvent class.\n
    Use the "ge_" prefix for in-code variable identification.
    '''

    def __init__(self, name, eventType: dict, chance = 1, duration = 1):
        self.name = name
        self.eventType = eventType # {"EventType": {"Item": <MATERIAL>, "Count": <INT>}}
        self.chance = chance
        self.duration = duration

    def DoIn(self, colony: Colony):
        for (currentType, currentValue) in self.eventType.items():
            if currentType is EventType.VISITOR:
                if type(currentValue) is not Person:

                    print(
                        f"Can't perform GameEvent <{self.name}> of Type <{currentType.name}. Cause: Type mismatch."
                    )
                    return None

                print(
                    f"Successfully performed GameEvent <{self.name}> of Type <{currentType.name}>."
                )
                return ('event.visitor', currentValue.name)

            elif currentType is EventType.COLONY_NAME_PROMPT:
                if type(currentValue) is not Person:
                    print(
                        f"Can't perform GameEvent <{self.name}> of Type <{currentType.name}. Cause: Type mismatch."
                    )
                    return None

                print(
                    f"Successfully performed GameEvent <{self.name}> of Type <{currentType.name}>."
                )
                return ('event.nameprompt', currentValue.name)

            elif currentType is EventType.VISITOR_GIFT:
                if type(currentValue) is not dict:
                    print(
                        f"Can't perform GameEvent <{self.name}> of Type <{currentType.name}. Cause: Type mismatch."
                    )
                    return None

                visitor = currentValue.get("Visitor")
                item = currentValue.get("Item")
                count = currentValue.get("Count")

                if visitor is None:
                    print(
                        f"Can't perform GameEvent <{self.name}> of Type <{currentType.name}. Cause: Visitor is none."
                    )
                    return None

                if item is None:
                    print(
                        f"Can't perform GameEvent <{self.name}> of Type <{currentType.name}. Cause: Item is none."
                    )
                    return None

                if count is None:
                    print(
                        f"Can't perform GameEvent <{self.name}> of Type <{currentType.name}. Cause: Count is none."
                    )
                    return None

                if type(visitor) is not Person:
                    print(
                        f"Can't perform GameEvent <{self.name}> of Type <{currentType.name}. Cause: Type mismatch in definition."
                    )
                    return None

                if not isinstance(item, Material):
                    print(
                        f"Can't perform GameEvent <{self.name}> of Type <{currentType.name}. Cause: Type mismatch in definition."
                    )
                    return None

                if type(count) is not int:
                    print(
                        f"Can't perform GameEvent <{self.name}> of Type <{currentType.name}. Cause: Type mismatch in definition."
                    )
                    return None


                if item not in colony.inventory:
                    colony.inventory[item] = count
                else:
                    colony.inventory[item] += count

                print(
                    f"Successfully performed GameEvent <{self.name}> of Type <{currentType.name}>."
                )

                return ('event.visitorgift', visitor, ItemPair(item, count))

            else:
                print(
                    f"Can't perform GameEvent <{self.name}>. Cause: Unknown GameEvent type."
                )
                return None

    def TryAt(self, colony: Colony):

        randomNumber = randint(1, self.chance)

        if randomNumber is not self.chance:
            return None

        self.DoIn(colony)



