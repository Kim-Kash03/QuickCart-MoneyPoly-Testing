"""
Entry point for the MoneyPoly game.
Provides a simple CLI to set up and run a game session.
"""
from moneypoly.game import Game


def get_player_names():
    """
    Prompt the user to enter names for the players.
    Returns a list of strings.
    """
    print("Enter player names separated by commas (minimum 2 players):")
    raw = input("> ").strip()
    names = [n.strip() for n in raw.split(",") if n.strip()]
    return names


def main():
    """Main execution loop for the MoneyPoly CLI."""
    names = get_player_names()
    try:
        game = Game(names)
        game.run()
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Goodbye!")
    except ValueError as exc:
        print(f"Setup error: {exc}")


if __name__ == "__main__":
    main()
