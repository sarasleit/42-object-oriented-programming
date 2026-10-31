def light_spell_allowed_ingredients() -> list[str]:
    allowed_ingredients = ["air", "fire", "water", "earth"]
    return allowed_ingredients


def light_spell_record(spell_name: str, ingredients: str) -> str:
    from alchemy.grimoire.light_validator import validate_ingredients
    return (f"Spell recorded:   {spell_name}: "
            f"{validate_ingredients(ingredients)}")
