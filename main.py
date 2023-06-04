import tabulate


def give_information(players: list, bank: int, total_bank: int, m_v_p):
    table = [[player.id, player.name, player.true, player.money] for player in players]
    columns = ["Number", "Player name", "True answers", "Money in bank"]
    print("Round ", 10-len(players))
    print(tabulate.tabulate(table, headers=columns))
    print("Bank in round: ", bank)
    print("Total bank: ", total_bank)
    print("Strongest link: ", m_v_p)
