#!/usr/bin/env python
"""
Demonstration of a custom completer class and the possibility of styling
completions independently by passing formatted text objects to the "display"
and "display_meta" arguments of "Completion".
"""

from quo.completion import Completion, Completer
from quo.prompt import Prompt
from quo.text import Text

animals = [
    "alligator",
    "ant",
    "ape",
    "bat",
    "bear",
    "beaver",
    "bee",
    "bison",
    "butterfly",
    "cat",
    "chicken",
    "crocodile",
    "dinosaur",
    "dog",
    "dolphin",
    "dove",
    "duck",
    "eagle",
    "elephant",
]

animal_family = {
    "alligator": "reptile",
    "ant": "insect",
    "ape": "mammal",
    "bat": "mammal",
    "bear": "mammal",
    "beaver": "mammal",
    "bee": "insect",
    "bison": "mammal",
    "butterfly": "insect",
    "cat": "mammal",
    "chicken": "bird",
    "crocodile": "reptile",
    "dinosaur": "reptile",
    "dog": "mammal",
    "dolphin": "mammal",
    "dove": "bird",
    "duck": "bird",
    "eagle": "bird",
    "elephant": "mammal",
}

family_colors = {
    "mammal": "magenta",
    "insect": "green",
    "reptile": "red",
    "bird": "yellow",
}

meta = {
    "alligator": Text("An <red>alligator</red> is a <u>crocodilian</u> in the genus Alligator of the family Alligatoridae."),
    "ant": Text("<red>Ants</red> are eusocial <u>insects</u> of the family Formicidae."),
    "ape": Text("<red>Apes</red> (Hominoidea) are a branch of Old World tailless anthropoid catarrhine <u>primates</u>."),
    "bat": Text("<red>Bats</red> are mammals of the order <u>Chiroptera</u>."),
    "bee": Text("<red>Bees</red> are flying <u>insects</u> closely related to wasps and ants."),
    "beaver": Text("The <red>beaver</red> (genus Castor) is a large, primarily <u>nocturnal</u>, semiaquatic <u>rodent</u>."),
    "bear": Text("<red>Bears</red> are carnivoran <u>mammals</u> of the family Ursidae."
    ),
    "butterfly": Text("<blue>Butterflies</blue> are <u>insects</u> in the macrolepidopteran clade Rhopalocera from the order Lepidoptera.")
    }


class AnimalCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for animal in animals:
            if animal.startswith(word):
                if animal in animal_family:
                    family = animal_family[animal]
                    family_color = family_colors.get(family, "default")

                    display = Text(
                        "%s<b>:</b> <red>(<"
                        + family_color
                        + ">%s</"
                        + family_color
                        + ">)</red>"
                    ) % (animal, family)
                else:
                    display = animal

                yield Completion(
                    animal,
                    start_position=-len(word),
                    display=display,
                    display_meta=meta.get(animal),
                )


def main():
    # Simple completion menu.
    print("(The completion menu displays colors.)")

    session = Prompt()
    session.prompt("Type an animal: ", completer=AnimalCompleter())

    # Multi-column menu.
    session = Prompt()
    session.prompt(
        "Type an animal: ",
        completer=AnimalCompleter(),
        complete_style="multi_column"
    )

    # Readline-like
    session = Prompt()
    session.prompt(
        "Type an animal: ",
        completer=AnimalCompleter(),
        complete_style="readline")

if __name__ == "__main__":
    main()
