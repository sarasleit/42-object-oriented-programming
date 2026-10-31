
import alchemy.grimoire


def main() -> None:
    print("=== Kaboom 0 ===")
    print("Using grimoire module directly")
    spell_result: str = alchemy.grimoire.light_spell_record(
        "Fantasy",
        "Earth, wind and fier"
    )
    print(f"Testing record light spell: {spell_result}")


if __name__ == "__main__":
    main()
