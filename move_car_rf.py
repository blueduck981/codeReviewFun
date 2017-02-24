# This is a program to move two vehicles around a grid.
# Each vehicle moves one space at a time in the direction
# that it is facing - or in the opposite direction it is 
# facing.  
##
# The user first inputs the size of their grid.
# Then the user picks where the first vehicle starts and the 
# direction it is facing.
# Next the user gives instructions for the movement of the vehicle.
#
# The previous two steps are repeated for the second vehicle.
# The program outputs the final positions of the vehicles on 
# the grid.

class Directions:
    #The vehicle is initialized in a particular direction.
    # It can turn Left (self.next) or Right (self.previous)
    """Circular buffer of possible directions"""
    DIRECTIONS = 'NESW'

    def __init__(self, start):
        self.index = self.DIRECTIONS.index(start)

    def next(self):
        self.index = (self.index + 1) % len(self.DIRECTIONS)

    def previous(self):
        self.index = (self.index - 1) % len(self.DIRECTIONS)

    @property
    def current(self):
        return self.DIRECTIONS[self.index]


class Vehicle():
    #Allowed directions and instructions for moving on XY grid
    MOVEMENT = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W':(-1, 0)}

    #A vehicle is initialized with a position in x,y, and a 
    # direction it is facing.  
    def __init__(self, x, y, facing, grid, obstacle):
        self.x = x
        self.y = y
        self.facing = Directions(facing)
        self.grid_width, self.grid_height = grid
        self.obstacle = obstacle

    @property
    def direction(self):
        return self.facing.current

    @property
    def position(self):
        return (self.x, self.y)

    #A vehicle can move forward (M) or backward (B)
    #Ot it can turn left (L) or right (R)    
    def parse_commands(self, commands):
        action = {
            'L': self.facing.previous,
            'R': self.facing.next,
            'M': self.move,
            'B': self.backwards,
        }
        for command in commands:
            action[command]()

    #function for moving the vehicle forward one space and checking for a collision
    # with the borders of the grid or with another vehicle.
    def move(self):
        offset_x, offset_y = self.MOVEMENT[self.facing.current]
        x = self.x + offset_x
        y = self.y + offset_y

        if (x, y) != self.obstacle and 0 <= x <= self.grid_width and 0 <= y <= self.grid_height:
            self.x = x
            self.y = y

    #function for moving the vehicle backward one space and checking for a collision
    # with the borders of the grid or with another vehicle. This is repetitive and 
    # should really be an option in "move"
    def backwards(self):
        offset_x, offset_y = self.MOVEMENT[self.facing.current]
        x = self.x - offset_x
        y = self.y - offset_y

        if (x, y) != self.obstacle and 0 <= x <= self.grid_width and 0 <= y <= self.grid_height:
            self.x = x
            self.y = y       


def setup_and_move_vehicle(grid, obstacle):
    print "Enter a starting position in the form 'X Y Direction'; e.g. 1 3 E"

    x, y, facing = raw_input().split()
    vehicle = Vehicle(int(x), int(y), facing, grid, obstacle)
    print "Enter commands for moving the vehicle in the form 'MLRB'; e.g. MMMBRRMLM"

    vehicle.parse_commands(raw_input().strip())
    return vehicle.position, vehicle.direction


def main():
    #user picks a grid:
    print "Enter a grid size in the form ' X Y '; e.g. 8 8"
    grid = map(int, raw_input().split())
    
    #print movement instructions for user:
    print 'Your vehicles can move North (N), South (S), East (E), West(W)'
    print 'Your vehicles can move forward one space (M) or backward one space (B)'
    
    #initialize and move vehicle 1
    print 'Vehicle 1:'
    v1_pos, v1_dir = setup_and_move_vehicle(grid, None)

    #initialize and move vehicle 2
    print 'Vehicle 2:'
    v2_pos, v2_dir = setup_and_move_vehicle(grid, v1_pos)
    
    #print the locations and facing directions of vehicles after moves
    print "Vehicle 1 is now at: "
    print v1_pos[0], v1_pos[1], v1_dir
    print "Vehicle 2 is now at: "
    print v2_pos[0], v2_pos[1], v2_dir


if __name__ == '__main__':
    main()