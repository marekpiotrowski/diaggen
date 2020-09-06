class Relation(object):
    USAGE = 1
    INHERITANCE = 2
    AGGREGATION = 3
    COMPOSITION = 4

    def __init__(self, party_a, party_b, type):
        self.party_a = party_a  # in case of inheritance, this is always going to be the child
        self.party_b = party_b
        self.type = type

    def __repr__(self):
        return "Relation type: {}, between {} and {}".format(self.type, self.party_a, self.party_b)