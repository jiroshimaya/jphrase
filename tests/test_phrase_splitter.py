import pytest
from jphrase import PhraseSplitter

@pytest.fixture
def splitter():
    return PhraseSplitter()

@pytest.fixture
def base_cases():
    return [
        ["痛さを", ["痛さを"]], #接尾辞
        ["ご丁寧に", ["ご丁寧に"]], # 接頭辞
        ["勉強する", ["勉強する"]], #サ変接続名詞+サ変
        ["abcする", ["abc", "する"]], #Unknown名詞+サ変
        ["違うする", ["違う", "する"]], #名詞以外+サ変
        ["「あなたは、『どこ』？」", ["「あなたは、", "『どこ』？」"]], # 記号
        ["はが", ["はが"]], # 助詞から始まる文節
        ["て、に、を、はなどの", ["て、","に、","を、","はなどの"]], # 記号直後の助詞
        ["「て。」や「に」などの", ["「て。」や","「に」などの"]] # 閉じカッコ直後の助詞
    ]

def test_split_text_surface_true(splitter, base_cases):
    specific_cases = [
        ["寝ているところなんです", ["寝て", "いる", "ところな","んです"]], # 非自立動詞
        ["寝ている、ところ", ["寝て","いる、", "ところ"]], # 非自立名詞
        ["寝ている」ところ", ["寝て","いる」", "ところ"]] # 非自立名詞
    ]
    for input_string, expected in base_cases + specific_cases:
        result = splitter.split_text(input_string, output_type=PhraseSplitter.OUTPUT_SURFACE, consider_non_independent_nouns_and_verbs_as_breaks=True)
        assert result == expected

def test_split_text_surface_false(splitter, base_cases):
    specific_cases = [
        ["寝ているところなんです", ["寝ているところなんです"]], # 非自立動詞
        ["寝ている、ところ", ["寝ている、", "ところ"]], # 非自立名詞
        ["寝ている」ところ", ["寝ている」ところ"]] # 非自立名詞
    ]
    for input_string, expected in base_cases + specific_cases:
        result = splitter.split_text(input_string, output_type=PhraseSplitter.OUTPUT_SURFACE, consider_non_independent_nouns_and_verbs_as_breaks=False)
        assert result == expected

def test_split_text_detailed_true(splitter):
    specific_cases = [
        ["寝ている", [['寝', 'て'], ['いる']]]
    ]
    for input_string, expected in specific_cases:
        detailed_phrases = splitter.split_text(input_string, PhraseSplitter.OUTPUT_DETAILED, consider_non_independent_nouns_and_verbs_as_breaks=True)
        surface_forms_only = [[token['surface_form'] for token in phrase] for phrase in detailed_phrases]
        result = surface_forms_only
        assert result == expected

def test_split_text_concatenated_true(splitter):
    specific_cases = [
        ["今日は", [{'surface_form': '今日は', 'reading': 'キョウハ', 'pronunciation': 'キョーワ'}]]
    ]
    for input_string, expected in specific_cases:
        result = splitter.split_text(input_string, output_type=PhraseSplitter.OUTPUT_CONCATENATED, consider_non_independent_nouns_and_verbs_as_breaks=True)
        assert result == expected
