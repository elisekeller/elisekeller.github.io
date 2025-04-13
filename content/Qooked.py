from flask import Flask, request, jsonify
import numpy as np
from pyqubo import Binary
from neal import SimulatedAnnealingSampler

app = Flask(__name__)

def matrix_to_qubo(matrix, alpha=5, beta=4, allow_adjacent_penalty=True):
    n = matrix.shape[0]
    variables = {}

    for i in range(n):
        for j in range(n):
            variables[(i, j)] = Binary(f"x{i}{j}")

    # Objective: maximize impact
    H = -sum(matrix[i][j] * variables[(i, j)] for i in range(n) for j in range(n))

    # Penalty: fewer units (sparse deployment)
    total_selected = sum(variables[(i, j)] for i in range(n) for j in range(n))
    H += alpha * total_selected

    # Penalty: avoid placing adjacent units
    if allow_adjacent_penalty:
        for i in range(n):
            for j in range(n):
                if i < n - 1:
                    H += beta * variables[(i, j)] * variables[(i + 1, j)]
                if j < n - 1:
                    H += beta * variables[(i, j)] * variables[(i, j + 1)]

    model = H.compile()
    qubo, offset = model.to_qubo()
    return qubo, offset, model

def solve_qubo_with_neal(matrix, alpha=5, beta=4, num_reads=1000):
    qubo, offset, model = matrix_to_qubo(matrix, alpha=alpha, beta=beta)
    sampler = SimulatedAnnealingSampler()
    sampleset = sampler.sample_qubo(qubo, num_reads=num_reads)
    decoded_samples = model.decode_sampleset(sampleset)
    best_sample = decoded_samples[0]

    n = matrix.shape[0]
    solution_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            var_name = f"x{i}{j}"
            solution_matrix[i, j] = best_sample.sample.get(var_name, 0)

    return solution_matrix, best_sample.energy + offset

@app.route("/solve_qubo", methods=["POST"])
def solve_qubo_endpoint():
    try:
        data = request.get_json()
        matrix = np.array(data["matrix"])
        alpha = int(data.get("alpha", 5))
        beta = int(data.get("beta", 4))
        num_reads = int(data.get("num_reads", 1000))
        solution, energy = solve_qubo_with_neal(matrix, alpha, beta, num_reads)

        return jsonify({
            "solution": solution.astype(int).tolist(),
            "energy": round(energy, 4),
            "units_used": int(solution.sum())
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "QUBO Solver API is running."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)




