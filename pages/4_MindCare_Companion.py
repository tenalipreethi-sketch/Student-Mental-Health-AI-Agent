from __future__ import annotations

import random
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.game_data import (
    GAME_COLLECTIONS,
    GAME_MENU,
)


# ============================================================
# 1. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MindCare Companion",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# 2. PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

HISTORY_PATH = (
    PROJECT_DIR
    / "records"
    / "prediction_history.csv"
)


# ============================================================
# 3. CONSTANTS
# ============================================================

WELCOME_MESSAGE = """
Heyy 👋 I'm **MindCare Companion** 💙

Nenu only precautions cheppe boring bot kaadhu 😭😂

Manam:

💬 Casual ga chat cheyyachu  
🎮 Games aadachu  
🧩 Riddles solve cheyyachu  
🎬 Telugu movie guessing aadachu  
🕵️ Mini mysteries solve cheyyachu  
⚡ Rapid fire aadachu  
😌 Relaxation try cheyyachu  
📚 Study stress gurinchi matladachu  
📊 Nee latest assessment explain cheyyachu  

**Ippudu nee mood ela undhi?** 😌
"""


ROMAN_TELUGU_WORDS = {
    "enti",
    "enduku",
    "ela",
    "em",
    "emi",
    "cheppu",
    "cheyyi",
    "cheddam",
    "chestha",
    "kavali",
    "vadhu",
    "ledu",
    "ledhu",
    "avunu",
    "avnu",
    "kadhu",
    "kaadhu",
    "baledhu",
    "baaledhu",
    "bagundi",
    "bagundhi",
    "naku",
    "naaku",
    "nuv",
    "nuvvu",
    "manam",
    "bro",
    "ra",
    "aadali",
    "adali",
    "aadudham",
    "adudham",
    "bore",
    "koduthundi",
    "undhi",
    "undi",
    "haa",
    "ha",
    "emo",
    "ayyo",
    "aithe",
    "inka",
    "ippudu",
    "mood",
    "nanna",
}


GAME_LABELS = {
    "movie": "🎬 Telugu Movie Guessing",
    "emoji_movie": "🎭 Emoji Movie Guessing",
    "riddle": "🧩 Riddle",
    "logic": "🧠 Logic Challenge",
    "mystery": "🕵️ Mini Mystery",
    "rapid_fire": "⚡ Rapid Fire",
    "would_you_rather": "🤔 Would You Rather",
    "fun_question": "😂 Random Fun Question",
}


ANSWER_BASED_GAMES = {
    "movie",
    "emoji_movie",
    "riddle",
    "logic",
    "mystery",
}


OPEN_RESPONSE_GAMES = {
    "rapid_fire",
    "would_you_rather",
    "fun_question",
}


# ============================================================
# 4. SESSION STATE
# ============================================================

if "companion_messages" not in st.session_state:
    st.session_state.companion_messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE,
        }
    ]


if "game_mode" not in st.session_state:
    st.session_state.game_mode = None


if "game_data" not in st.session_state:
    st.session_state.game_data = None


if "hint_index" not in st.session_state:
    st.session_state.hint_index = 0


if "asked_question_ids" not in st.session_state:
    st.session_state.asked_question_ids = {
        game_name: []
        for game_name in GAME_COLLECTIONS
    }


if "game_score" not in st.session_state:
    st.session_state.game_score = 0


if "game_streak" not in st.session_state:
    st.session_state.game_streak = 0


if "preferred_difficulty" not in st.session_state:
    st.session_state.preferred_difficulty = "all"


# ============================================================
# 5. BASIC HELPERS
# ============================================================

def normalize(text: str) -> str:

    return (
        str(text)
        .lower()
        .strip()
        .replace(".", "")
        .replace(",", "")
        .replace("!", "")
        .replace("?", "")
        .replace("-", " ")
    )


def contains_any(
    text: str,
    words: list[str],
) -> bool:

    lowered = text.lower()

    return any(
        word in lowered
        for word in words
    )


def add_message(
    role: str,
    content: str,
) -> None:

    st.session_state.companion_messages.append(
        {
            "role": role,
            "content": content,
        }
    )


