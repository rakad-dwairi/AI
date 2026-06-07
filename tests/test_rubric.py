from thohor_validation.core.paths import FORM_PATH
from thohor_validation.core.rubric import load_form_criteria, load_rubric_levels


def test_excel_form_extracts_expected_rows():
    criteria = load_form_criteria(FORM_PATH)
    levels = load_rubric_levels(FORM_PATH)

    assert len(criteria) >= 40
    assert len(levels) >= 40
    assert criteria[0].axis == "الأداء الصوتي"
    assert "وضوح المخارج" in criteria[0].name
