import cv2
import numpy as np
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_INDEX = """
<!DOCTYPE html>
<html>
  <head>
    <title>Capture Image</title>
  </head>
  <body>
    <h1>Webcam Capture Demo</h1>
    <p>
      When you click "Capture", the server will open a local OpenCV window.<br>
      Stand in front of your webcam and press ESC to close the window.<br>
      The final image will be saved to D:/hand_Right.jpg.
    </p>

    <form action="/capture" method="post">
      <button type="submit">Capture</button>
    </form>
  </body>
</html>
"""

@app.route("/")
def index():
    # Simple page with a "Capture" button
    return render_template_string(HTML_INDEX)

@app.route("/capture", methods=["POST"])
def capture():
    # This route triggers the webcam capture when the user clicks "Capture"
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Could not open webcam (is it connected?)"

    hand = "Right"  # or "Left", etc.

    while True:
        ret, frame = cap.read()
        if not ret:
            # Could not grab frame
            break

        # Flip horizontally for a mirror-like view
        img = cv2.flip(frame, 1)

        # Split or crop: capturing right half or left half
        h, w, _ = img.shape
        midpoint = w // 2
        if hand == "Right":
            img = img[:, midpoint:w]
        else:
            img = img[:, 0:midpoint]

        # Add instructions overlay
        instruction1 = "Hold your hand inside the box"
        instruction2 = "Press ESC to quit."

        cv2.putText(img, instruction1, (10, 30),
                    cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,0,255), 2, cv2.LINE_AA)
        cv2.putText(img, instruction2, (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,0,255), 2, cv2.LINE_AA)

        cv2.imshow("Webcam", img)

        # Press ESC to quit
        if cv2.waitKey(1) & 0xFF == 27:
            # ESC is pressed
            # We'll save the final frame at this moment
            filename = f"D:/hand_{hand}.jpg"
            cv2.imwrite(filename, img)
            break

    cap.release()
    cv2.destroyAllWindows()

    return f"Image captured and saved to D:/hand_{hand}.jpg!"

if __name__ == "__main__":
    # Run the Flask dev server on localhost:5000
    app.run(debug=True)
