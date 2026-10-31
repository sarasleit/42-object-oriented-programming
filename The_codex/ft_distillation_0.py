
from alchemy.potions import healing_potion, strength_potion


def main() -> None:
    print("=== Distillation 0 ===")
    print("Direct access to alchemy/potions.py")
    print("Testing healing_potion: ", healing_potion())
    print("Testing strength_potion: ", strength_potion())


if __name__ == "__main__":
    main()
