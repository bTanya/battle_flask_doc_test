import Units

#Tanya Boychenko
class Squad:
    """
    Squads are consisted out of a number of units (soldiers or vehicles), that behave as a coherent group.
    A squad is active as long as is contains an active unit.
    """
    __units = None
    __health = None

    def __init__(self, **kwargs):
        self.__units = [Units.Solder() for _ in range(1, kwargs['soldiers'] + 1)]
        self.__units += [Units.Vehicles() for _ in range(1, kwargs['vehicles'] + 1)]

    @property
    def get_experience(self):
        return sum([i.get_experience for i in self.__units])

    @property
    def get_health(self):
        self.__health = sum([i.get_health for i in self.__units])
        return self.__health

    @property
    def do_attack(self):
        """
        The attack success probability of a squad is determined
        as the average o the attack success probability of each member.
        :return:
            (int) the probability of attack success
        """
        return sum([i.do_attack for i in self.__units]) / len(self.__units)

    def take_damage(self, damage):
        """
        The damage received on a successful attack is distributed evenly to all squad members.
         The damage inflicted on a successful attack is the accumulation of the damage inflicted by each squad member.
        :param damage:how much damage can cause
        :return:change health after attack
        """
        damage /= len(self.__units)
        for i in self.__units:
            i.take_damage(damage)

