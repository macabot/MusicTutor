
class Theory:

    def __init__(self, names, components, info):
        self.names = names
        self.components = components
        self.info = info


class Scale(Theory):

    def __init__(self, names, intervals, info):
        super(Theory, self).__init__(names, intervals, info)

    def create_scale(root):
        yield root
        for i in self.intervals:
            yield root + i
            root += i


class Chord(Theory):

    def __init__(self, names, invervals, rule):
        if intervals[0] != 0:
            intervals = [0] + intervals
        super(Theory, self).__init__(names, intervals, info)
        
    def create_chord(root):
        return (root + i for i in self.intervals)
            
        