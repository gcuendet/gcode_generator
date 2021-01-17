""" The content of this file  https://sourceforge.net/p/cadpy/wiki/Home/"""
import numpy as np


class CAStates:
    #
    # CA state definition class
    #
    def __init__(self):
        self.empty = 0
        self.interior = 1
        self.edge = 1 << 1  # 2
        self.north = 1 << 2  # 4
        self.west = 2 << 2  # 8
        self.east = 3 << 2  # 12
        self.south = 4 << 2  # 16
        self.stop = 5 << 2  # 20
        self.corner = 6 << 2  # 24


class RuleTable:
    #
    # CA rule table class
    #
    # 0 = empty
    # 1 = interior
    # 2 = edge
    # edge+direction = start
    #
    def __init__(self):
        self.table = np.zeros((2 ** (9 * 2),), dtype=np.uint32)
        self.s = CAStates()
        #
        # 1 0:
        #
        # 011
        # 111
        # 111
        self.add_rule(0, 1, 1, 1, 1, 1, 1, 1, 1, self.s.north)
        # 101
        # 111
        # 111
        self.add_rule(1, 0, 1, 1, 1, 1, 1, 1, 1, self.s.east)
        #
        # 2 0's:
        #
        # 001
        # 111
        # 111
        self.add_rule(0, 0, 1, 1, 1, 1, 1, 1, 1, self.s.east)
        # 100
        # 111
        # 111
        self.add_rule(1, 0, 0, 1, 1, 1, 1, 1, 1, self.s.east)
        # 010
        # 111
        # 111
        self.add_rule(0, 1, 0, 1, 1, 1, 1, 1, 1, self.s.east)
        # 011
        # 110
        # 111
        self.add_rule(0, 1, 1, 1, 1, 0, 1, 1, 1, self.s.south)
        # 110
        # 011
        # 111
        self.add_rule(1, 1, 0, 0, 1, 1, 1, 1, 1, self.s.east)
        # 101
        # 011
        # 111
        self.add_rule(1, 0, 1, 0, 1, 1, 1, 1, 1, self.s.east)
        # 101
        # 110
        # 111
        self.add_rule(1, 0, 1, 1, 1, 0, 1, 1, 1, self.s.south)
        # 011
        # 111
        # 110
        self.add_rule(0, 1, 1, 1, 1, 1, 1, 1, 0, self.s.corner)
        # 011
        # 111
        # 101
        self.add_rule(0, 1, 1, 1, 1, 1, 1, 0, 1, self.s.north)
        # 110
        # 111
        # 101
        self.add_rule(1, 1, 0, 1, 1, 1, 1, 0, 1, self.s.west)
        # 101
        # 111
        # 110
        self.add_rule(1, 0, 1, 1, 1, 1, 1, 1, 0, self.s.south)
        # 101
        # 111
        # 011
        self.add_rule(1, 0, 1, 1, 1, 1, 0, 1, 1, self.s.east)
        #
        # 3 0's:
        #
        # 001
        # 011
        # 111
        self.add_rule(0, 0, 1, 0, 1, 1, 1, 1, 1, self.s.east)
        # 010
        # 011
        # 111
        self.add_rule(0, 1, 0, 0, 1, 1, 1, 1, 1, self.s.east)
        # 010
        # 110
        # 111
        self.add_rule(0, 1, 0, 1, 1, 0, 1, 1, 1, self.s.south)
        # 010
        # 111
        # 011
        self.add_rule(0, 1, 0, 1, 1, 1, 0, 1, 1, self.s.east)
        # 010
        # 111
        # 110
        self.add_rule(0, 1, 0, 1, 1, 1, 1, 1, 0, self.s.south)
        # 110
        # 011
        # 011
        self.add_rule(1, 1, 0, 0, 1, 1, 0, 1, 1, self.s.east)
        # 011
        # 110
        # 110
        self.add_rule(0, 1, 1, 1, 1, 0, 1, 1, 0, self.s.south)
        # 101
        # 011
        # 011
        self.add_rule(1, 0, 1, 0, 1, 1, 0, 1, 1, self.s.east)
        # 101
        # 110
        # 110
        self.add_rule(1, 0, 1, 1, 1, 0, 1, 1, 0, self.s.south)
        # 011
        # 011
        # 011
        self.add_rule(0, 1, 1, 0, 1, 1, 0, 1, 1, self.s.north)
        #
        # 4 0's:
        #
        # 001
        # 011
        # 011
        self.add_rule(0, 0, 1, 0, 1, 1, 0, 1, 1, self.s.east)
        # 100
        # 110
        # 110
        self.add_rule(1, 0, 0, 1, 1, 0, 1, 1, 0, self.s.south)
        # 010
        # 011
        # 011
        self.add_rule(0, 1, 0, 0, 1, 1, 0, 1, 1, self.s.east)
        # 010
        # 110
        # 110
        self.add_rule(0, 1, 0, 1, 1, 0, 1, 1, 0, self.s.south)
        # 001
        # 110
        # 110
        self.add_rule(0, 0, 1, 1, 1, 0, 1, 1, 0, self.s.south)
        # 100
        # 011
        # 011
        self.add_rule(1, 0, 0, 0, 1, 1, 0, 1, 1, self.s.east)
        #
        # 5 0's:
        #
        # 000
        # 011
        # 011
        self.add_rule(0, 0, 0, 0, 1, 1, 0, 1, 1, self.s.east)
        #
        # edge states
        #
        # 200
        # 211
        # 211
        self.add_rule(2, 0, 0, 2, 1, 1, 2, 1, 1, self.s.east + self.s.edge)
        # 201
        # 211
        # 211
        self.add_rule(2, 0, 1, 2, 1, 1, 2, 1, 1, self.s.east + self.s.edge)
        # 210
        # 211
        # 211
        self.add_rule(2, 1, 0, 2, 1, 1, 2, 1, 1, self.s.east + self.s.edge)
        # 002
        # 112
        # 112
        self.add_rule(0, 0, 2, 1, 1, 2, 1, 1, 2, self.s.stop)
        # 102
        # 112
        # 112
        self.add_rule(1, 0, 2, 1, 1, 2, 1, 1, 2, self.s.stop)
        # 002
        # 112
        # 102
        self.add_rule(0, 0, 2, 1, 1, 2, 1, 0, 2, self.s.stop)
        # 012
        # 112
        # 112
        self.add_rule(0, 1, 2, 1, 1, 2, 1, 1, 2, self.s.stop)
        # 012
        # 112
        # 102
        self.add_rule(0, 1, 2, 1, 1, 2, 1, 0, 2, self.s.stop)

    def add_rule(self, nw, nn, ne, ww, cc, ee, sw, ss, se, rule):
        #
        # add a CA rule, with rotations
        #
        s = CAStates()
        #
        # add the rule
        #
        state = (
            (nw << 0)
            + (nn << 2)
            + (ne << 4)
            + (ww << 6)
            + (cc << 8)
            + (ee << 10)
            + (sw << 12)
            + (ss << 14)
            + (se << 16)
        )
        self.table[state] = rule
        #
        # rotate 90 degrees
        #
        state = (
            (sw << 0)
            + (ww << 2)
            + (nw << 4)
            + (ss << 6)
            + (cc << 8)
            + (nn << 10)
            + (se << 12)
            + (ee << 14)
            + (ne << 16)
        )
        if rule == s.east:
            self.table[state] = s.south
        elif rule == s.south:
            self.table[state] = s.west
        elif rule == s.west:
            self.table[state] = s.north
        elif rule == s.north:
            self.table[state] = s.east
        elif rule == (s.east + s.edge):
            self.table[state] = s.south + s.edge
        elif rule == (s.south + s.edge):
            self.table[state] = s.west + s.edge
        elif rule == (s.west + s.edge):
            self.table[state] = s.north + s.edge
        elif rule == (s.north + s.edge):
            self.table[state] = s.east + s.edge
        elif rule == s.corner:
            self.table[state] = s.corner
        elif rule == s.stop:
            self.table[state] = s.stop
        #
        # rotate 180 degrees
        #
        state = (
            (se << 0)
            + (ss << 2)
            + (sw << 4)
            + (ee << 6)
            + (cc << 8)
            + (ww << 10)
            + (ne << 12)
            + (nn << 14)
            + (nw << 16)
        )
        if rule == s.east:
            self.table[state] = s.west
        elif rule == s.south:
            self.table[state] = s.north
        elif rule == s.west:
            self.table[state] = s.east
        elif rule == s.north:
            self.table[state] = s.south
        elif rule == (s.east + s.edge):
            self.table[state] = s.west + s.edge
        elif rule == (s.south + s.edge):
            self.table[state] = s.north + s.edge
        elif rule == (s.west + s.edge):
            self.table[state] = s.east + s.edge
        elif rule == (s.north + s.edge):
            self.table[state] = s.south + s.edge
        elif rule == s.corner:
            self.table[state] = s.corner
        elif rule == s.stop:
            self.table[state] = s.stop
        #
        # rotate 270 degrees
        #
        state = (
            (ne << 0)
            + (ee << 2)
            + (se << 4)
            + (nn << 6)
            + (cc << 8)
            + (ss << 10)
            + (nw << 12)
            + (ww << 14)
            + (sw << 16)
        )
        if rule == s.east:
            self.table[state] = s.north
        elif rule == s.south:
            self.table[state] = s.east
        elif rule == s.west:
            self.table[state] = s.south
        elif rule == s.north:
            self.table[state] = s.west
        elif rule == (s.east + s.edge):
            self.table[state] = s.north + s.edge
        elif rule == (s.south + s.edge):
            self.table[state] = s.east + s.edge
        elif rule == (s.west + s.edge):
            self.table[state] = s.south + s.edge
        elif rule == (s.north + s.edge):
            self.table[state] = s.west + s.edge
        elif rule == s.corner:
            self.table[state] = s.corner
        elif rule == s.stop:
            self.table[state] = s.stop


