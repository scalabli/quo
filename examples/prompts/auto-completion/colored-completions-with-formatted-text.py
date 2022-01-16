#!/usr/bin/env python
"""
Demonstration of a custom completer class and the possibility of styling
completions independently by passing formatted text objects to the "display"
and "display_meta" arguments of "Completion".
"""

import quo

session = quo.Prompt()

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
    "alligator": quo.text.HTML(
        "An <red>alligator</red> is a <u>crocodilian</u> in the genus Alligator of the family Alligatoridae."
    ),
    "ant": quo.text.HTML(
        "<red>Ants</red> are eusocial <u>insects</u> of the family Formicidae."
    ),
    "ape": quo.text.HTML(
        "<red>Apes</red> (Hominoidea) are a branch of Old World tailless anthropoid catarrhine <u>primates</u>."
    ),
    "bat": quo.text.HTML("<red>Bats</red> are mammals of the order <u>Chiroptera</u>."),
    "bee": quo.text.HTML(
        "<red>Bees</red> are flying <u>insects</u> closely related to wasps and ants."
    ),
    "beaver": quo.text.HTML(
        "The <red>beaver</red> (genus Castor) is a large, primarily <u>nocturnal</u>, semiaquatic <u>rodent</u>."
    ),
    "bear": quo.text.HTML(
        "<red>Bears</red> are carnivoran <u>mammals</u> of the family Ursidae."
    ),
    "butterfly": quo.text.HTML(
        "<blue>Butterflies</blue> are <u>insects</u> in the macrolepidopteran clade Rhopalocera from the order Lepidoptera."
    ),
    # ...
}


class AnimalCompleter(quo.completion.Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for animal in animals:
            if animal.startswith(word):
                if animal in animal_family:
                    family = animal_family[animal]
                    family_color = family_colors.get(family, "default")

                    display = quo.text.HTML(
                        "%s<b>:</b> <red>(<"
                        + family_color
                        + ">%s</"
                        + family_color
                        + ">)</red>"
                    ) % (animal, family)
                else:
                    display = animal

                yield quo.completion.Completion(
                    animal,
                    start_position=-len(word),
                    display=display,
                    display_meta=meta.get(animal),
                )


def main():
    # Simple completion menu.
    print("(The completion menu displays colors.)")
    session.prompt("Type an animal: ", completer=AnimalCompleter())

    # Multi-column menu.
    session.prompt(
        "Type an animal: ",
        completer=AnimalCompleter(),
        complete_style=quo.completion.CompleteStyle.multi_column,
    )

    # Readline-like
    session.prompt(
        "Type an animal: ",
        completer=AnimalCompleter(),
        complete_style=quo.completion.CompleteStyle.neat,
    )


if __name__ == "__main__":
    main()
