import os
from tkinter import *
from PIL import Image, ImageTk

import live_emotion

try:
    import vlc
except Exception:
    vlc = None


class EmotionMusicPlayer:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.instance = None
        self.player = None
        if vlc is not None:
            try:
                self.instance = vlc.Instance()
            except Exception:
                self.instance = None

    def _resolve_music_path(self, emotion):
        file_map = {
            "angry": "angry",
            "disgust": "disgust",
            "scared": "scared",
            "happy": "happy",
            "sad": "sad",
            "surprised": "surprise",
            "neutral": "neutral",
        }
        key = file_map.get(emotion, "neutral")
        return os.path.join(self.base_dir, "music", f"{key}.mp3")

    def stop(self):
        if self.player is not None:
            try:
                self.player.stop()
            except Exception:
                pass
        self.player = None

    def play_for_emotion(self, emotion):
        music_path = self._resolve_music_path(emotion)
        if not os.path.exists(music_path):
            return None, f"Không tìm thấy file nhạc: {music_path}"

        self.stop()
        if self.instance is not None:
            try:
                media = self.instance.media_new(music_path)
                self.player = self.instance.media_player_new()
                self.player.set_media(media)
                self.player.play()
                return music_path, None
            except Exception as exc:
                self.player = None
                return None, f"Lỗi phát nhạc bằng VLC: {exc}"

        try:
            os.startfile(music_path)
            return music_path, "Không dùng được VLC, đã mở file bằng trình phát mặc định."
        except Exception as exc:
            return None, f"Không thể phát nhạc: {exc}"


