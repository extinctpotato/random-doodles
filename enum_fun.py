from enum import Enum

def ask_for_enum(en: Enum) -> int:
    print(f"Available options for {en.__name__}:")
    for e in (enum_opts := list(en)):
        print(f"\t{e.name.lower().capitalize()}\t[{e.value}]")

    while True:
        try:
            if (choice := int(input("Your choice? "))) in [x.value for x in enum_opts]:
                return choice
            print(f"Invalid option {choice}")
        except ValueError:
            print("Not an integer!")
            pass
