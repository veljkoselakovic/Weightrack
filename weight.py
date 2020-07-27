# 1 POUND TO KG
poundkgCONST = 0.453592


class Weight():
    """
    Class for using weights in both imperial and metric
    Weights are kept in metric by default, and converted afterwards
    Metric is also the default measurment standard
    @TODO: Write the rest of the documentation
    @TODO: Refactor/Rename the code, both amount and state are weird names
    @TODO: Extensively test this, not really sure how correctly is it working with the database
           (database is always in metric)
    """

    def __init__(self, amount, state=None):
        """
        Constructor
        :param amount: Mass
        :param state: Measurement standard
        """
        global poundkgCONST
        if state == 'metric' or state is None:
            self.amount = amount
        else:
            self.amount = amount * poundkgCONST
        if state == 'metric' or state is None:
            self.state = 'metric'
        else:
            self.state = 'imperial'

    def __repr__(self):
        """
        String representation of Weight class
        :example:
            w = Weight(130)
            print(w)
            >>130
        :return: Depending on the measurement standard, displays different numbers
        :rtype: string, not float
        """
        global poundkgCONST
        if self.state == 'metric':
            return str(self.amount)
        if self.state == 'imperial':
            return str(self.amount / poundkgCONST)

    def add(self, amount, state=None):
        """
        Adds a certain amount of weight
        :param amount: How much
        :param state: measurement standard, if None the class standard is used
        :return: None
        """
        global poundkgCONST
        if state is None:
            self.amount += amount
        if state == 'metric':
            if self.state == 'metric':
                self.amount += amount
            if self.state == 'imperial':
                self.amount += amount / poundkgCONST
        if state == 'imperial':
            if self.state == 'metric':
                self.amount += amount * poundkgCONST
            if self.state == 'imperial':
                self.amount += amount

    def __add__(self, other):
        """
        + operation implementation, measurement standard is ALWAYS the one that's in the instance (use @setStateTo
        functions to change this)
        :example:
            w = Weight(130)
            w += 10
            print(w)
            >>140
        :param other: The right operator @TODO: Rename to something else?
        :return: Returns the same class it adds onto
        :rtype: Weight
        """
        self.amount += other
        return self

    def sub(self, amount, state=None):
        """
        Subtracts a certain amount of weight
        :param amount: How much
        :param state: measurement standard, if None the class standard is used
        :return: None
        """
        global poundkgCONST
        if state is None:
            self.amount += amount
        if state == 'metric':
            if self.state == 'metric':
                self.amount -= amount
            if self.state == 'imperial':
                self.amount -= amount / poundkgCONST
        if state == 'imperial':
            if self.state == 'metric':
                self.amount -= amount * poundkgCONST
            if self.state == 'imperial':
                self.amount -= amount

    def __sub__(self, other):
        """
        - operation implementation, measurement standard is ALWAYS the one that's in the instance (use @setStateTo
        functions to change this)
        :example:
            w = Weight(130)
            w -= 10
            print(w)
            >>120
        :param other: The right operator @TODO: Rename to something else?
        :return: Returns the same class it adds onto
        :rtype: Weight
        """
        self.amount -= other
        return self

    def setStateToImperial(self):
        self.state = 'imperial'

    def setStateToMetric(self):
        self.state = 'metric'

    def val(self, state='metric'):
        global poundkgCONST
        if state == 'metric':
            return self.amount
        if state == 'imperial':
            return self.amount / poundkgCONST
        if state is None:
            return self.amount

    def set(self, amount, state=None):
        if state is None:
            self.amount = amount
        if state == 'metric':
            if self.state == 'metric':
                self.amount = amount
            if self.state == 'imperial':
                self.amount = amount / poundkgCONST
        if state == 'imperial':
            if self.state == 'imperial':
                self.amount = amount
            if self.state == 'metric':
                self.amount = amount * poundkgCONST

    def __eq__(self, other):
        if other.state == self.state:
            return other.amount == self.amount
        else:
            if other.state == 'imperial':
                return other.amount * poundkgCONST == self.amount
            if other.state == 'metric':
                return other.amount / poundkgCONST == self.amount

    def __lt__(self, other):
        if other.state == self.state:
            return other.amount > self.amount
        else:
            if other.state == 'imperial':
                return other.amount * poundkgCONST > self.amount
            if other.state == 'metric':
                return other.amount / poundkgCONST > self.amount

    def __le__(self, other):
        if other.state == self.state:
            return other.amount >= self.amount
        else:
            if other.state == 'imperial':
                return other.amount * poundkgCONST >= self.amount
            if other.state == 'metric':
                return other.amount / poundkgCONST >= self.amount

    def __gt__(self, other):
        if other.state == self.state:
            return other.amount < self.amount
        else:
            if other.state == 'imperial':
                return other.amount * poundkgCONST < self.amount
            if other.state == 'metric':
                return other.amount / poundkgCONST < self.amount

    def __ge__(self, other):
        if other.state == self.state:
            return other.amount <= self.amount
        else:
            if other.state == 'imperial':
                return other.amount * poundkgCONST <= self.amount
            if other.state == 'metric':
                return other.amount / poundkgCONST <= self.amount

    def __neq__(self, other):
        if other.state == self.state:
            return other.amount != self.amount
        else:
            if other.state == 'imperial':
                return other.amount * poundkgCONST != self.amount
            if other.state == 'metric':
                return other.amount / poundkgCONST != self.amount
