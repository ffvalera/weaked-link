import tabulate
import typing as tp
from dataclasses import dataclass, field

sums: list[int] = [0, 10, 20, 50, 100, 200, 300, 400, 500, 1000]


@dataclass(order= True)
class Player:
    id: int = field(compare= False)
    name: str = field(compare= False)
    true: int = 0
    money: int = 0
    in_game: bool = True

    def __str__(self) -> str:
        return self.name


class Game:
    total_bank: int = 0
    local_bank: int = 0
    players: list[Player] = []
    round_number = 0
    true_ans = 0
    first_player: Player

    def __init__(self):
        self.total_bank = self.local_bank = 0
        self.count = int(input("Введите количество игроков "))
        players_ = set()
        for i in range(self.count):
            name = input("Имя игрока " + str(i) + " ")
            while name in players_:
                print("Имена не должны повторяться. Попробуйте ещё раз ")
                name = input("Имя игрока " + str(i))
            players_.add(name)
            self.players.append(Player(id=i, name=name))

        self.first_player = min([(player.name, player) for player in self.players])[1]


    def turn(self, player: Player) -> int:
        ans = input("Ответил ли игрок " + player.name + " на вопрос ")
        if ans == 's':
            return 1
        elif ans == 'b':
            self.local_bank += sums[self.true_ans]
            player.money += sums[self.true_ans]
            self.true_ans = 0
            return self.turn(player)

        elif ans == '0' or ans == '1':
            if ans == '1':
                self.true_ans += 1
                player.true += 1
            else:
                self.true_ans = 0
            return 0
        else:
            return self.turn(player)

    def round(self) -> Player:
        self.local_bank = 0
        self.round_number += 1
        for player in self.players:
            player.true = 0
            player.money = 0
        current_player = self.first_player

        while self.local_bank <= sums[-1]:
            while not current_player.in_game:
                current_player = self.players[(current_player.id+1) % self.count]

            if self.turn(current_player):
                break

            current_player = self.players[(current_player.id + 1) % self.count]

        m_v_p = max(self.players)
        self.first_player = m_v_p
        self.total_bank += self.local_bank
        return m_v_p

    def delete_player(self, player: Player):
        player.in_game = False
        if self.first_player == player:
            self.first_player = min([(player.name, player) for player in self.players if player.in_game])[1]

    def give_information(self, m_v_p: Player):
        table = [[player.id, player.name, player.true, player.money] for player in self.players if player.in_game]
        columns = ["Number", "Player name", "True answers", "Money in bank"]
        print("Round ", self.round_number)
        print(tabulate.tabulate(table, headers=columns))
        print("Bank in round: ", self.local_bank)
        print("Total bank: ", self.total_bank)
        print("Strongest link: ", m_v_p)

    def end(self):
        print("total bank: ", self.total_bank)


game = Game()
for i in range(game.count-1):
    m_v_p = game.round()
    game.give_information(m_v_p)

    if i < game.count-2:

        table = [[player.id, player.name] for player in game.players if player.in_game]
        columns = ["ID", "Player name"]
        print(tabulate.tabulate(table, headers=columns))

        id = int(input("Какого игрока выгнать? "))
        game.delete_player(game.players[id])
    else:
        game.end()
