from create_piece import createPiece

def fitness(c): # c = chromosome
    measures = createPiece(c)

    return 50