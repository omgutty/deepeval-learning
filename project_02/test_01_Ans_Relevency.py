from deepeval.test_case import LLMTestCase
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric


def test_hello_world():
    test= LLMTestCase (
        input="what is 2+2",
        actual_output="4",
        expected_output="4",
        context=["Basic arthmetic performace and give result"]
    )
    metric= [AnswerRelevancyMetric(threshold=0.9)]
    assert_test(test,metric)
