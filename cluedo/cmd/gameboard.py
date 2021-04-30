
from cluedo.cmd.player import Player
from cluedo.cmd.room import Room


class GameBoard:
    """gameboard for players to move on

    Where I really need some other brilliant minds to work together on
    """
    def __init__(self):
        self.board = []
        self.rooms = []

    def check_reachable_rooms(self, start, move_points) -> list:
        """Find all rooms the player can enter within their move points

        Args:
            start (Player): current player in action
            move_points (int): the step number player can use

        Returns:
            list: list of rooms player can enter
        """
        result_list = []
        # if player is not already in a room, find by coordinate
        if isinstance(start, Player) and not start.in_room:
            for this_room in self.rooms:
                for this_door in this_room.entrance:
                    distance = abs(start.coordinate[0] - this_door[0]) + abs(start.coordinate[1] - this_door[1])
                    if distance <= move_points:
                        result_list.append(this_room)
                    break
        #if isinstance(start, Room):
        # if player is already in a room, find by all doors the room player is in
        else:
            start = start.in_room
            for my_door in start.entrance:
                for this_room in self.rooms:
                    if this_room == start:
                        continue
                    for this_door in this_room.entrance:
                        distance = abs(my_door[0] - this_door[0]) + abs(my_door[1] - this_door[1])
                        if distance <= move_points:
                            if this_room not in result_list:
                                result_list.append(this_room)
                        break

        # add secret paths
        if start == self.rooms[0]:
            result_list.append(self.rooms[4])

        if start == self.rooms[6]:
            result_list.append(self.rooms[2])

        if start == self.rooms[4]:
            result_list.append(self.rooms[0])

        if start == self.rooms[2]:
            result_list.append(self.rooms[6])

        return result_list

    def move_player_to_room(self, player, room):
        player.in_room = room

    def move_player_to_coordinate(self, player, coord):
        """DEPRECATED

        """
        player.coordinate = coord

    def __repr__(self) -> str:
        constr = ""
        for row in self.board:
            for col in row:
                if col == 0:
                    constr += "一"
                elif col > 500:
                    constr += "墙"
                else:
                    constr += "口"
            constr += "\n"
        return constr

    def check_reachable_square(self,start,move_points) -> list:
        """DEPRECATED

        """
        pass
