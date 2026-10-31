def validate_ingredients(ingredients: str) -> str:
    from alchemy.grimoire.light_spellbook import (
            light_spell_allowed_ingredients)

    allowed_ingredients = light_spell_allowed_ingredients()
    for i in allowed_ingredients:
        if i.lower() in ingredients.lower():
            return f"({ingredients} - VALID)"

    return f"({ingredients} - INVALID)"