def sort_segments(unsorted_segments):
    def distance(x1, y1, x2, y2):
        return np.sqrt((x1-x2)**2+(y1-y2)**2)

    sorted_segments = []
    if len(unsorted_segments) > 0:
        sorted_segments.append(
            unsorted_segments.pop(0)
        )  # starts with the first path in the list
    else:
        print("empty path --- strange")

    while len(unsorted_segments) > 0:
        # find closest start to the the last sorted segment start
        min_dist = 99999
        min_dist_index = None
        for i in range(len(unsorted_segments)):
            dist = distance(
                sorted_segments[-1][0][0],
                sorted_segments[-1][0][1],
                unsorted_segments[i][0][0],
                unsorted_segments[i][0][1],
            )
            if dist < min_dist:
                min_dist = dist
                min_dist_index = i

        # print "min_dist: %d index: %d" % (min_dist, min_dist_index)
        sorted_segments.append(unsorted_segments.pop(min_dist_index))
    return sorted_segments


def evaluate_state(arr):
    #
    # assemble the state bit strings
    #
    (ny, nx) = np.shape(arr)
    s = CAStates()
    nn = np.concatenate(([s.edge + np.zeros(nx, np.uint32)], arr[: (ny - 1)]))
    ss = np.concatenate((arr[1:], [s.edge + np.zeros(nx, np.uint32)]))
    ww = np.concatenate(
        (np.reshape(s.edge + np.zeros(ny, np.uint32), (ny, 1)), arr[:, : (nx - 1)]), 1
    )
    ee = np.concatenate(
        (arr[:, 1:], np.reshape(s.edge + np.zeros(ny, np.uint32), (ny, 1))), 1
    )
    cc = arr
    nw = np.concatenate(([s.edge + np.zeros(nx, np.uint32)], ww[: (ny - 1)]))
    ne = np.concatenate(([s.edge + np.zeros(nx, np.uint32)], ee[: (ny - 1)]))
    sw = np.concatenate((ww[1:], [s.edge + np.zeros(nx, np.uint32)]))
    se = np.concatenate((ee[1:], [s.edge + np.zeros(nx, np.uint32)]))
    state = (
        (nw << 0)
        + (nn << 2)
        + (ne << 4)
        + (ww << 6)
        + (cc << 8)
        + (ee << 10)
        + (sw << 12)
        + (ss << 14)
        + (se << 16)
    )
    return state


