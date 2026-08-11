from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        os.environ["DATABASE_URL"]
    )


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS licenses (
            id SERIAL PRIMARY KEY,
            android_id TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def check_id(android_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM licenses WHERE android_id = %s LIMIT 1",
        (android_id,)
    )

    exists = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return exists


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "API is running"
    })


@app.route("/check-id", methods=["POST"])
def check_license():
    data = request.get_json(silent=True)

    print("Received:", data)

    if not data:
        return jsonify({
            "licensed": False,
            "message": "No data received"
        }), 400

    android_id = (
        data.get("androidId")
        or data.get("android_id")
        or data.get("id")
    )

    if not android_id:
        return jsonify({
            "licensed": False,
            "message": "Android ID required"
        }), 400

    exists = check_id(android_id)

    print(
        f"[LICENSE CHECK] Android ID: {android_id}"
        f" -> licensed={exists}"
    )

    return jsonify({
        "licensed": exists
    }), 200


@app.route("/add-id", methods=["POST"])
def add_id():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    android_id = (
        data.get("androidId")
        or data.get("android_id")
        or data.get("id")
    )

    if not android_id:
        return jsonify({
            "success": False,
            "message": "Android ID required"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO licenses (android_id)
            VALUES (%s)
            ON CONFLICT (android_id) DO NOTHING
            """,
            (android_id,)
        )

        conn.commit()

        return jsonify({
            "success": True,
            "message": "ID added"
        }), 200

    finally:
        cursor.close()
        conn.close()


@app.route("/delete-id", methods=["POST"])
def delete_id():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    android_id = (
        data.get("androidId")
        or data.get("android_id")
        or data.get("id")
    )

    if not android_id:
        return jsonify({
            "success": False,
            "message": "Android ID required"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM licenses WHERE android_id = %s",
            (android_id,)
        )

        deleted = cursor.rowcount > 0
        conn.commit()

        return jsonify({
            "success": deleted,
            "message": "ID deleted" if deleted else "ID not found"
        }), 200

    finally:
        cursor.close()
        conn.close()


# مهم لـ Render / Gunicorn
create_table()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
