import math

# Utility function
def calculate_utility(gene, target, weights):
    score = 0
    n = max(len(gene), len(target))

    for i in range(n):
        w = weights[i] if i < len(weights) else 1
        g = ord(gene[i]) if i < len(gene) else 0
        t = ord(target[i]) if i < len(target) else 0
        score -= w * abs(g - t)

    return score


# Minimax with Alpha-Beta Pruning
def minimax(pool, gene, depth, is_max, alpha, beta, target, weights):
    # Game over
    if not pool:
        return calculate_utility(gene, target, weights), gene

    if is_max:
        best_score = -math.inf
        best_gene = ""

        for ch in pool:
            new_pool = pool.copy()
            new_pool.remove(ch)

            score, final_gene = minimax(
                new_pool,
                gene + ch,
                depth + 1,
                False,
                alpha,
                beta,
                target,
                weights
            )

            if score > best_score:
                best_score = score
                best_gene = final_gene

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        return best_score, best_gene

    else:
        best_score = math.inf
        best_gene = ""

        for ch in pool:
            new_pool = pool.copy()
            new_pool.remove(ch)

            score, final_gene = minimax(
                new_pool,
                gene + ch,
                depth + 1,
                True,
                alpha,
                beta,
                target,
                weights
            )

            if score < best_score:
                best_score = score
                best_gene = final_gene

            beta = min(beta, best_score)
            if beta <= alpha:
                break

        return best_score, best_gene


# ---------- INPUT ----------
pool = input().strip().split(",")      # A,T,C,G
target = input().strip()               # target gene
student_id = list(map(int, input().split()))

# take last n digits as weights
weights = student_id[-len(target):]

# ---------- RUN ----------
score, best_gene = minimax(
    pool,
    "",
    0,
    True,
    -math.inf,
    math.inf,
    target,
    weights
)

# ---------- OUTPUT ----------
print("Best gene sequence generated:", best_gene)
print("Utility score:", score)