# ============================================================
# 6. LANGUAGE STYLE
# ============================================================

def detect_chat_style(
    text: str,
) -> str:

    cleaned = (
        text.lower()
        .replace("?", " ")
        .replace("!", " ")
        .replace(".", " ")
        .replace(",", " ")
    )

    words = set(
        cleaned.split()
    )

    matches = words.intersection(
        ROMAN_TELUGU_WORDS
    )

    if matches:
        return "mixed"

    return "english"


def style_reply(
    english: str,
    mixed: str,
    user_text: str,
) -> str:

    if detect_chat_style(
        user_text
    ) == "mixed":

        return mixed

    return english


# ============================================================
# 7. ASSESSMENT HELPERS
# ============================================================

def load_latest_assessment():

    if "latest_assessment" in st.session_state:

        latest = st.session_state[
            "latest_assessment"
        ]

        if isinstance(
            latest,
            pd.Series,
        ):
            return latest.to_dict()

        if isinstance(
            latest,
            dict,
        ):
            return latest

    if not HISTORY_PATH.exists():
        return None

    try:

        history = pd.read_csv(
            HISTORY_PATH
        )

        if history.empty:
            return None

        return history.iloc[-1].to_dict()

    except Exception:
        return None


def explain_latest_assessment():

    latest = load_latest_assessment()

    if latest is None:

        return """
You haven't completed an assessment yet 😄

Go to **Assessment**, complete it, and come back.

Appudu nee latest result ni simple ga explain chestha 💙
"""

    risk = latest.get(
        "risk_probability",
        "-",
    )

    category = latest.get(
        "risk_level",
        "-",
    )

    wellness = latest.get(
        "wellness_score",
        "-",
    )

    grade = latest.get(
        "wellness_grade",
        "-",
    )

    mood = latest.get(
        "mood",
        "-",
    )

    return f"""
Nee latest assessment summary 👇

🤖 **ML Concern Probability:** {risk}%  
🎯 **Model Category:** {category}

🌱 **Current Wellness Score:** {wellness}/100  
🏅 **Wellness Grade:** {grade}

🙂 **Recorded Mood:** {mood}

Remember:

- ML concern prediction = trained academic/profile features
- Wellness score = current lifestyle and self-reported wellbeing

So rendu different ga undadam possible 💙
"""


# ============================================================
# 8. SAFETY
# ============================================================

def needs_immediate_support(
    text: str,
) -> bool:

    serious_phrases = [
        "kill myself",
        "want to die",
        "don't want to live",
        "dont want to live",
        "self harm",
        "hurt myself",
        "suicide",
        "end my life",
    ]

    return contains_any(
        text,
        serious_phrases,
    )


def safety_response():

    return """
I'm really sorry you're feeling this much pain. 💙

Please don't handle this alone right now.

- Stay near a trusted person.
- Tell a friend, family member, teacher, counsellor, or another responsible person immediately.
- Move away from anything you could use to hurt yourself.
- If you may act on these thoughts or feel in immediate danger, contact local emergency services or go to the nearest emergency department.

I can stay here and talk with you, but I cannot replace immediate human or professional support.

For now, focus on one thing:

**Get close to a safe person.**
"""


# ============================================================
# 9. RELAX / MOOD
# ============================================================

def relaxation_response(
    user_text: str = "",
):

    return style_reply(
        """
Okay 😌 no lecture.

Let's do a quick 60-second reset.

🌬️ Inhale slowly for 4 seconds  
⏸️ Hold for 2 seconds  
💨 Exhale slowly for 6 seconds  

Repeat 3 times.

Now notice:

👀 3 things you can see  
👂 2 things you can hear  
🤲 1 thing you can feel  

How do you feel now? 💙
""",
        """
Okay 😌 lecture vadhu.

Quick 60-second reset cheddham.

🌬️ 4 seconds inhale  
⏸️ 2 seconds hold  
💨 6 seconds exhale  

3 times repeat cheyyi.

Tarvatha:

👀 3 things chudu  
👂 2 sounds vinu  
🤲 1 thing feel cheyyi  

Ippudu konchem better aa? 💙
""",
        user_text,
    )


