import random
from abc import ABCMeta, abstractmethod

#Tanya Boychenko
class AttackStrategy:
    """
    Each time a squad attacks it must choose a target squad, depending on the chosen strategy.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def select_squad(self, army):
        pass


class Random(AttackStrategy):
    """
    Each time a squad attacks it must choose a target squad, depending on the chosen strategy random
    """

    def select_squad(self, army):
        """
        attack any random squad
        :param army: chose army which will attack
        :return: (int) number squads which will be attacked
        """
        squads = army.get_squads
        random_squad = random.randint(0, len(squads) - 1)
        return squads[random_squad]


class Weakest(AttackStrategy):
    """
    Each time a squad attacks it must choose a target squad, depending on the chosen strategy weakest
    """

    def select_squad(self, army):
        """
        attack the weakest opposing squad
        :param army: chose army which will attack
        :return: (int) number squads which will be attacked
        """
        res = None
        squads = army.get_squads
        min_experience = min([i.get_experience for i in squads])
        for i in squads:
            if i.get_experience == min_experience:
                res = i
                break
            else:
                res = None
        return res


class Strongest(AttackStrategy):
    """
    Each time a squad attacks it must choose a target squad, depending on the chosen strategy strongest
    """

    def select_squad(self, army):
        """
        attack the strongest opposing squad
        :param army: chose army which will attack
        :return: (int) number squads which will be attacked
        """
        res = None
        squads = army.get_squads
        max_experience = max([i.get_experience for i in squads])
        for i in squads:
            if i.get_experience == max_experience:
                res = i
                break
            else:
                res = None
        return res

