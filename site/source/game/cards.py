colors = ['red', 'green', 'blue', 'yellow']
values = [str(x) for x in range(1, 10)] * 2 + ['reverse', 'skip', 'draw-two'] * 2 + ['0']
wild_cards = [{'color': 'black', 'value': 'wild'}] * 4
draw_four_cards = [{'color': 'black', 'value': 'draw-four'}] * 4


def generate_cards():
    cards = []
    for col in colors:
        for val in values:
            cards.append({
                'color': col,
                'value': val,
            })
    return cards + wild_cards + draw_four_cards
