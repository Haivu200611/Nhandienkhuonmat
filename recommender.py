import random


class EmotionRecommender:
    EMOTION_MAP = {
        "angry": "Anger",
        "disgust": "Disgust",
        "scared": "Fear",
        "happy": "Happy",
        "sad": "Sad",
        "surprised": "Surprise",
        "neutral": "Neutral",
    }

    def __init__(self):
        self.recommendations = self._load_recommendations()

    def _load_recommendations(self):
        return {
            "Happy": {
                "message": "Bạn đang vui! Hãy tận hưởng khoảnh khắc này!",
                "music": [
                    "Happy - Pharrell Williams",
                    "Can't Stop The Feeling - Justin Timberlake",
                    "Uptown Funk - Bruno Mars",
                    "Walking On Sunshine - Katrina & The Waves",
                ],
                "activities": [
                    "Gọi điện cho bạn bè",
                    "Đi dạo ngoài trời",
                    "Chụp ảnh kỷ niệm",
                    "Xem phim hài",
                ],
                "quotes": [
                    "Happiness is not something ready made. It comes from your own actions.",
                    "The most wasted of all days is one without laughter.",
                ],
                "movies": [
                    "The Intouchables",
                    "Forrest Gump",
                    "The Grand Budapest Hotel",
                ],
                "color": (0, 255, 0),
            },
            "Sad": {
                "message": "Bạn buồn à? Mọi chuyện rồi sẽ ổn thôi!",
                "music": [
                    "Someone Like You - Adele",
                    "Fix You - Coldplay",
                    "Let Her Go - Passenger",
                    "Nuvole Bianche - Ludovico Einaudi",
                ],
                "activities": [
                    "Viết nhật ký",
                    "Nghe podcast truyền cảm hứng",
                    "Tập yoga nhẹ nhàng",
                    "Nấu món ăn yêu thích",
                ],
                "quotes": [
                    "Even the darkest night will end and the sun will rise.",
                    "It's okay to not be okay. Tomorrow is a new day.",
                ],
                "movies": [
                    "The Pursuit of Happyness",
                    "Good Will Hunting",
                    "A Beautiful Mind",
                ],
                "color": (255, 0, 0),
            },
            "Anger": {
                "message": "Bình tĩnh nào! Hãy thử hít thở sâu nhé.",
                "music": [
                    "Weightless - Marconi Union",
                    "Clair de Lune - Debussy",
                    "Gymnopedie No.1 - Erik Satie",
                    "River Flows In You - Yiruma",
                ],
                "activities": [
                    "Hít thở sâu 4-7-8",
                    "Đi bộ 15 phút",
                    "Uống trà ấm",
                    "Viết ra điều khiến bạn bực bội",
                ],
                "quotes": [
                    "For every minute you remain angry, you give up sixty seconds of peace.",
                    "When you are angry, think before you speak.",
                ],
                "movies": [
                    "Inside Out",
                    "Peaceful Warrior",
                    "The Secret Life of Walter Mitty",
                ],
                "color": (0, 0, 255),
            },
            "Fear": {
                "message": "Đừng sợ! Bạn mạnh mẽ hơn bạn nghĩ.",
                "music": [
                    "Brave - Sara Bareilles",
                    "Fight Song - Rachel Platten",
                    "Stronger - Kelly Clarkson",
                    "Eye of the Tiger - Survivor",
                ],
                "activities": [
                    "Thiền 10 phút",
                    "Gọi cho người thân",
                    "Tập thể dục nhẹ",
                    "Đọc sách truyền cảm hứng",
                ],
                "quotes": [
                    "Fear is only temporary. Regret lasts forever.",
                    "Courage is not the absence of fear, but the triumph over it.",
                ],
                "movies": [
                    "The King's Speech",
                    "Hidden Figures",
                    "Soul",
                ],
                "color": (128, 0, 128),
            },
            "Surprise": {
                "message": "Wow! Bất ngờ quá! Hãy khám phá thêm nhé!",
                "music": [
                    "Unwritten - Natasha Bedingfield",
                    "Adventure of a Lifetime - Coldplay",
                    "On Top of the World - Imagine Dragons",
                    "Best Day Of My Life - American Authors",
                ],
                "activities": [
                    "Khám phá địa điểm mới",
                    "Thử món ăn lạ",
                    "Học kỹ năng mới",
                    "Chơi game giải đố",
                ],
                "quotes": [
                    "Life is full of surprises. Embrace them!",
                    "The unexpected is what makes life interesting.",
                ],
                "movies": [
                    "The Truman Show",
                    "Inception",
                    "Interstellar",
                ],
                "color": (255, 255, 0),
            },
            "Disgust": {
                "message": "Hãy chuyển hướng sự chú ý sang điều tích cực hơn.",
                "music": [
                    "Three Little Birds - Bob Marley",
                    "Here Comes The Sun - The Beatles",
                    "Don't Worry Be Happy - Bobby McFerrin",
                    "Good Vibrations - The Beach Boys",
                ],
                "activities": [
                    "Rời khỏi môi trường hiện tại",
                    "Nghe podcast hài",
                    "Dọn dẹp không gian sống",
                    "Vẽ tranh hoặc tô màu",
                ],
                "quotes": [
                    "Focus on the good. It's always there.",
                    "Change your thoughts and you change your world.",
                ],
                "movies": [
                    "The Good Place",
                    "Ted Lasso",
                    "Schitt's Creek",
                ],
                "color": (0, 255, 255),
            },
            "Neutral": {
                "message": "Trạng thái ổn định! Hãy thử làm điều gì đó mới mẻ.",
                "music": [
                    "Lo-fi Hip Hop Playlist",
                    "Acoustic Covers",
                    "Jazz Classics",
                    "Nature Sounds",
                ],
                "activities": [
                    "Đọc sách",
                    "Học ngôn ngữ mới",
                    "Xem TED Talks",
                    "Lên kế hoạch tuần mới",
                ],
                "quotes": [
                    "Every day is a new opportunity to learn something.",
                    "Stay curious. Stay hungry. Stay foolish.",
                ],
                "movies": [
                    "The Social Network",
                    "The Imitation Game",
                    "Limitless",
                ],
                "color": (200, 200, 200),
            },
        }

    def get_recommendation(self, emotion):
        emotion_label = self.EMOTION_MAP.get(emotion, "Neutral")
        return self.recommendations.get(emotion_label, self.recommendations["Neutral"])

    def get_random_item(self, category, emotion):
        rec = self.get_recommendation(emotion)
        items = rec.get(category, [])
        return random.choice(items) if items else "Không có gợi ý"

    def get_full_recommendation(self, emotion):
        rec = self.get_recommendation(emotion)
        return {
            "emotion": emotion,
            "message": rec["message"],
            "music": random.choice(rec["music"]),
            "activity": random.choice(rec["activities"]),
            "quote": random.choice(rec["quotes"]),
            "movie": random.choice(rec["movies"]),
            "color": rec["color"],
        }
