
def main() -> None:
    print("=== Kaboom 1 ===")
    print("Access to alchemy/grimoire/dark_spellbook.py directly")
    print("Test import now :")

    try:
        from alchemy.grimoire.dark_spellbook import dark_spell_record

        dark_spell_result: str = dark_spell_record(
            "Fantasy",
            "Bats, frogs, arsenic and eyeball"
        )
        print(f"Testing record dark spell: {dark_spell_result}")

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
