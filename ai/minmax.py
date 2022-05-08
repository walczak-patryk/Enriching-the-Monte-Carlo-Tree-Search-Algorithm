from math import inf

def alpha_beta_minmax(iteration_state, player, current_player, d: int, alpha: int, beta: int, get_all_posible_moves, board_move, get_result, change_player, evaluate):
    if d <= 0:
        return None, evaluate(iteration_state, player), 1

    if not get_all_posible_moves(iteration_state, player) and not get_all_posible_moves(iteration_state, change_player(player)):
        winner = get_result(iteration_state, player)
        return None, 1 if winner == player else -1, 1

    maximizing = current_player == player 
    f = max if maximizing else min
    evaluations = {}
    nn = 0
    moves = get_all_posible_moves(iteration_state, current_player)
    for move in moves:
        new_state = board_move(iteration_state, move, current_player)
        _, e, n = alpha_beta_minmax(new_state, player, change_player(current_player), d - 1, alpha, beta, get_all_posible_moves, board_move, get_result, change_player, evaluate)
        if maximizing:
            alpha = f(alpha, e)
        else:
            beta = f(beta, e)
        evaluations[move] = e
        nn += n
        if beta <= alpha:
            break

    if not evaluations:
        if maximizing:
            return None, -inf, 1 
        else:
            return None, inf, 1 
    best = f(evaluations, key=evaluations.get)
    return best, evaluations[best], nn