def boredom_response(
    user_text: str = "bore",
):

    return style_reply(
        GAME_MENU,
        """
😂 Sare bro, bore ni pampincheddham.

🎬 Telugu Movie Guessing  
🎭 Emoji Movie Guessing  
🧩 Riddle  
🧠 Logic Challenge  
🕵️ Mini Mystery  
⚡ Rapid Fire  
🤔 Would You Rather  
😂 Random Fun Question  

Leka `surprise me` ani type cheyyi 🎲
""",
        user_text,
    )


def sad_response(
    user_text: str,
):

    return style_reply(
        """
Aww 💙 I'm here.

We don't have to turn this into a serious advice session immediately.

Choose what feels better:

💬 Tell me what happened  
🎮 Play something  
😌 One-minute relaxation  
😂 Just distract me  

You choose. I'll follow your mood.
""",
        """
Ayyoo 🫂 okay bro.

Ventane advice lecture start cheyyanu 😭

Choose cheyyi:

💬 Em jarigindo cheppu  
🎮 Game aadadhama  
😌 One-minute relax  
😂 Just distract cheyyi  

Nuv choose cheyyi. Nee mood batti veldham 💙
""",
        user_text,
    )


def stressed_response(
    user_text: str,
):

    return style_reply(
        """
That sounds stressful 😭

Three options:

😌 Calm first  
😂 Distract first  
💬 Talk first  

Tell me what would help right now.
""",
        """
Ayyoo stress aa 😭

Three options:

😌 First calm avudham  
😂 First distract avudham  
💬 First em jarigindo cheppu  

First vintaa. Lecture later 😂
""",
        user_text,
    )


# ============================================================
# 10. GAME ENGINE HELPERS
# ============================================================

def reset_game_state():

    st.session_state.game_mode = None
    st.session_state.game_data = None
    st.session_state.hint_index = 0


def get_game_pool(
    game_name: str,
):

    pool = GAME_COLLECTIONS.get(
        game_name,
        [],
    )

    preferred = st.session_state.preferred_difficulty

    if preferred in {
        "easy",
        "medium",
        "hard",
    }:

        filtered = [
            item
            for item in pool
            if item.get(
                "difficulty"
            ) == preferred
        ]

        if filtered:
            return filtered

    return pool


def get_next_question(
    game_name: str,
):

    pool = get_game_pool(
        game_name
    )

    if not pool:
        return None

    used_ids = set(
        st.session_state.asked_question_ids.get(
            game_name,
            [],
        )
    )

    available = [
        item
        for item in pool
        if item.get(
            "id"
        )
        not in used_ids
    ]

    if not available:

        st.session_state.asked_question_ids[
            game_name
        ] = []

        available = pool.copy()

    item = random.choice(
        available
    )

    item_id = item.get(
        "id"
    )

    if item_id:

        st.session_state.asked_question_ids[
            game_name
        ].append(
            item_id
        )

    return item


def format_game_question(
    game_name: str,
    item: dict,
):

    label = GAME_LABELS.get(
        game_name,
        "🎮 Game",
    )

    if game_name == "movie":

        return (
            f"{label}\n\n"
            f"{item['clue']}\n\n"
            "Movie name guess cheyyi 😌"
        )

    if game_name == "emoji_movie":

        return (
            f"{label}\n\n"
            f"Guess this movie:\n\n"
            f"## {item['question']}\n\n"
            "Movie name cheppu 😂"
        )

    if game_name in {
        "riddle",
        "logic",
        "mystery",
    }:

        return (
            f"{label}\n\n"
            f"{item['question']}\n\n"
            "Answer guess cheyyi 😌"
        )

    if game_name in {
        "would_you_rather",
        "fun_question",
        "rapid_fire",
    }:

        return (
            f"{label}\n\n"
            f"{item['question']}"
        )

    return str(item)


def start_game(
    game_name: str,
):

    item = get_next_question(
        game_name
    )

    if item is None:

        return (
            "Ayyoo 😭 game data dorakaledhu."
        )

    st.session_state.game_mode = game_name
    st.session_state.game_data = item
    st.session_state.hint_index = 0

    return format_game_question(
        game_name,
        item,
    )