def vectorize_toolpaths(arr, tol: float = 0.2):
    #
    # convert lattice toolpath directions to vectors
    #
    s = CAStates()
    toolpaths = []
    start_sites = (
        (arr == (s.north + s.edge))
        | (arr == (s.south + s.edge))
        | (arr == (s.east + s.edge))
        | (arr == (s.west + s.edge))
    )
    num_start_sites = sum(sum(1.0 * start_sites))
    path_sites = (arr == s.north) | (arr == s.south) | (arr == s.east) | (arr == s.west)
    num_path_sites = sum(sum(1.0 * path_sites))
    remaining_sites = num_start_sites + num_path_sites
    while remaining_sites != 0:
        # print remaining_sites
        if num_start_sites > 0:
            #
            # begin segment on a start state
            #3
            if np.argmax(start_sites[0, :], axis=0) != 0:
                x = np.argmax(start_sites[0, :], axis=0)
                y = 0
            elif np.argmax(start_sites[:, 0], axis=0) != 0:
                x = 0
                y = np.argmax(start_sites[:, 0], axis=0)
            elif np.argmax(start_sites[-1, :], axis=0) != 0:
                x = np.argmax(start_sites[-1, :], axis=0)
                y = arr.shape[0] - 1
            elif np.argmax(start_sites[:, -1], axis=0) != 0:
                x = arr.shape[1] - 1
                y = np.argmax(start_sites[:, -1], axis=0)
            else:
                print("error: internal start")
                sys.exit()
            # print "start from ",x,y
        else:
            #
            # no start states; begin segment on upper-left boundary point
            #
            maxcols = np.argmax(path_sites, axis=1)
            y = np.argmax(np.argmax(path_sites, axis=1))
            x = maxcols[y]
            arr[y][x] += s.edge
            # print "segment from ",x,y
        segment = [(x, y)]
        vector = [(x, y)]
        while 1:
            #
            # follow path
            #
            y = vector[-1][1]
            x = vector[-1][0]
            state = arr[y][x]
            #
            # if start state, set stop
            #
            if state == (s.north + s.edge):
                state = s.north
                arr[y][x] = s.stop
            elif state == (s.south + s.edge):
                state = s.south
                arr[y][x] = s.stop
            elif state == (s.east + s.edge):
                state = s.east
                arr[y][x] = s.stop
            elif state == (s.west + s.edge):
                state = s.west
                arr[y][x] = s.stop
            # print "x,y,state,arr: ",x,y,state,arr[y][x]
            #
            # move if a valid direction
            #
            if state == s.north:
                direction = "north"
                # print "north"
                ynew = y - 1
                xnew = x
            elif state == s.south:
                direction = "south"
                # print "south"
                ynew = y + 1
                xnew = x
            elif state == s.east:
                direction = "east"
                # print "east"
                ynew = y
                xnew = x + 1
            elif state == s.west:
                direction = "west"
                # print "west"
                ynew = y
                xnew = x - 1
            elif state == s.corner:
                # print "corner"
                if direction == "east":
                    # print "south"
                    xnew = x
                    ynew = y + 1
                elif direction == "west":
                    # print "north"
                    xnew = x
                    ynew = y - 1
                elif direction == "north":
                    # print "east"
                    ynew = y
                    xnew = x + 1
                elif direction == "south":
                    # print "west"
                    ynew = y
                    xnew = x - 1
            else:
                #
                # not a valid direction, terminate segment on previous point
                #
                print("unexpected path termination at", x, y)
                # sys.exit()
                segment.append((x, y))
                toolpaths.append(segment)
                arr[y][x] = s.interior
                break
            # print "xnew,ynew,snew",xnew,ynew,arr[ynew][xnew]
            #
            # check if stop reached
            #
            if arr[ynew][xnew] == s.stop:
                # print "stop at ",xnew,ynew
                segment.append((xnew, ynew))
                toolpaths.extend([segment])
                if state != s.corner:
                    arr[y][x] = s.interior
                arr[ynew][xnew] = s.interior
                break
            #
            # find max transverse distance from vector to new point
            #
            dmax = 0
            dx = xnew - vector[0][0]
            dy = ynew - vector[0][1]
            norm = np.sqrt(dx ** 2 + dy ** 2)
            nx = dy / norm
            ny = -dx / norm
            for i in range(len(vector)):
                dx = vector[i][0] - vector[0][0]
                dy = vector[i][1] - vector[0][1]
                d = abs(nx * dx + ny * dy)
                if d > dmax:
                    dmax = d
            #
            # start new vector if transverse distance > tol
            #
            if dmax >= tol:
                # print "max at ",x,y
                segment.append((x, y))
                vector = [(x, y)]
            #
            # otherwise add point to vector
            #
            else:
                # print "add ",xnew,ynew
                vector.append((xnew, ynew))
                if (arr[y][x] != s.corner) & (arr[y][x] != s.stop):
                    arr[y][x] = s.interior
        start_sites = (
            (arr == (s.north + s.edge))
            | (arr == (s.south + s.edge))
            | (arr == (s.east + s.edge))
            | (arr == (s.west + s.edge))
        )
        num_start_sites = sum(sum(1.0 * start_sites))
        path_sites = (
            (arr == s.north) | (arr == s.south) | (arr == s.east) | (arr == s.west)
        )
        num_path_sites = sum(sum(1.0 * path_sites))
        remaining_sites = num_start_sites + num_path_sites
    #
    # reverse segment order, to start from inside to out
    #
    newpaths = []
    for segment in range(len(toolpaths)):
        newpaths.append(toolpaths[-1 - segment])
    return newpaths

