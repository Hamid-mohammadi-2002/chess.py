import abc
import tkinter as tk
from PIL import Image, ImageTk

#################################################
#               Initial data                    #
#################################################
height = 70
width = 70
root = tk.Tk()
root.title("Chess")
status = tk.Label(root, text="White player turn:", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status.grid(row=225, column=0, sticky="we", columnspan=25)
my_image = ImageTk.PhotoImage(Image.open("pictures/Test.png"))
none_image = ImageTk.PhotoImage(Image.open("pictures/pices/none.png"))
pawn_image_black = ImageTk.PhotoImage(Image.open("pictures/pices/black_pawn.png"))
pawn_image_white = ImageTk.PhotoImage(Image.open("pictures/pices/white_pawn.png"))
king_image_white = ImageTk.PhotoImage(Image.open("pictures/pices/white_king.png"))
king_image_black = ImageTk.PhotoImage(Image.open("pictures/pices/black_king.png"))
queen_image_white = ImageTk.PhotoImage(Image.open("pictures/pices/white_queen.png"))
queen_image_black = ImageTk.PhotoImage(Image.open("pictures/pices/black_queen.png"))
bishop_image_white = ImageTk.PhotoImage(Image.open("pictures/pices/white_bishop.png"))
bishop_image_black = ImageTk.PhotoImage(Image.open("pictures/pices/black_bishop.png"))
knight_image_white = ImageTk.PhotoImage(Image.open("pictures/pices/white_knight.png"))
knight_image_black = ImageTk.PhotoImage(Image.open("pictures/pices/black_knight.png"))
rook_image_white = ImageTk.PhotoImage(Image.open("pictures/pices/white_rook.png"))
rook_image_black = ImageTk.PhotoImage(Image.open("pictures/pices/black_rook.png"))
board_column = "abcdefgh"
board_data = dict()


#################################################
#               Creating board                  #
#################################################
class Board:
    def __init__(self):
        self.board_data = dict()
        self.board_legend = dict()
        self.my_image = ""
        self.possible = list()
        self.last_slot = None
        ###############
        #   legends
        ##############
        for i in board_column:
            self.board_legend[i] = tk.Label(root, text=i).grid(row=0, column=board_column.index(i) + 1)
            self.board_legend[board_column.index(i)] = tk.Label(root, text=9 - (board_column.index(i) + 1)).grid(
                row=board_column.index(i) + 1, column=0)
            self.board_legend[f"{i}2"] = tk.Label(root, text=i).grid(row=9, column=board_column.index(i) + 1)
            self.board_legend[f"{board_column.index(i)}D"] = tk.Label(root, text=9 - (board_column.index(i) + 1)).grid(
                row=board_column.index(i) + 1, column=9)

        #########################
        #   loading board data
        #########################
        for row in range(1, 9):
            for column in board_column:
                if row % 2 == 0:
                    color = "gray" if board_column.index(column) % 2 == 0 else "white"
                else:
                    color = "white" if board_column.index(column) % 2 == 0 else "gray"
                data = self.contributor(row, column)

                # print(my_image)
                # print(data[1])
                # img=data[1]
                self.board_data[f"{column}{9 - row}"] = [
                    tk.Button(root, height=height, width=width, bg=color, image=data[1],
                              command=lambda slot=f"{column}{9 - row}": self.select(slot)), data[0]]
                self.board_data[f"{column}{9 - row}"][0].grid(row=row, column=board_column.index(column) + 1)

    def select(self, slot):
        # if self.board_data[slot][1] is not None and self.board_data[slot][1].white == Player.whos_turn_is_it().white:
        # print(main_board.board_data.keys())
        for field in self.board_data.keys():
            if int(field[1]) % 2 == 0:
                color = "white" if board_column.find(field[0]) % 2 == 0 else "gray"
            else:
                color = "gray" if board_column.find(field[0]) % 2 == 0 else "white"
            self.board_data[field][0].configure(bg=color)
        if self.possible is None and self.board_data[slot][1].white == Player.whos_turn_is_it().white:
            self.board_data[slot][0].configure(bg="red")
            # print(self.board_data[slot][0])
            if self.board_data[slot][1] is not None:
                possible = self.board_data[slot][1].possible_movements()
                if possible is not None:
                    self.possible = possible
                    for p in self.possible:
                        self.board_data[p][0].configure(bg="yellow")
            self.last_slot = slot
        if self.possible is not None and slot not in self.possible:
            if self.board_data[slot][1] is not None and self.board_data[slot][
                1].white == Player.whos_turn_is_it().white:
                self.board_data[slot][0].configure(bg="red")
                if self.board_data[slot][1] is not None:
                    possible = self.board_data[slot][1].possible_movements()
                    if possible is not None:
                        self.possible = possible
                        for p in self.possible:
                            self.board_data[p][0].configure(bg="yellow")
                self.last_slot = slot
        else:
            if self.possible is not None:
                if self.board_data[slot][1] is not None:
                    Piece.diactivated_pieces.append(self.board_data[slot][1])
                    show_dicativated()
                    self.board_data[slot][1].activated = False
                    self.board_data[slot][1].location = None

                self.board_data[slot][1] = self.board_data[self.last_slot][1]
                self.board_data[slot][1].update_location(slot)
                self.board_data[slot][0].configure(image=self.board_data[slot][1].image)
                self.board_data[self.last_slot][0].configure(image=none_image)
                self.board_data[self.last_slot][1] = None
                self.last_slot = None
                self.possible = None
                Player.whos_turn_is_it().play()

    def contributor(self, row, column):
        if row in [3, 4, 5, 6]:
            return [None, none_image]
        elif row == 7:
            # print(f"{column}{row}")
            return [Pawn(True, f"{column}{9 - row}"), pawn_image_white]
            # return [None, pawn_image_white]
        elif row == 2:
            return [Pawn(False, f"{column}{9 - row}"), pawn_image_black]
            # return [None, pawn_image_black]
        elif row == 8:
            if column == "e":
                return [King(True, f"{column}{9 - row}"), king_image_white]
            if column == "d":
                return [Queen(True, f"{column}{9 - row}"), queen_image_white]
            if column == "c" or column == "f":
                return [Bishop(True, f"{column}{9 - row}"), bishop_image_white]
            if column == "b" or column == "g":
                return [Knight(True, f"{column}{9 - row}"), knight_image_white]
            if column == "a" or column == "h":
                return [Rook(True, f"{column}{9 - row}"), rook_image_white]
            # return [None, none_image]

        elif row == 1:
            if column == "e":
                return [King(False, f"{column}{9 - row}"), king_image_black]
            if column == "d":
                return [Queen(False, f"{column}{9 - row}"), queen_image_black]
            if column == "c" or column == "f":
                return [Bishop(False, f"{column}{9 - row}"), bishop_image_black]
            if column == "b" or column == "g":
                return [Knight(False, f"{column}{9 - row}"), knight_image_black]
            if column == "a" or column == "h":
                return [Rook(False, f"{column}{9 - row}"), rook_image_black]
            # return [None, none_image]


##################################
#   Defining Pieces
##################################

class Piece:
    all_pieces = list()
    diactivated_pieces = list()

    def __init__(self, white, location, range=9):
        self.white = white
        self.location = location
        self.activated = True
        self.range = range
        self.possible_movements_list = list()
        self.image = ""
        self.first_move = True
        Piece.all_pieces.append(self)
        # ImageTk.PhotoImage(Image.open("pictures/Test.png"))

    def update_location(self, loc):
        self.location = loc
        if self.first_move:
            self.first_move = False

    def possible_movements(self):
        pass

    def cross(self):
        cross_possible_movements = list()
        (W, E, N, S) = (True, True, True, True)
        for changer in range(1, self.range + 1):
            if W:
                W = True if board_column.find(self.location[0]) - changer >= 0 else False
            if E:
                E = True if board_column.find(self.location[0]) + changer < 8 else False
            if N:
                N = True if int(self.location[1]) + changer <= 8 else False
            if S:
                S = True if int(self.location[1]) - changer > 0 else False

            if W:
                column = board_column[board_column.find(self.location[0]) - changer]
                row = self.location[1]
                # print(main_board.board_data[f"{column}{row}"][1])
                if main_board.board_data[f"{column}{row}"][1] is None:
                    cross_possible_movements.append(f"{column}{row}")
                elif main_board.board_data[f"{column}{row}"][1].white is not self.white:
                    cross_possible_movements.append(f"{column}{row}")
                    W = False
                elif main_board.board_data[f"{column}{row}"][1].white is self.white:
                    W = False
            if E:
                # print(board_column.find(self.location[0]), changer)
                column = board_column[board_column.find(self.location[0]) + changer]
                row = self.location[1]
                if main_board.board_data[f"{column}{row}"][1] is None:
                    cross_possible_movements.append(f"{column}{row}")
                elif main_board.board_data[f"{column}{row}"][1].white is not self.white:
                    cross_possible_movements.append(f"{column}{row}")
                    E = False
                elif main_board.board_data[f"{column}{row}"][1].white is self.white:
                    E = False

            if N:
                column = self.location[0]
                row = int(self.location[1]) + changer
                if main_board.board_data[f"{column}{row}"][1] is None:
                    cross_possible_movements.append(f"{column}{row}")
                elif main_board.board_data[f"{column}{row}"][1].white is not self.white:
                    cross_possible_movements.append(f"{column}{row}")
                    N = False
                elif main_board.board_data[f"{column}{row}"][1].white is self.white:
                    N = False

            if S:
                column = self.location[0]
                row = int(self.location[1]) - changer
                if main_board.board_data[f"{column}{row}"][1] is None:
                    cross_possible_movements.append(f"{column}{row}")
                elif main_board.board_data[f"{column}{row}"][1].white is not self.white:
                    cross_possible_movements.append(f"{column}{row}")
                    S = False
                elif main_board.board_data[f"{column}{row}"][1].white is self.white:
                    S = False

        return cross_possible_movements

    def diagonal(self):
        ####################################################
        # p=positive n= negative
        ####################################################
        (pp, pn, np, nn) = (True, True, True, True)
        possible_diagonal_movements = list()
        #############################
        #   board border check
        #############################
        for row in range(1, self.range + 1):
            if pp:
                pp = True if board_column.index(self.location[0]) + row < 8 and (
                        (int(self.location[1]) - 1) + row) < 8 else False
            if pn:
                pn = True if board_column.index(self.location[0]) + row < 8 and (
                        (int(self.location[1]) - 1) - row) >= 0 else False
            if nn:
                nn = True if board_column.index(self.location[0]) - row >= 0 and (
                        (int(self.location[1]) - 1) - row) >= 0 else False
            if np:
                np = True if board_column.index(self.location[0]) - row >= 0 and (
                        (int(self.location[1]) - 1) + row) < 8 else False
            if pp:
                column = board_column[board_column.index(self.location[0]) + row]
                roww = int(self.location[1]) + row
                if main_board.board_data[f"{column}{roww}"][1] is None:
                    possible_diagonal_movements.append(f"{column}{roww}")
                elif main_board.board_data[f"{column}{roww}"][1].white is not self.white:
                    possible_diagonal_movements.append(f"{column}{roww}")
                    pp = False
                elif main_board.board_data[f"{column}{roww}"][1].white == self.white:
                    pp = False

            if pn:
                column = board_column[board_column.index(self.location[0]) + row]
                roww = int(self.location[1]) - row
                if main_board.board_data[f"{column}{roww}"][1] is None:
                    possible_diagonal_movements.append(f"{column}{roww}")
                elif main_board.board_data[f"{column}{roww}"][1].white is not self.white:
                    possible_diagonal_movements.append(f"{column}{roww}")
                    pn = False
                elif main_board.board_data[f"{column}{roww}"][1].white == self.white:
                    pn = False

            if nn:
                column = board_column[board_column.index(self.location[0]) - row]
                roww = int(self.location[1]) - row
                if main_board.board_data[f"{column}{roww}"][1] is None:
                    possible_diagonal_movements.append(f"{column}{roww}")
                elif main_board.board_data[f"{column}{roww}"][1].white is not self.white:
                    possible_diagonal_movements.append(f"{column}{roww}")
                    nn = False
                elif main_board.board_data[f"{column}{roww}"][1].white == self.white:
                    nn = False
            if np:
                column = board_column[board_column.index(self.location[0]) - row]
                roww = int(self.location[1]) + row
                if main_board.board_data[f"{column}{roww}"][1] is None:
                    possible_diagonal_movements.append(f"{column}{roww}")
                elif main_board.board_data[f"{column}{roww}"][1].white is not self.white:
                    possible_diagonal_movements.append(f"{column}{roww}")
                    np = False
                elif main_board.board_data[f"{column}{roww}"][1].white == self.white:
                    np = False
        return possible_diagonal_movements

    def pawn_movement(self):
        possible_pawn_list = list()
        forward = True
        if self.white:
            if self.first_move:
                if forward:
                    for r in range(1, 3):
                        if main_board.board_data[f"{self.location[0]}{int(self.location[1]) + r}"][1] is None:
                            possible_pawn_list.append(f"{self.location[0]}{int(self.location[1]) + r}")
                        else:
                            forward = False
                if board_column.find(self.location[0]) + 1 < 8:
                    if main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) + 1}"][
                        1] is None:
                        pass
                        # possible_pawn_list.append(
                        # f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) + 1}")
                    elif main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) + 1}"][
                        1].white is not self.white:
                        possible_pawn_list.append(
                            f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) + 1}")
                if board_column.find(self.location[0]) - 1 >= 0:
                    if main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) + 1}"][
                        1] is None:
                        pass
                        # possible_pawn_list.append(
                        # f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) + 1}")
                    elif main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) + 1}"][
                        1].white is not self.white:
                        possible_pawn_list.append(
                            f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) + 1}")
            else:

                if main_board.board_data[f"{self.location[0]}{int(self.location[1]) + 1}"][1] is None:
                    possible_pawn_list.append(f"{self.location[0]}{int(self.location[1]) + 1}")

                if board_column.find(self.location[0]) + 1 <= 8:
                    if main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) + 1}"][
                        1] is None:
                        pass
                        # possible_pawn_list.append(
                        # f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) + 1}")
                    elif main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) + 1}"][
                        1].white is not self.white:
                        possible_pawn_list.append(
                            f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) + 1}")
                if board_column.find(self.location[0]) - 1 >= 0:
                    if main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) + 1}"][
                        1] is None:
                        pass
                        # possible_pawn_list.append(
                        # f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) + 1}")
                    elif main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) + 1}"][
                        1].white is not self.white:
                        possible_pawn_list.append(
                            f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) + 1}")
        else:
            if self.first_move:
                if forward:
                    for r in range(1, 3):
                        if main_board.board_data[f"{self.location[0]}{int(self.location[1]) - r}"][1] is None:
                            possible_pawn_list.append(f"{self.location[0]}{int(self.location[1]) - r}")
                        else:
                            forward = False
                if board_column.find(self.location[0]) - 1 >= 0:
                    if main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) - 1}"][
                        1] is None:
                        pass
                        # possible_pawn_list.append(
                        # f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) + 1}")
                    elif main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) - 1}"][
                        1].white is not self.white:
                        possible_pawn_list.append(
                            f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) - 1}")
                if board_column.find(self.location[0]) - 1 >= 0:
                    if main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) - 1}"][
                        1] is None:
                        pass
                        # possible_pawn_list.append(
                        # f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) + 1}")
                    elif main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) - 1}"][
                        1].white is not self.white:
                        possible_pawn_list.append(
                            f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) - 1}")
            else:

                if main_board.board_data[f"{self.location[0]}{int(self.location[1]) - 1}"][1] is None:
                    possible_pawn_list.append(f"{self.location[0]}{int(self.location[1]) - 1}")

                if board_column.find(self.location[0]) + 1 <= 8:
                    if main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) - 1}"][
                        1] is None:
                        pass
                        # possible_pawn_list.append(
                        # f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) + 1}")
                    elif main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) - 1}"][
                        1].white is not self.white:
                        possible_pawn_list.append(
                            f"{board_column[board_column.find(self.location[0]) + 1]}{int(self.location[1]) - 1}")
                if board_column.find(self.location[0]) - 1 >= 0:
                    if main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) - 1}"][
                        1] is None:
                        pass
                        # possible_pawn_list.append(
                        # f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) + 1}")
                    elif main_board.board_data[
                        f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) - 1}"][
                        1].white is not self.white:
                        possible_pawn_list.append(
                            f"{board_column[board_column.find(self.location[0]) - 1]}{int(self.location[1]) - 1}")
        return possible_pawn_list

    def knight_movement(self):
        possible_movements = list()
        movement_patern = [[1, 2], [2, 1], [-1, 2], [-2, 1], [2, - 1], [1, -2], [-1, -2], [-2, -1]]
        for move in movement_patern:
            if board_column.find(self.location[0]) + move[0] >= 0 and board_column.find(self.location[0]) + move[
                0] < 8 and int(self.location[1]) + move[1] > 0 and int(self.location[1]) + move[1] <= 8:
                if main_board.board_data[
                    f"{board_column[board_column.find(self.location[0]) + move[0]]}{int(self.location[1]) + move[1]}"][
                    1] is None:
                    possible_movements.append(
                        f"{board_column[board_column.find(self.location[0]) + move[0]]}{int(self.location[1]) + move[1]}")
                elif main_board.board_data[
                    f"{board_column[board_column.find(self.location[0]) + move[0]]}{int(self.location[1]) + move[1]}"][
                    1].white is not self.white:
                    possible_movements.append(
                        f"{board_column[board_column.find(self.location[0]) + move[0]]}{int(self.location[1]) + move[1]}")
        return possible_movements