def answer_matches(
    user_text: str,
    accepted_answers,
):

    guess = normalize(
        user_text
    )

    if isinstance(
        accepted_answers,
        str,
    ):

        accepted_answers = [
            accepted_answers
        ]

    for answer in accepted_answers:

        answer_clean = normalize(
            answer
        )

        if not answer_clean:
            continue

        if (
            guess == answer_clean
            or answer_clean in guess
            or guess in answer_clean
        ):
            return True

    return False


def get_hint():

    data = st.session_state.game_data

    if not data:

        return "Current game ledu bro 😄"

    hints = data.get(
        "hints"
    )

    if not hints:

        single_hint = data.get(
            "hint"
        )

        if single_hint:
            return f"💡 Hint: {single_hint}"

        return "Ee question ki extra hint ledu 😭"

    index = st.session_state.hint_index

    if index >= len(
        hints
    ):

        return (
            "Hints anni aipoyayi bro 😭 "
            "Try answer or type `skip`."
        )

    hint = hints[
        index
    ]

    st.session_state.hint_index += 1

    return (
        f"💡 Hint {index + 1}: "
        f"{hint}"
    )


def score_text():

    return (
        f"🏆 Score: {st.session_state.game_score} | "
        f"🔥 Streak: {st.session_state.game_streak}"
    )


def next_same_game():

    current_game = st.session_state.game_mode

    if current_game is None:
        return GAME_MENU

    return start_game(
        current_game
    )


def handle_active_game(
    user_text: str,
):

    game_name = st.session_state.game_mode
    data = st.session_state.game_data
    text = normalize(
        user_text
    )

    if not game_name or not data:
        return None


    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    if text in {
        "stop",
        "quit",
        "exit",
        "end game",
        "stop game",
    }:

        reset_game_state()

        return (
            "Okay bro 😂 game stop chesam.\n\n"
            + score_text()
            + "\n\nIppudu em cheddham?"
        )


    # --------------------------------------------------------
    # CHANGE GAME
    # --------------------------------------------------------

    if text in {
        "change game",
        "another game",
        "different game",
    }:

        reset_game_state()

        return GAME_MENU


    # --------------------------------------------------------
    # SKIP
    # --------------------------------------------------------

    if text in {
        "skip",
        "next",
        "next question",
    }:

        st.session_state.game_streak = 0

        return next_same_game()


    # --------------------------------------------------------
    # HINT
    # --------------------------------------------------------

    if text in {
        "hint",
        "another hint",
        "more hint",
        "clue",
    }:

        return get_hint()


    # --------------------------------------------------------
    # HARDER
    # --------------------------------------------------------

    if text in {
        "harder",
        "hard",
        "hard question",
    }:

        st.session_state.preferred_difficulty = (
            "hard"
        )

        return next_same_game()


    # --------------------------------------------------------
    # EASIER
    # --------------------------------------------------------

    if text in {
        "easier",
        "easy",
        "easy question",
    }:

        st.session_state.preferred_difficulty = (
            "easy"
        )

        return next_same_game()


    # --------------------------------------------------------
    # OPEN RESPONSE GAMES
    # --------------------------------------------------------

    if game_name in OPEN_RESPONSE_GAMES:

        user_answer = user_text

        response = random.choice(
            [
                f"😂 Niceee! **{user_answer}**\n\nInteresting choice bro.",
                f"Okayyy 👀 **{user_answer}** — unexpected answer 😂",
                f"Good one 😭😂 **{user_answer}**",
                f"Haha okay 😌 **{user_answer}** noted.",
            ]
        )

        next_question = start_game(
            game_name
        )

        return (
            response
            + "\n\n---\n\n"
            + next_question
        )


    # --------------------------------------------------------
    # ANSWER-BASED GAMES
    # --------------------------------------------------------

    accepted_answers = data.get(
        "answer",
        []
    )

    if answer_matches(
        user_text,
        accepted_answers,
    ):

        st.session_state.game_score += 1
        st.session_state.game_streak += 1

        reaction = random.choice(
            [
                "Correcttttt 😭🔥",
                "Yessss 😂🔥 correct!",
                "Brooo correct 😭👏",
                "Ahaaa! Perfect answer 😎",
            ]
        )

        score = score_text()

        next_question = start_game(
            game_name
        )

        return (
            f"{reaction}\n\n"
            f"{score}\n\n"
            "---\n\n"
            f"{next_question}"
        )

    st.session_state.game_streak = 0

    return """
Ayyoo kaadhu 😂

Malli try cheyyi.

Commands:

💡 `hint`  
⏭️ `skip`  
🔄 `change game`
"""


