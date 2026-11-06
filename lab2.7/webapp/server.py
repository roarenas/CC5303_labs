from flask import Flask, request, jsonify
import os
import time
import random
import threading
import socket
import subprocess
import signal
import sys

HAPROXY_API_HOST = os.environ.get("HAPROXY_API_HOST", "frontend").strip()
HAPROXY_API_PORT = int(os.environ.get("HAPROXY_API_PORT", 9999))
BACKEND = os.environ.get("BACKEND", "wdefault").strip()
SERVER_NAME = subprocess.run(['hostname'], capture_output=True, text=True).stdout.strip()
SERVER_IP = subprocess.run(['hostname', '-I'], capture_output=True, text=True).stdout.split()[0]
SERVER_PORT = int(os.environ.get("SERVER_PORT", 5000))

def sigterm_handler(signum, frame):
    print(f"Received SIGTERM ({signum}). Cleaning up...")

    add_cmd = f"disable server {BACKEND}/{SERVER_NAME}"
    print(f"Sending command: {add_cmd}")
    add_res = send_haproxy_command(add_cmd, HAPROXY_API_HOST, HAPROXY_API_PORT)
    print(f"Response: {add_res.strip()}")

    add_cmd = f"shutdown sessions server {BACKEND}/{SERVER_NAME}"
    print(f"Sending command: {add_cmd}")
    add_res = send_haproxy_command(add_cmd, HAPROXY_API_HOST, HAPROXY_API_PORT)
    print(f"Response: {add_res.strip()}")

    add_cmd = f"wait srv-removable {BACKEND}/{SERVER_NAME} 5s"
    print(f"Sending command: {add_cmd}")
    add_res = send_haproxy_command(add_cmd, HAPROXY_API_HOST, HAPROXY_API_PORT)
    print(f"Response: {add_res.strip()}")

    add_cmd = f"del server {BACKEND}/{SERVER_NAME} 5s"
    print(f"Sending command: {add_cmd}")
    add_res = send_haproxy_command(add_cmd, HAPROXY_API_HOST, HAPROXY_API_PORT)
    print(f"Response: {add_res.strip()}")

    sys.exit(0)

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

def send_haproxy_command(cmd: str, apihost,apiport) -> str:
    """Opens a short-lived TCP connection to HAProxy, sends a command, and returns the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        s.connect((apihost, apiport))

        # HAProxy commands over the Runtime API must end with a newline
        s.sendall(f"{cmd}\n".encode("utf-8"))

        response = []
        while True:
            data = s.recv(4096)
            if not data:
                break
            response.append(data.decode("utf-8"))

        return "".join(response)


def wait_for_haproxy(timeout: int = 30, interval: int = 2, apihost="127.0.0.1", apiport: int = 99999) -> bool:
    """Polls HAProxy Runtime API until it answers correctly or hits a timeout."""
    print(
        f"Waiting for HAProxy Runtime API at {apihost}:{apiport}..."
    )
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            # 'show info' is an excellent lightweight command to test if HAProxy is active
            res = send_haproxy_command("show info", apihost, apiport)
            if "Version" in res:
                print("HAProxy is running and Runtime API is active.")
                return True
        except (socket.error, socket.timeout):
            # HAProxy isn't up yet or refusing connections
            pass
        time.sleep(interval)

    print("Timed out waiting for HAProxy.")
    return False


def main():

    signal.signal(signal.SIGTERM, sigterm_handler)

    #if not wait_for_haproxy(30, 2, HAPROXY_API_HOST, HAPROXY_API_PORT):
    #    return

    # 1. Add the server to the backend dynamically
    # Syntax: add server <backend>/<name> [settings]
    add_cmd = f"add server {BACKEND}/{SERVER_NAME} {SERVER_IP}:{SERVER_PORT} check"
    print(f"Sending command: {add_cmd}")
    add_res = send_haproxy_command(add_cmd, HAPROXY_API_HOST, HAPROXY_API_PORT)
    print(f"Response: {add_res.strip()}")

    # 2. Dynamic servers initialize in a 'down/disabled' state. Enable it to put it into rotation.
    enable_cmd = f"enable server {BACKEND}/{SERVER_NAME}"
    print(f"Sending command: {enable_cmd}")
    enable_res = send_haproxy_command(enable_cmd, HAPROXY_API_HOST, HAPROXY_API_PORT)
    print(f"Response: {enable_res.strip()}")

    # 3. Health checks on dynamic servers start disabled; turn them on.
    health_cmd = f"enable health {BACKEND}/{SERVER_NAME}"
    print(f"Sending command: {health_cmd}")
    health_res = send_haproxy_command(health_cmd, HAPROXY_API_HOST, HAPROXY_API_PORT)
    print(f"Response: {health_res.strip()}")

    app.run(host="0.0.0.0", port=SERVER_PORT)


if __name__ == "__main__":
    main()