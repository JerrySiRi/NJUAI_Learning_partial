# utils.py


class Indexer(object):
    """
    Bijection between objects and integers starting at 0. Useful for mapping
    labels, features, etc. into coordinates of a vector space.

    Attributes:
        objs_to_ints
        ints_to_objs
    """
    def __init__(self):
        self.objs_to_ints = {}
        self.ints_to_objs = {}

    def __repr__(self):
        return str([str(self.get_object(i)) for i in range(0, len(self))])

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.objs_to_ints)

    def get_object(self, index):
        """
        :param index: integer index to look up
        :return: Returns the object corresponding to the particular index or None if not found
        """
        if (index not in self.ints_to_objs):
            return None
        else:
            return self.ints_to_objs[index]

    def contains(self, object):
        """
        :param object: object to look up
        :return: Returns True if it is in the Indexer, False otherwise
        """
        return self.index_of(object) != -1

    def index_of(self, object):
        """
        :param object: object to look up
        :return: Returns -1 if the object isn't present, index otherwise
        """
        if (object not in self.objs_to_ints):
            return -1
        else:
            return self.objs_to_ints[object]

    def add_and_get_index(self, object, add=True):
        """
        Adds the object to the index if it isn't present, always returns a nonnegative index
        :param object: object to look up or add
        :param add: True by default, False if we shouldn't add the object. If False, equivalent to index_of.
        :return: The index of the object
        """
        if not add:
            return self.index_of(object)
        if (object not in self.objs_to_ints):
            new_idx = len(self.objs_to_ints)
            self.objs_to_ints[object] = new_idx
            self.ints_to_objs[new_idx] = object
        return self.objs_to_ints[object]


class Beam(object):
    """
    Beam data structure. Maintains a list of scored elements like a Counter, but only keeps the top n
    elements after every insertion operation. Insertion is O(n) (list is maintained in
    sorted order), access is O(1). Still fast enough for practical purposes for small beams.
    """
    def __init__(self, size):
        self.size = size
        self.elts = []
        self.scores = []

    def __repr__(self):
        return "Beam(" + repr(list(self.get_elts_and_scores())) + ")"

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.elts)

    def add(self, elt, score):
        """
        Adds the element to the beam with the given score if the beam has room or if the score
        is better than the score of the worst element currently on the beam

        :param elt: element to add
        :param score: score corresponding to the element
        """
        if len(self.elts) == self.size and score < self.scores[-1]:
            # Do nothing because this element is the worst
            return
        # If the list contains the item with a lower score, remove it
        i = 0
        while i < len(self.elts):
            if self.elts[i] == elt and score > self.scores[i]:
                del self.elts[i]
                del self.scores[i]
            i += 1
        # If the list is empty, just insert the item
        if len(self.elts) == 0:
            self.elts.insert(0, elt)
            self.scores.insert(0, score)
        # Find the insertion point with binary search
        else:
            lb = 0
            ub = len(self.scores) - 1
            # We're searching for the index of the first element with score less than score
            while lb < ub:
                m = (lb + ub) // 2
                # Check > because the list is sorted in descending order
                if self.scores[m] > score:
                    # Put the lower bound ahead of m because all elements before this are greater
                    lb = m + 1
                else:
                    # m could still be the insertion point
                    ub = m
            # lb and ub should be equal and indicate the index of the first element with score less than score.
            # Might be necessary to insert at the end of the list.
            if self.scores[lb] > score:
                self.elts.insert(lb + 1, elt)
                self.scores.insert(lb + 1, score)
            else:
                self.elts.insert(lb, elt)
                self.scores.insert(lb, score)
            # Drop and item from the beam if necessary
            if len(self.scores) > self.size:
                self.elts.pop()
                self.scores.pop()

    def get_elts(self):
        return self.elts

    def get_elts_and_scores(self):
        return zip(self.elts, self.scores)

    def head(self):
        return self.elts[0]


##################
# Tests
def test_beam():
    print("TESTING BEAM")
    beam = Beam(3)
    beam.add("a", 5)
    beam.add("b", 7)
    beam.add("c", 6)
    beam.add("d", 4)
    print("Should contain b, c, a: %s" % beam)
    beam.add("e", 8)
    beam.add("f", 6.5)
    print("Should contain e, b, f: %s" % beam)
    beam.add("f", 9.5)
    print("Should contain f, e, b: %s" % beam)

    beam = Beam(5)
    beam.add("a", 5)
    beam.add("b", 7)
    beam.add("c", 6)
    beam.add("d", 4)
    print("Should contain b, c, a, d: %s" % beam)
    beam.add("e", 8)
    beam.add("f", 6.5)
    print("Should contain e, b, f, c, a: %s" % beam)

if __name__ == '__main__':
    test_beam()
