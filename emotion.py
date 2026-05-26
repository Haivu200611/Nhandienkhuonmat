import os
from tkinter import *
from PIL import Image, ImageTk
import cv2

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
            "fear": "scared",
            "scared": "scared",
            "happy": "happy",
            "sad": "sad",
            "surprise": "surprise",
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
    root.config(bg="#0f172a")

    music_player = EmotionMusicPlayer(cwd)

    emotion_vi_map = {
        "angry": "Giận dữ",
        "disgust": "Ghê tởm",
        "scared": "Sợ hãi",
        "happy": "Vui vẻ",
        "sad": "Buồn bã",
        "surprised": "Ngạc nhiên",
        "neutral": "Bình thường",
    }
    emotion_vi_map["fear"] = emotion_vi_map["scared"]
    emotion_vi_map["surprise"] = emotion_vi_map["surprised"]

    ui_state = {
        "running": False,
        "stop_requested": False,
        "current_music_emotion": None,
        "latest_music_status": "",
    }

    header = Label(
        root,
        text="EMOLAYER - NHẬN DIỆN CẢM XÚC VÀ GỢI Ý THỜI GIAN THỰC",
        font=("Segoe UI Semibold", 16),
        fg="#f8fafc",
        bg="#0f172a",
    )
    header.pack(fill=X, padx=16, pady=(14, 8))

    body = Frame(root, bg="#0f172a")
    body.pack(fill=BOTH, expand=True, padx=14, pady=(0, 10))

    video_panel = LabelFrame(
        body,
        text="Live Feed",
        font=("Segoe UI Semibold", 11),
        fg="#e2e8f0",
        bg="#1e293b",
        bd=1,
        relief="solid",
        padx=8,
        pady=8,
    )
    video_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

    video_label = Label(
        video_panel,
        text="Nhấn Start để bắt đầu nhận diện",
        font=("Segoe UI", 12),
        fg="#cbd5e1",
        bg="#0b1220",
        width=140,
        height=26,
    )
    video_label.pack(fill=BOTH, expand=True)

    right_panel = LabelFrame(
        body,
        text="Kết Quả & Phản Hồi",
        font=("Segoe UI Semibold", 11),
        fg="#e2e8f0",
        bg="#1e293b",
        bd=1,
        relief="solid",
        padx=10,
        pady=10,
    )
    right_panel.pack(side=RIGHT, fill=Y)

    emotion_label = Label(
        right_panel,
        text="Cảm xúc: --",
        font=("Segoe UI Semibold", 14),
        fg="#f8fafc",
        bg="#1e293b",
        anchor="w",
        justify=LEFT,
    )
    emotion_label.pack(fill=X, pady=(2, 8))

    music_status_label = Label(
        right_panel,
        text="Nhạc: --",
        font=("Segoe UI", 10),
        fg="#facc15",
        bg="#1e293b",
        wraplength=360,
        anchor="w",
        justify=LEFT,
    )
    music_status_label.pack(fill=X, pady=(0, 10))

    response_title = Label(
        right_panel,
        text="Phản hồi tiếng Việt",
        font=("Segoe UI Semibold", 11),
        fg="#93c5fd",
        bg="#1e293b",
        anchor="w",
        justify=LEFT,
    )
    response_title.pack(fill=X, pady=(0, 6))

    response_text = Text(
        right_panel,
        wrap=WORD,
        font=("Segoe UI", 10),
        width=46,
        height=24,
        bg="#0b1220",
        fg="#e2e8f0",
        insertbackground="#e2e8f0",
        padx=12,
        pady=10,
        relief="flat",
    )
    response_text.pack(fill=BOTH, expand=True)
    response_text.config(state=DISABLED)

    action_bar = Frame(root, bg="#0f172a")
    action_bar.pack(fill=X, padx=14, pady=(0, 12))

    def update_response_panel(emotion, recommendation, music_status):
        if recommendation is None:
            content = (
                "Đang nhận diện cảm xúc...\n"
                "Khi cảm xúc ổn định, hệ thống sẽ hiển thị phản hồi tại đây."
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

        response_text.config(state=NORMAL)
        response_text.delete("1.0", END)
        response_text.insert(END, content)
        response_text.config(state=DISABLED)

    def render_frame(combined_view):
        if not root.winfo_exists():
            return

        rgb_frame = cv2.cvtColor(combined_view, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_frame)
        photo = ImageTk.PhotoImage(image=image)
        video_label.config(image=photo, text="")
        video_label.image = photo

        try:
            root.update_idletasks()
            root.update()
        except TclError:
            pass

    def on_emotion_update(emotion, recommendation):
        if emotion and emotion != ui_state["current_music_emotion"]:
            music_path, music_error = music_player.play_for_emotion(emotion)
            if music_error:
                ui_state["latest_music_status"] = music_error
            elif music_path:
                ui_state["latest_music_status"] = f"Đang phát: {os.path.basename(music_path)}"
            ui_state["current_music_emotion"] = emotion

        emotion_label.config(text=f"Cảm xúc: {emotion.upper()}")
        music_status_label.config(text=f"Nhạc: {ui_state['latest_music_status'] or '--'}")
        update_response_panel(emotion, recommendation, ui_state["latest_music_status"])

        try:
            root.update_idletasks()
            root.update()
        except TclError:
            pass

    def should_stop():
        return ui_state["stop_requested"] or not root.winfo_exists()

    def callback_start():
        if ui_state["running"]:
            return

        ui_state["running"] = True
        ui_state["stop_requested"] = False
        ui_state["current_music_emotion"] = None
        ui_state["latest_music_status"] = ""

        music_path, music_error = music_player.play_for_emotion("neutral")
        if music_error:
            ui_state["latest_music_status"] = music_error
        elif music_path:
            ui_state["latest_music_status"] = f"Đang phát: {os.path.basename(music_path)}"
            ui_state["current_music_emotion"] = "neutral"

        music_status_label.config(text=f"Nhạc: {ui_state['latest_music_status'] or '--'}")
        update_response_panel("neutral", None, ui_state["latest_music_status"])
        root.update()

        res = live_emotion.main(
            on_emotion_update=on_emotion_update,
            on_frame_update=render_frame,
            show_window=False,
            should_stop=should_stop,
        )

        ui_state["running"] = False
        emotion = res.get("emotion", "neutral")
        recommendation = res.get("recommendation")
        emotion_label.config(text=f"Cảm xúc: {emotion.upper()}")
        update_response_panel(emotion, recommendation, ui_state["latest_music_status"])

    def callback_stop_webcam():
        ui_state["stop_requested"] = True

    def callback_refresh():
        ui_state["stop_requested"] = True
        music_player.stop()
        ui_state["current_music_emotion"] = None
        ui_state["latest_music_status"] = ""
        emotion_label.config(text="Cảm xúc: --")
        music_status_label.config(text="Nhạc: --")
        update_response_panel("neutral", None, "")
        video_label.config(image="", text="Nhấn Start để bắt đầu nhận diện")
        video_label.image = None

    def callback_stop_music():
        music_player.stop()
        ui_state["latest_music_status"] = "Đã dừng nhạc."
        music_status_label.config(text=f"Nhạc: {ui_state['latest_music_status']}")
        update_response_panel("neutral", None, ui_state["latest_music_status"])

    def on_close():
        ui_state["stop_requested"] = True
        music_player.stop()
        root.destroy()

    root.title("EMOLAYER - AI Emotion Recommender")
    root.geometry("1366x760")
    root.minsize(1180, 680)
    root.resizable(width=True, height=True)
    root.protocol("WM_DELETE_WINDOW", on_close)

    Button(
        action_bar,
        text="Start - Nhận diện cảm xúc",
        command=callback_start,
        font=("Segoe UI Semibold", 10),
        bg="#22c55e",
        fg="#0f172a",
        activebackground="#16a34a",
        relief="flat",
        padx=14,
        pady=8,
    ).pack(side=LEFT, padx=(0, 8))

    Button(
        action_bar,
        text="Stop Webcam",
        command=callback_stop_webcam,
        font=("Segoe UI", 10),
        bg="#f59e0b",
        fg="#111827",
        activebackground="#d97706",
        relief="flat",
        padx=12,
        pady=8,
    ).pack(side=LEFT, padx=(0, 8))

    Button(
        action_bar,
        text="Refresh",
        command=callback_refresh,
        font=("Segoe UI", 10),
        bg="#e2e8f0",
        fg="#111827",
        activebackground="#cbd5e1",
        relief="flat",
        padx=12,
        pady=8,
    ).pack(side=LEFT, padx=(0, 8))

    Button(
        action_bar,
        text="Stop nhạc",
        command=callback_stop_music,
        font=("Segoe UI", 10),
        bg="#f87171",
        fg="#111827",
        activebackground="#ef4444",
        relief="flat",
        padx=12,
        pady=8,
    ).pack(side=LEFT)

    root.mainloop()


main()

