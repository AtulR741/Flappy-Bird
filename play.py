from game import init, play_step

record = 0

if __name__ == '__main__':
    init()
    while True:
        move = [0, 0]
        score, _, gameOver = play_step(move, record)
        if record < score:
            record = score
        if gameOver:
            init()