# ============================================================
# 11. EMOJI MOOD
# ============================================================

def emoji_response(
    emoji: str,
):

    responses = {

        "😊": """
Awww 😊 niceee!

Good mood maintain cheddham 😌

🎮 Game?
😂 Random fun?
💬 Just chat?
""",

        "😔": """
Ayyoo 😔🫂

Serious lecture vadhu.

💬 Natho matladava?
😌 Relax cheddhama?
🎮 Small game aadadhama?
""",

        "😭": """
Ayyayyo 😭🫂

Okay okay... nenu ikkade unna.

Matladali anukunte nenu vintaa.

Leka game tho konchem distract avudham 💙
""",

        "😡": """
Oho 😡 anger mode aa 😭

First vent cheyyi if you want.

Leka:
😌 cool down
🎮 game
💬 chat
""",

        "😴": """
Sleepy mode 😴😂

Choose:

😌 calming chat  
🧩 easy riddle  
🌬️ relaxation
""",

        "😂": """
Ahaaa 😂 fun mood!

🎬 Movie guessing
🧩 Riddle
⚡ Rapid fire
😂 Random question
""",

        "❤️": """
Awww ❤️ wholesome mood detected 😭😂

Tell me one small thing that made you smile today 😌
""",
    }

    return responses.get(
        emoji,
        "Mood received 😌💙",
    )


# ============================================================
# 12. MAIN RESPONSE ENGINE
# ============================================================

