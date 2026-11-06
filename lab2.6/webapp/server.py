from flask import Flask, request, jsonify
import os
import time
import random
import threading

app = Flask(__name__)
processing_lock = threading.Lock()
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("/random", methods=["GET"])
def random_number():
    if not processing_lock.acquire(blocking=False):
        return jsonify({
            "status": "rejected",
            "message": "System busy"
            }), 429
    try:
        # Read seed from query parameter
        seed = request.args.get("seed", type=int)

        if (seed==0):
            rng = random.Random()
        else:
            rng = random.Random(seed)

        # Generate random number
        number = rng.randint(1, 100)
        #number = int(rng.integers(1, 101))

        time.sleep(3)

        return jsonify({
            "status": "ok",
            "message": number
        })

    finally:
        processing_lock.release()

if __name__ == "__main__":
    # Use PORT env variable if available, otherwise default to 5000
    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)