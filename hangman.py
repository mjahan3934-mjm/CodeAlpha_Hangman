import random

# ----- Word lists by difficulty -----
EASY_WORDS = ["cat", "dog", "bird", "fish", "tree", "house", "book", "phone"]
MEDIUM_WORDS = ["python", "laptop", "rocket", "bridge", "guitar", "elephant", "keyboard", "library"]
HARD_WORDS = ["algorithm", "byzantine", "crystallize", "ephemeral", "phenomenon", "javascript", "achievement"]

# ----- Difficulty settings -----
DIFFICULTY_SETTINGS = {
    "easy": {"wrong_allowed": 8, "words": EASY_WORDS},
    "medium": {"wrong_allowed": 6, "words": MEDIUM_WORDS},
    "hard": {"wrong_allowed": 4, "words": HARD_WORDS},
}

# ----- ASCII art stages -----
HANGMAN_STAGES = [
    """
       -----
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """,
]


class GameStats:
    def __init__(self):
        self.total_games = 0
        self.wins = 0
        self.losses = 0
    
    def record_win(self) -> None:
        self.wins += 1
        self.total_games += 1
    
    def record_loss(self) -> None:
        self.losses += 1
        self.total_games += 1
    
    def win_percentage(self) -> float:
        return (self.wins / self.total_games * 100) if self.total_games > 0 else 0
    
    def display(self) -> None:
        print("\n" + "=" * 45)
        print("    SESSION STATS")
        print("=" * 45)
        print(f"  Total Games: {self.total_games}")
        print(f"  Wins:        {self.wins}")
        print(f"  Losses:      {self.losses}")
        print(f"  Win Rate:    {self.win_percentage():.1f}%")
        print("=" * 45 + "\n")


def select_difficulty() -> tuple[str, int, list]:
    
    print("\n" + "=" * 45)
    print("       SELECT DIFFICULTY")
    print("=" * 45)
    print("  1. Easy   (8 wrong guesses allowed)")
    print("  2. Medium (6 wrong guesses allowed)")
    print("  3. Hard   (4 wrong guesses allowed)\n")
    
    while True:
        choice = input("  Choose (1/2/3): ").strip()
        if choice == "1":
            return "easy", DIFFICULTY_SETTINGS["easy"]["wrong_allowed"], DIFFICULTY_SETTINGS["easy"]["words"]
        elif choice == "2":
            return "medium", DIFFICULTY_SETTINGS["medium"]["wrong_allowed"], DIFFICULTY_SETTINGS["medium"]["words"]
        elif choice == "3":
            return "hard", DIFFICULTY_SETTINGS["hard"]["wrong_allowed"], DIFFICULTY_SETTINGS["hard"]["words"]
        else:
            print("  ⚠  Please enter 1, 2, or 3.\n")


def display_state(word: str, guessed: set, wrong_count: int, max_wrong: int) -> None:
    
    print(HANGMAN_STAGES[min(wrong_count, len(HANGMAN_STAGES) - 1)])
    masked = " ".join(ch if ch in guessed else "_" for ch in word)
    print(f"  Word : {masked}")
    wrong_letters = sorted(guessed - set(word))
    print(f"  Wrong guesses ({wrong_count}/{max_wrong}): {', '.join(wrong_letters) or '—'}")
    print()


def get_guess(guessed: set) -> str:
    
    while True:
        guess = input("  Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("  ⚠  Please enter a single alphabetic letter.\n")
        elif guess in guessed:
            print(f"  ⚠  You already guessed '{guess}'. Try another.\n")
        else:
            return guess


def play_game(difficulty: str, word_list: list, max_wrong: int, stats: GameStats) -> None:
    
    word = random.choice(word_list)
    guessed: set = set()
    wrong_count = 0

    print("\n" + "=" * 45)
    print(f"       H A N G M A N   ({difficulty.upper()})")
    print("=" * 45)
    print(f"  A {len(word)}-letter word has been chosen. Good luck!\n")

    while True:
        display_state(word, guessed, wrong_count, max_wrong)

        # --- Win condition ---
        if all(ch in guessed for ch in word):
            print(f"  🎉 You won! The word was '{word.upper()}'.\n")
            stats.record_win()
            break

        # --- Lose condition ---
        if wrong_count >= max_wrong:
            print(f"  💀 Game over! The word was '{word.upper()}'.\n")
            stats.record_loss()
            break

        # --- Get and process guess ---
        guess = get_guess(guessed)
        guessed.add(guess)

        if guess in word:
            print(f"  ✅ '{guess}' is in the word!\n")
        else:
            wrong_count += 1
            print(f"  ❌ '{guess}' is NOT in the word.\n")


def main() -> None:
    
    stats = GameStats()
    
    print("\n" + "=" * 45)
    print("    WELCOME TO HANGMAN")
    print("=" * 45 + "\n")
    
    while True:
        difficulty, max_wrong, word_list = select_difficulty()
        play_game(difficulty, word_list, max_wrong, stats)
        
        again = input("  Play again? (y/n): ").strip().lower()
        if again != "y":
            stats.display()
            print("  Thanks for playing Hangman! Goodbye. 👋\n")
            break


if __name__ == "__main__":
    main()