def main():
    cwd = os.getcwd()
    root = Tk()
    root.config(bg="green")

    music_player = EmotionMusicPlayer(cwd)
    vi_window = None
    vi_text = None

    emotion_vi_map = {
        "angry": "Giận dữ",
        "disgust": "Ghê tởm",
        "scared": "Sợ hãi",
        "happy": "Vui vẻ",
        "sad": "Buồn bã",
        "surprised": "Ngạc nhiên",
        "neutral": "Bình thường",
    }

    header = Label(root, text="NHAN DIEN CAM XUC - AI RECOMMENDER", font=("Arial Bold", 14), fg="red", bg="green")
    header.pack(pady=6)

    bg_path = os.path.join(cwd, "bg2.jpg")
    if os.path.exists(bg_path):
        image = Image.open(bg_path)
        photo = ImageTk.PhotoImage(image)
        image_label = Label(root, image=photo)
        root.image = photo
        image_label.pack()
    else:
        image_label = Label(root, text="EMOLAYER", font=("Arial Bold", 24), bg="green", fg="white")
        image_label.pack()
        root.image = None

    emotion_label = Label(root, text="Cảm xúc: --", font=("Arial Bold", 14), bg="green", fg="white")
    emotion_label.pack(pady=8)

    music_status_label = Label(root, text="Nhạc: --", font=("Arial", 10), bg="green", fg="yellow", wraplength=420)
    music_status_label.pack(pady=4)

    hint_label = Label(
        root,
        text="Nhấn Start để mở webcam.\nCửa sổ phản hồi tiếng Việt sẽ tách riêng và cập nhật ngay khi nhận diện.",
        font=("Arial", 10),
        bg="green",
        fg="cyan",
        justify="center",
    )
    hint_label.pack(pady=8)

    def create_or_focus_response_window():
        nonlocal vi_window, vi_text

        if vi_window is None or not vi_window.winfo_exists():
            vi_window = Toplevel(root)
            vi_window.title("Phan hoi tieng Viet")
            vi_window.geometry("560x420")

            title = Label(vi_window, text="Phản hồi tiếng Việt (Realtime)", font=("Arial Bold", 12))
            title.pack(pady=8)

            vi_text = Text(vi_window, wrap=WORD, font=("Arial", 10), padx=12, pady=10)
            vi_text.pack(fill=BOTH, expand=True, padx=10, pady=8)
        else:
            vi_window.deiconify()
            vi_window.lift()

    def update_response_window(emotion, recommendation, music_status):
        if vi_window is None or not vi_window.winfo_exists() or vi_text is None:
            return

        if recommendation is None:
            content = (
                "Đang nhận diện cảm xúc...\n"
                "Khi cảm xúc ổn định, hệ thống sẽ trả lời tại đây ngay lập tức."
            )
        else:
            emotion_text = emotion_vi_map.get(emotion, emotion)
            content = (
                f"Trạng thái cảm xúc: {emotion_text}\n\n"
                f"Phản hồi: {recommendation['message']}\n\n"
                f"Gợi ý nhạc: {recommendation['music']}\n"
                f"Gợi ý hoạt động: {recommendation['activity']}\n"
                f"Câu nói: {recommendation['quote']}\n"
                f"Gợi ý phim: {recommendation['movie']}"
            )

        if music_status:
            content += f"\n\nTrạng thái nhạc: {music_status}"

        vi_text.config(state=NORMAL)
        vi_text.delete("1.0", END)
        vi_text.insert(END, content)
        vi_text.config(state=DISABLED)

    def callback():
        current_music_emotion = None
        latest_music_status = ""

        create_or_focus_response_window()
        update_response_window("neutral", None, "")

        def on_emotion_update(emotion, recommendation):
            nonlocal current_music_emotion, latest_music_status

            if emotion and emotion != current_music_emotion:
                music_path, music_error = music_player.play_for_emotion(emotion)
                if music_error:
                    latest_music_status = music_error
                elif music_path:
                    latest_music_status = f"Đang phát: {os.path.basename(music_path)}"
                current_music_emotion = emotion

            emotion_label.config(text=f"Cảm xúc: {emotion.upper()}")
            music_status_label.config(text=f"Nhạc: {latest_music_status or '--'}")
            update_response_window(emotion, recommendation, latest_music_status)
            root.update()

        # Bật nhạc nền ngay khi mở webcam.
        music_path, music_error = music_player.play_for_emotion("neutral")
        if music_error:
            latest_music_status = music_error
        elif music_path:
            latest_music_status = f"Đang phát: {os.path.basename(music_path)}"
            current_music_emotion = "neutral"

        music_status_label.config(text=f"Nhạc: {latest_music_status or '--'}")
        update_response_window("neutral", None, latest_music_status)
        root.update()

        res = live_emotion.main(on_emotion_update=on_emotion_update)
        emotion = res.get("emotion", "neutral")
        recommendation = res.get("recommendation")

        emotion_label.config(text=f"Cảm xúc: {emotion.upper()}")
        update_response_window(emotion, recommendation, latest_music_status)

        output_path = res.get("output_path", os.path.join(cwd, "outputs", "output.jpg"))
        if not os.path.exists(output_path):
            fallback_path = os.path.join(cwd, "output.jpg")
            if os.path.exists(fallback_path):
                output_path = fallback_path
        if os.path.exists(output_path):
            image = Image.open(output_path)
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            root.image = photo

    def callback_refresh():
        music_player.stop()
        emotion_label.config(text="Cảm xúc: --")
        music_status_label.config(text="Nhạc: --")

        if vi_window is not None and vi_window.winfo_exists():
            vi_window.destroy()

    def on_close():
        music_player.stop()
        if vi_window is not None and vi_window.winfo_exists():
            vi_window.destroy()
        root.destroy()

    root.title("EMOLAYER - AI Emotion Recommender")
    root.geometry("480x640")
    root.resizable(width=True, height=True)
    root.protocol("WM_DELETE_WINDOW", on_close)

    Button(text="Start - Nhan dien cam xuc", command=callback, font=("Arial", 10), bg="yellow").pack(side=TOP, padx=10, pady=6)
    Button(text="Refresh", command=callback_refresh, font=("Arial", 10)).pack(side=TOP, padx=10, pady=6)
    Button(text="Stop nhac", command=music_player.stop, font=("Arial", 10)).pack(side=TOP, padx=10, pady=6)

    root.mainloop()


main()
