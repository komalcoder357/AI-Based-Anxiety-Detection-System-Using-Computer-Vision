from flask import Flask, render_template, Response, jsonify, request, redirect, url_for, session
import cv2
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = "muzamil_secret_key"

# ================= CAMERA =================
camera = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
smile_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_smile.xml"
)

# ================= GLOBAL STATE =================
current_data = {"anxiety": 40, "level": "LOW"}
current_anxiety = 40
last_face_area = None
last_update = time.time()
no_face_frames = 0


# ================= REAL & RESPONSIVE ANXIETY LOGIC =================
def calculate_anxiety(face_gray, face_area, smile_detected):
    global last_face_area, current_anxiety, no_face_frames

    prev = current_anxiety

    # ----- FACE MOVEMENT -----
    if last_face_area is not None and face_area > 0:
        movement_ratio = abs(face_area - last_face_area) / face_area
        movement_score = min(movement_ratio * 40, 25)  # strong & visible
    else:
        movement_score = 3  # idle baseline

    last_face_area = face_area

    # ----- SMILE EFFECT -----
    smile_score = 12 if smile_detected else 0

    # ----- NO FACE PENALTY -----
    face_penalty = min(no_face_frames * 1.2, 25)

    # ----- RAW ANXIETY -----
    anxiety_raw = prev + movement_score - smile_score + face_penalty
    anxiety_raw = max(10, min(100, anxiety_raw))  # allow down & up

    # ----- SMOOTHING (NOT FREEZE) -----
    anxiety = int(0.60 * prev + 0.40 * anxiety_raw)
    current_anxiety = anxiety

    # ----- LEVEL -----
    if anxiety < 35:
        level = "LOW"
    elif anxiety < 70:
        level = "MODERATE"
    else:
        level = "HIGH"

    return anxiety, level


# ================= VIDEO STREAM =================
def generate_frames():
    global last_update, no_face_frames

    while True:
        success, frame = camera.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # ----- NO FACE -----
        if len(faces) == 0:
            no_face_frames += 1
        else:
            no_face_frames = 0

        for (x, y, w, h) in faces:
            face = gray  [y:y+h, x:x+w]
            smiles = smile_cascade.detectMultiScale(face, 1.7, 22)

            anxiety, level = calculate_anxiety(
                face_gray=face,
                face_area=w * h,
                smile_detected=len(smiles) > 0
            )

            if time.time() - last_update > 1:
                current_data["anxiety"] = anxiety
                current_data["level"] = level
                last_update = time.time()

            color = (0,255,0) if anxiety < 40 else (0,255,255) if anxiety < 70 else (0,0,255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(
                frame,
                f"{anxiety}% {level}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

        _, buffer = cv2.imencode(".jpg", frame)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            buffer.tobytes() +
            b"\r\n"
        )


# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")

        if not username:
            return render_template("login.html", error="Enter your name")

        session["user"] = username
        session["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session["start_anxiety"] = current_data["anxiety"]

        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ================= DASHBOARD =================
@app.route("/")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", user=session["user"])


# ================= VIDEO ROUTE =================
@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ================= LIVE DATA =================
@app.route("/data")
def data():
    return jsonify(current_data)


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    print("\n===== SESSION SUMMARY =====")
    print("User:", session.get("user"))
    print("Start Time:", session.get("start_time"))
    print("Start Anxiety:", session.get("start_anxiety"))
    print("End Anxiety:", current_data["anxiety"])
    print("===========================\n")

    session.clear()
    return redirect(url_for("login"))


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)