def generate_response(
    user_text: str,
):

    text = normalize(
        user_text
    )


    # --------------------------------------------------------
    # SAFETY FIRST
    # --------------------------------------------------------

    if needs_immediate_support(
        user_text
    ):

        reset_game_state()

        return safety_response()


    # --------------------------------------------------------
    # EMOJI
    # --------------------------------------------------------

    if user_text.strip() in {
        "😊",
        "😔",
        "😭",
        "😡",
        "😴",
        "😂",
        "❤️",
    }:

        return emoji_response(
            user_text.strip()
        )


    # --------------------------------------------------------
    # ACTIVE GAME
    # --------------------------------------------------------

    if st.session_state.game_mode:

        game_reply = handle_active_game(
            user_text
        )

        if game_reply:
            return game_reply


    # --------------------------------------------------------
    # SURPRISE ME
    # --------------------------------------------------------

    if text in {
        "surprise me",
        "random game",
        "anything",
        "edhaina",
    }:

        game_name = random.choice(
            list(
                GAME_COLLECTIONS.keys()
            )
        )

        return start_game(
            game_name
        )


    # --------------------------------------------------------
    # MOVIE
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "movie guessing",
            "movie game",
            "guess movie",
            "telugu movie",
        ],
    ):

        return start_game(
            "movie"
        )


    # --------------------------------------------------------
    # EMOJI MOVIE
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "emoji movie",
            "emoji guessing",
        ],
    ):

        return start_game(
            "emoji_movie"
        )


    # --------------------------------------------------------
    # RIDDLE
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "riddle",
            "brain teaser",
        ],
    ):

        return start_game(
            "riddle"
        )


    # --------------------------------------------------------
    # LOGIC
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "logic",
            "logic challenge",
            "logical question",
        ],
    ):

        return start_game(
            "logic"
        )


    # --------------------------------------------------------
    # MYSTERY
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "mystery",
            "detective",
            "mini mystery",
        ],
    ):

        return start_game(
            "mystery"
        )


    # --------------------------------------------------------
    # RAPID FIRE
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "rapid fire",
            "rapid",
        ],
    ):

        return start_game(
            "rapid_fire"
        )


    # --------------------------------------------------------
    # WOULD YOU RATHER
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "would you rather",
            "this or that",
        ],
    ):

        return start_game(
            "would_you_rather"
        )


    # --------------------------------------------------------
    # FUN QUESTION
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "fun question",
            "random question",
            "crazy question",
        ],
    ):

        return start_game(
            "fun_question"
        )


    # --------------------------------------------------------
    # GENERIC GAME
    # --------------------------------------------------------

    if text in {
        "game",
        "games",
        "play",
        "lets play",
        "let's play",
        "game aadali",
        "aadali",
    }:

        return GAME_MENU


    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    if text in {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "bro",
        "amore",
        "hola",
    }:

        return style_reply(
            random.choice(
                [
                    "Hey! 😄 How are you feeling today?",
                    "Hii 👋 How's your day going?",
                    "Hey there 😌 What's going on?",
                ]
            ),
            random.choice(
                [
                    "Heyyy 😄 ela unnav?",
                    "Hiiii 👋 em chesthunnav?",
                    "Brooo 😂 cheppu em scene?",
                    "Hey 😌 ivala mood enti?",
                ]
            ),
            user_text,
        )


    # --------------------------------------------------------
    # BORED
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "bore",
            "bored",
            "boring",
        ],
    ):

        return boredom_response(
            user_text
        )


    # --------------------------------------------------------
    # LOW MOOD
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "mood baledhu",
            "mood baaledu",
            "sad",
            "feeling low",
            "not feeling good",
            "bad mood",
            "upset",
            "not okay",
        ],
    ):

        return sad_response(
            user_text
        )


    # --------------------------------------------------------
    # STRESS
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "stress",
            "stressed",
            "exam tension",
            "pressure",
            "overwhelmed",
            "tension",
        ],
    ):

        return stressed_response(
            user_text
        )


    # --------------------------------------------------------
    # RELAX
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "relax",
            "calm",
            "breathing",
            "relaxation",
        ],
    ):

        return relaxation_response(
            user_text
        )


    # --------------------------------------------------------
    # ASSESSMENT
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "my result",
            "assessment",
            "explain result",
            "risk",
            "wellness score",
        ],
    ):

        return explain_latest_assessment()


    # --------------------------------------------------------
    # MOTIVATION
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "motivate",
            "motivation",
            "lazy",
            "can't study",
            "cant study",
            "no interest",
        ],
    ):

        return style_reply(
            """
Don't try to become productive for five hours.

Just do this:

📚 10 minutes study  
📱 Keep the phone away  
✅ Finish one tiny task  

The hardest part is usually starting.

Want to try a 10-minute challenge? 😌
""",
            """
Bro 5 hours productive avvali ani think cheyyaku 😭

Just:

📚 10 minutes study  
📱 Phone pakkana  
✅ One tiny task finish  

Main problem motivation kaadhu.

Starting.

10-minute challenge try cheddhama? 😌
""",
            user_text,
        )


    # --------------------------------------------------------
    # SLEEP
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "sleep",
            "can't sleep",
            "cant sleep",
            "insomnia",
        ],
    ):

        return style_reply(
            """
Let's keep it simple:

📱 Reduce screen brightness  
🛏️ Avoid scrolling in bed  
🌬️ Take 4 slow breaths  
🎵 Play calm audio  
📝 Write tomorrow's tasks down  

Don't force perfect sleep.

First goal: calm your body 😌
""",
            """
Simple ga try cheddham:

📱 Brightness reduce  
🛏️ Bed lo scrolling avoid  
🌬️ 4 slow breaths  
🎵 Soft music  
📝 Tomorrow tasks rasuko  

Perfect sleep force cheyyaku.

First body calm avvali 😌
""",
            user_text,
        )


    # --------------------------------------------------------
    # THANKS
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "thanks",
            "thank you",
            "tq",
        ],
    ):

        return random.choice(
            [
                "Anytime bro 😌💙",
                "Always 😄",
                "No thanks needed 😂",
                "We're a team 😭😂",
            ]
        )


    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    return style_reply(
        random.choice(
            [
                "I'm listening 😌 Tell me a little more.",
                "Okay 👀 continue... what happened next?",
                "Hmm, I get what you're saying. How did that make you feel?",
                "Tell me the full story 😂 I'm listening.",
            ]
        ),
        random.choice(
            [
                "Hmm 😌 nenu vintunna. Konchem more cheppu...",
                "Okay okay 👀 continue... tarvatha em ayindhi? 😂",
                "Acha 😭😂 full story cheppu bro.",
                "Hmm... ardham avuthundi. Nuv appudu ela feel ayyav?",
            ]
        ),
        user_text,
    )


