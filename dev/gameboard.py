class GameBoard:
    """gameboard for players to move on

    Where I really need some other brilliant minds to work together on
    """
    def __init__(self):
        self.board = []
        self.rooms = []

    def check_reachable_rooms(self, player, move_points) -> list:
        pass

    def move_player_to_room(self, player, room):
        pass

    def move_player_to_coordinate(self, player, coord):
        pass

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