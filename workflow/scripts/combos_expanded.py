import itertools
import pickle


def get_search_combos():
    population_terms = [
        # nuclear specific
        "nuclear",
        "radiation",
        # transportation
        "aerospace",
        "aviation",
        "aircraft",
        "airport",
        '"autonomous driving"',
        '"autonomous vehicle*"',
        "self-driving",
        "automotive*",
        # energy systems
        "energy",
        '"power grid*"',
        '"electric grid*"',
        "chemical",
        "petroleum",
        # medical terms related to engineered equipment/devices ONLY
        '"medical device*"',
        '"medical equipment"',
        '"diagnostic device*"',
        '"imaging device*"',
        '"surgical robot*"',
        '"implantable device*"',
        "drug*",
        '"patient safety"',
        "pharmaceutical*",
        "radiotherapy",
        '"clinical trial*"',
    ]
    interv_terms_ai = [
        '"artificial intelligence"',
        "AI",
        '"machine learning"',
        "ML",
        '"neural network*"',
        '"language model*"',
        "computer vision",
        "automated",
        '"deep learning"',
    ]
    interv_terms_decision = ["decision*"]
    outcome_terms = [
        "incident*",
        '"close call*"',
        "accident*",
        '"near miss*"',
        "injur*",
        "failure*",
        '"adverse event*"',
        "malfunction",
        "fatalit*",
        "misdiagnos*",
        "harm",
        '"operating experience*"',
        '"OSHA citation*"',
        '"FDA recall*"',
        '"NHTSA investigation*"',
        "violation*",
        '"enforcement action*"',
        "risk",
        "hazard",
        "error"
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
    print(f"Combo list 1: {combo_list[1]}")
    with open(snakemake.output.combos, "wb") as f:
        pickle.dump(combo_list, f)
