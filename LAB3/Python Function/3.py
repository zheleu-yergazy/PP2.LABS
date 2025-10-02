def solve(numheads, numlegs):
    rabbits = (numlegs - 2 * numheads) // 2
    chickens = numheads - rabbits
    return chickens, rabbits


chickens, rabbits = solve(35, 94)
print(f"Chickens: {chickens}, Rabbits: {rabbits}")
