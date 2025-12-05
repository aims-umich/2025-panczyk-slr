import itertools
import pickle


def get_search_combos():
    population_terms = [
        "nuclear",
        "aerospace",
        "health*",
        "medic*",
        "clinical",
        '"autonomous driving"',
        '"autonomous vehicle"',
        "automotive",
        "radiation",
        "emergency",
        '"first responders"',
        "fire",
        "hospital",
        "energy",
        "pharmaceutical",
        "aviation",
        '"power grid"',
        '"electric grid"',
    ]
    interv_terms_ai = [
        '"artificial intelligence"',
        '"machine learning"',
        '"neural networks"',
        '"language models"',
        "computer vision",
        "automated",
        '"deep learning"',
    ]
    interv_terms_decision = ["decision*"]
    outcome_terms = [
        "incidents",
        '"close call*"',
        "accidents",
        '"near miss*"',
        "injuries",
        "failure",
        '"adverse event"',
        "malfunction",
        "fatalities",
        "misdiagnos*",
        "harm",
        "litigation",
        "lawsuit*",
        '"operating experience"',
    ]
    regulation_terms = [
        "regulat*",
        "governance",
        "oversight",
        "compliance",
        '"safety standards"',
    ]
    combinations = list(
        itertools.product(
            population_terms, interv_terms_ai, interv_terms_decision, outcome_terms
        )
    )
    return combinations


if __name__ == "__main__":
    combo_list = get_search_combos()
    print(f"Total search combinations: {len(combo_list)}")
    with open(snakemake.output.combos, "wb") as f:
        pickle.dump(combo_list, f)
