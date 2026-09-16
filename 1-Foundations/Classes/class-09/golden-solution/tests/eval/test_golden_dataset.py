from widgetware_sdr.eval.golden_dataset import GOLDEN_DATASET, REQUIRED_CATEGORIES


def test_every_required_category_has_at_least_one_case() -> None:
    represented = {case.category for case in GOLDEN_DATASET}
    missing = REQUIRED_CATEGORIES - represented
    assert not missing, f"golden dataset is missing categories: {missing}"


def test_every_case_has_a_unique_id() -> None:
    ids = [case.case_id for case in GOLDEN_DATASET]
    assert len(ids) == len(set(ids))