class Queen(Piece):
    def __init__(self, white, location, range=9):
        super().__init__(white, location, range)
        if self.white:
            self.image = queen_image_white
        else:
            self.image = queen_image_black

    def possible_movements(self):
        possible_movements_list = list()
        possible_movements_list += self.diagonal()
        possible_movements_list += self.cross()
        return possible_movements_list


class Rook(Piece):
    def __init__(self, white, location, range=9):
        super().__init__(white, location, range)
        if self.white:
            self.image = rook_image_white
        else:
            self.image = rook_image_black

    def possible_movements(self):
        return self.cross()


class Bishop(Piece):
    def __init__(self, white, location, range=9):
        super().__init__(white, location, range)
        if self.white:
            self.image = bishop_image_white
        else:
            self.image = bishop_image_black

    def possible_movements(self):
        return self.diagonal()


class King(Piece):
    def __init__(self, white, location, range=1):
        super().__init__(white, location, range)
        if self.white:
            self.image = king_image_white
        else:
            self.image = king_image_black

    def possible_movements(self):
        possible_movements_list = list()
        possible_movements_list += self.diagonal()
        possible_movements_list += self.cross()
        return possible_movements_list


class Pawn(Piece):
    def __init__(self, white, location, range=1):
        super().__init__(white, location, range)
        if self.white:
            self.image = pawn_image_white
        else:
            self.image = pawn_image_black

    def possible_movements(self):
        return self.pawn_movement()


class Knight(Piece):
    def __init__(self, white, location, range=9):
        super().__init__(white, location, range)
        if self.white:
            self.image = knight_image_white
        else:
            self.image = knight_image_black

    def possible_movements(self):
        return self.knight_movement()


class Player:
    players = list()

    def __init__(self, white, ai=False):
        self.turn = False
        self.white = white
        self.ai = ai
        if self.white:
            self.turn = True
            status.configure(text="Player turn: White")
        Player.players.append(self)

    def play(self):
        self.turn = False
        x = set(Player.players)
        x.discard(self)
        x = list(x)
        x[0].turn = True
        if x[0].white:
            status.configure(text="Player turn: White")
        else:
            status.configure(text="Player turn: Black")

    @staticmethod
    def whos_turn_is_it():

        return [x for x in Player.players if x.turn is True][0]


main_board = Board()
player1 = Player(True, False)
player2 = Player(False, False)


def show_dicativated():
    label_pics = list()
    row = 0
    column = 0
    x = 0
    for pic in Piece.diactivated_pieces:
        if row > 6:
            column += 1
            row = 0
        label_pics.append(tk.Label(image=pic.image))
        label_pics[x].grid(row=row + 1, column=50 + column)
        x += 1
        row += 1


root.mainloop()