# ============================================================
# 13. PAGE HEADER
# ============================================================

st.title(
    "🤖 MindCare Companion"
)

st.caption(
    "Chat • Relax • Play • Laugh • Reflect • Get Support"
)


# ============================================================
# 14. GAME STATUS
# ============================================================

with st.container(
    border=True
):

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        current_game = (
            GAME_LABELS.get(
                st.session_state.game_mode,
                "No active game",
            )
        )

        st.metric(
            "Current Game",
            current_game,
        )

    with col2:

        st.metric(
            "Score",
            st.session_state.game_score,
        )

    with col3:

        st.metric(
            "Streak",
            st.session_state.game_streak,
        )


# ============================================================
# 15. QUICK ACTIONS
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "⚡ Quick Actions"
    )

    col1, col2, col3, col4 = st.columns(
        4
    )


    with col1:

        if st.button(
            "🎮 Play",
            width="stretch",
        ):

            add_message(
                "assistant",
                GAME_MENU,
            )

            st.rerun()


    with col2:

        if st.button(
            "🎲 Surprise Me",
            width="stretch",
        ):

            random_game = random.choice(
                list(
                    GAME_COLLECTIONS.keys()
                )
            )

            add_message(
                "assistant",
                start_game(
                    random_game
                ),
            )

            st.rerun()


    with col3:

        if st.button(
            "😌 Relax",
            width="stretch",
        ):

            add_message(
                "assistant",
                relaxation_response(
                    "relax"
                ),
            )

            st.rerun()


    with col4:

        if st.button(
            "🧹 Clear Chat",
            width="stretch",
        ):

            st.session_state.companion_messages = [
                {
                    "role": "assistant",
                    "content": WELCOME_MESSAGE,
                }
            ]

            reset_game_state()

            st.session_state.game_score = 0
            st.session_state.game_streak = 0

            st.rerun()


# ============================================================
# 16. EMOJI MOOD
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "😊 Express Your Mood"
    )

    emoji_columns = st.columns(
        7
    )

    emojis = [
        "😊",
        "😔",
        "😭",
        "😡",
        "😴",
        "😂",
        "❤️",
    ]

    for column, emoji in zip(
        emoji_columns,
        emojis,
    ):

        with column:

            if st.button(
                emoji,
                key=f"emoji_{emoji}",
                width="stretch",
            ):

                add_message(
                    "user",
                    emoji,
                )

                add_message(
                    "assistant",
                    emoji_response(
                        emoji
                    ),
                )

                st.rerun()


# ============================================================
# 17. CHAT HISTORY
# ============================================================

with st.container(
    border=True
):

    for message in (
        st.session_state.companion_messages
    ):

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


# ============================================================
# 18. CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Message MindCare Companion... 😊"
)


if user_input:

    add_message(
        "user",
        user_input,
    )

    reply = generate_response(
        user_input
    )

    add_message(
        "assistant",
        reply,
    )

    st.rerun()


# ============================================================
# 19. HELP
# ============================================================

with st.expander(
    "🎮 Game Commands"
):

    st.markdown(
        """
`hint` — next hint  
`another hint` — another clue  
`skip` — skip current question  
`change game` — choose another game  
`harder` — prefer harder questions  
`easier` — prefer easier questions  
`stop` — stop current game  
`surprise me` — random game
"""
    )


# ============================================================
# 20. FOOTER
# ============================================================

st.caption(
    "💙 MindCare Companion is for friendly wellness support, relaxation and fun. "
    "It is not a medical professional or emergency service."
)