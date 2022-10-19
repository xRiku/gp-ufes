def rank(position: int):
    mark = 10
    points = 10
    while mark != 100:
        if position < mark:
            break
        mark += 10
        points -= 1
    return points