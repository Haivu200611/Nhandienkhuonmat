import os
from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
# import vlc  # Commented out: VLC library not needed
from recommender import EmotionRecommender

happy = cv2.imread("emojis/happy.jpg")
if happy is not None:
    happy = cv2.resize(happy, (100, 100), interpolation=cv2.INTER_AREA)

sad = cv2.imread("emojis/sad.jpg")
if sad is not None:
    sad = cv2.resize(sad, (100, 100), interpolation=cv2.INTER_AREA)

angry = cv2.imread("emojis/angry.jpg")
if angry is not None:
    angry = cv2.resize(angry, (100, 100), interpolation=cv2.INTER_AREA)

surprise = cv2.imread("emojis/surprise.jpg")
if surprise is not None:
    surprise = cv2.resize(surprise, (100, 100), interpolation=cv2.INTER_AREA)

nuetral = cv2.imread("emojis/nuetral.jpg")
if nuetral is not None:
    nuetral = cv2.resize(nuetral, (100, 100), interpolation=cv2.INTER_AREA)

disgust = cv2.imread("emojis/disgust.jpg")
if disgust is not None:
    disgust = cv2.resize(disgust, (100, 100), interpolation=cv2.INTER_AREA)

scared = cv2.imread("emojis/scared.jpg")
if scared is not None:
    scared = cv2.resize(scared, (100, 100), interpolation=cv2.INTER_AREA)

recommender = EmotionRecommender()


def main(on_emotion_update=None, on_frame_update=None, show_window=True, should_stop=None):
    detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
    emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'
    output_dir = os.path.join(os.getcwd(), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "output.jpg")

    face_detection = cv2.CascadeClassifier(detection_model_path)
    emotion_classifier = load_model(emotion_model_path, compile=False)
    EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

    if show_window:
        cv2.namedWindow("Emotion Recognition")
    camera = cv2.VideoCapture(0)

    frame_count = 0
    stable_emotion = None
    recommendation = None
    last_frame = None

    while True:
        if should_stop is not None and should_stop():
            break

        ok, frame = camera.read()
        if not ok or frame is None:
            break

        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detection.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        canvas = np.zeros((350, 300, 3), dtype="uint8")
        frameClone = frame.copy()
        emoji_frame = np.zeros((350, 350, 3), dtype="uint8")

        if len(faces) > 0:
            faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = emotion_classifier.predict(roi)[0]
            label = EMOTIONS[preds.argmax()]

            frame_count += 1
            if frame_count % 30 == 0:
                stable_emotion = label
                recommendation = recommender.get_full_recommendation(label)
                if on_emotion_update is not None:
                    on_emotion_update(stable_emotion, recommendation)

            for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
                text = "{}: {:.2f}%".format(emotion, prob * 100)
                w = int(prob * 300)
                cv2.rectangle(canvas, (7, (i * 35) + 5), (w, (i * 35) + 35), (0, 0, 255), -1)
                cv2.putText(canvas, text, (10, (i * 35) + 23), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)

            cv2.putText(frameClone, label.upper(), (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (0, 255, 0), 2)

            emoji_map = {
                "happy": happy,
                "sad": sad,
                "angry": angry,
                "neutral": nuetral,
                "surprised": surprise,
                "disgust": disgust,
                "scared": scared
            }
            if label in emoji_map and emoji_map[label] is not None:
                emoji_frame = cv2.resize(emoji_map[label], (350, 350), interpolation=cv2.INTER_AREA)
        else:
            frame_count = 0
            stable_emotion = None
            recommendation = None

        frame_resized = cv2.resize(frameClone, (500, 350), interpolation=cv2.INTER_AREA)
        combined_view = cv2.hconcat([emoji_frame, frame_resized, canvas])
        last_frame = frameClone

        if on_frame_update is not None:
            on_frame_update(combined_view)

        if show_window:
            cv2.imshow("Emotion Recognition", combined_view)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    if last_frame is not None:
        cv2.imwrite(output_path, last_frame)

    result = {
        "emotion": stable_emotion if stable_emotion else "neutral",
        "recommendation": recommendation,
        "output_path": output_path,
    }

    camera.release()
    cv2.destroyAllWindows()
    return result
