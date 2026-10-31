from alchemy.grimoire.dark_validator import validate_dark_ingredients


def dark_spell_allowed_ingredients() -> list[str]:
    allowed_dark_ingredients = ["bats", "frogs", "arsenic", "eyeball"]
    return allowed_dark_ingredients


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    return (f"Spell recorded:   {spell_name}: "
            f"{validate_dark_ingredients(ingredients)}")
