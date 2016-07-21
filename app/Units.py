import random
import time
from abc import ABCMeta, abstractmethod, abstractproperty

#Tanya Boychenko
class Unit:
    """
    Each unit represents either a soldier or a vehicle maned by a predetermined number of soldiers.
    All units have the following properties:health and recharge
    :argument
        prev_time: stores time the last battle

    """

    __metaclass__ = ABCMeta
    __health = None
    __recharge = None
    __next_attack_time = 0
    prev_time = None

    @abstractproperty
    def do_attack(self):
        pass

    @abstractmethod
    def take_damage(self, *args):
        pass

    @property
    def get_recharge(self):
        return self.__recharge

    def set_recharge(self, recharge):
        self.__recharge = recharge

    @property
    def get_health(self):
        return self.__health

    def set_health(self, health):
        self.__health = health

    @abstractproperty
    def get_experience(self):
        pass

    @property
    def get_next_attack_time(self):
        return self.__next_attack_time

    def set_next_attack_time(self, next_attack_time):
        self.__next_attack_time = next_attack_time

    def check_attack(self):
        """
        Checks have enough time to recharge,using property recharge.
        Represents the number of ms required to recharge the unit for an attack
        :return
            True: if the attack will be carried out
            False: if the attack won`t be carried out
        """
        now = time.time() * 1000
        if self.prev_time is None:
            return True
        else:
            next_time = self.prev_time + self.get_recharge
            if now >= next_time:
                return True
            else:
                return False


class Solder(Unit):
    """
    Soldiers are units that have an additional property:experience
    The experience property is incremented after each successful attack,
    and is sed to calculate the attack success probability and the amount of damage inflicted
    Soldiers are considered active as long as they have any health.
    """
    __experience = 0

    def __init__(self):
        """
        Inits SampleClass with healt=100 and recharge in [100,2000].
        """
        self.set_health(100)
        self.set_recharge(random.randint(100, 2000) / 10000)

    @property
    def get_experience(self):
        return self.__experience

    def set_experience(self):
        if self.__experience < 50:
            self.__experience += 1

    @property
    def do_attack(self):
        """
        Soldiers attack success probability is calculated:
        0.5 * (1 + health/100) * random(50 + experience, 100) / 100
        where random(min, max) returns a random number between min and max (inclusive)
        :return
            (int) how much damage Soldier can cause
        """
        if self.get_health > 0 and self.check_attack():
            soldiers_attack = 0.5 * (1 + self.get_health) * \
                random.randint(50 + self.__experience, 100) / 100
            self.set_experience()
            self.prev_time = time.time() * 1000
            return soldiers_attack
        else:
            return 0

    def take_damage(self, damage):
        """
        The amount of damage a soldier can afflict is calculated as follows:
        0.05 + experience / 100
        :param damage: how much damage Soldier can cause
        :return: change health after attack
        """
        attack = damage - (0.05 + self.__experience / 1000)
        self.set_health(self.get_health - attack)


class Vehicles(Unit):
    """
    A battle vehicle has these additional properties:
    operators the number of soldiers required to operate the vehicle
    The recharge property for a vehicle must be greater than 1000 (ms).
    The total health of a vehicle unit is represented as the average health
    of all it's operators and the health of the vehicle.
    A vehicle is considered active as long as it self has any health and there
    is an vehicle operator with any health.

    :attribute
        operators is dict Solder in [1,3]

    """
    operators = []

    def __init__(self):
        """
        Inits SampleClass with operators in[1,3] and recharge in [1000,2000].
        """
        self.set_recharge(random.randint(1000, 2000) / 10000)
        operator_count = random.randint(1, 3)
        self.operators = [Solder() for _ in range(0, operator_count)]
        list_operators = [i.get_health for i in self.operators]
        self.set_health(sum(list_operators) / len(list_operators))

    def get_operators(self):
        return self.operators

    @property
    def get_experience(self):
        return sum([i.get_experience for i in self.operators])

    @staticmethod
    def alive(units):
        """
        Check live the unit in vehicle
        :param units: one of the dict operators
        :return:
            True: if unit live
            False: if unit die
        """
        res = False
        for i in units:
            if i.get_health > 0:
                res = True
                break
        return res

    @property
    def do_attack(self):
        """
        The Vehicle attack success probability is determined as follows:
        0.5 * (1 + vehicle.health / 100) * gavg(operators.attack_success)
        where gavg is the geometric average of the attack success of all the vehicle operators
        :return:
            (int) how much damage Vehicle can cause
        """
        if self.get_health > 0 and self.check_attack() \
                and self.alive(self.operators):
            list_attack_soldiers = [i.do_attack for i in
                                    self.operators]
            vehicles_attack = 0.5 * (1 + self.get_health / 100) * (
                sum(list_attack_soldiers) / len(list_attack_soldiers))
            self.prev_time = time.time() * 1000
            return vehicles_attack
        else:
            return 0

    def take_damage(self, damage):
        """
        The damage afflicted by a vehicle is calculated:
        0.1 + sum(operators.experience / 100)
        The total damage inflicted on the vehicle is distributed to the operators as follows:
        60% of the total damage is inflicted on the vehicle
        20% of the total damage is inflicted on a random vehicle operator
        The rest of the damage is inflicted evenly to the other operators (10% each)
        :param
            damage:how much damage can cause
        :return:
            change health after attack for each unit in operators and vehicle

        """
        list_operators_experience = [i.get_experience / 1000 for i in
                                     self.operators]
        damage -= 0.1 + sum(list_operators_experience)
        self.set_health(self.get_health - damage * 0.6)
        random_operator = random.randint(0, len(self.operators) - 1)
        j = 0
        while j < len(self.operators):
            if j == random_operator:
                self.operators[j].take_damage(damage * 0.2)
            else:
                self.operators[j].take_damage(damage * 0.1)
            j += 1

