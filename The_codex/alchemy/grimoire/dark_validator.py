from alchemy.grimoire.dark_spellbook import dark_spell_allowed_ingredients


def validate_dark_ingredients(ingredients: str) -> str:
    allowed_dark_ingredients = dark_spell_allowed_ingredients()
    for i in allowed_dark_ingredients:
        if i.lower() in ingredients.lower():
            return f"({ingredients} - VALID)"

    return f"({ingredients} - INVALID)"
