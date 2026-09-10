"""Golden cases for the RAG pipeline (Subsystem B).

These are used by the retrieval metrics, which need both the answer and the
chunks that produced it.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RagGolden:
    input: str
    expected_output: str
    expected_context_keywords: list[str] = field(default_factory=list)
    expected_sources: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)


RAG_GOLDENS: list[RagGolden] = [
    RagGolden(
        input="How long do refunds take?",
        expected_output=(
            "Refunds are processed within 7 business days of receiving the returned item."
        ),
        expected_context_keywords=["7 business days"],
        expected_sources=["refund_policy.md"],
        categories=["refund"],
    ),
    RagGolden(
        input="What is your holiday return policy?",
        expected_output=(
            "Items purchased between November 1 and December 24 can be returned "
            "through January 31 of the following year."
        ),
        expected_context_keywords=["November 1", "January 31"],
        expected_sources=["return_policy.md"],
        categories=["return"],
    ),
    RagGolden(
        input="How fast is overnight shipping?",
        expected_output=(
            "Overnight shipping costs $24.99 and arrives next business day if "
            "ordered before 12pm ET."
        ),
        expected_context_keywords=["$24.99", "12pm ET"],
        expected_sources=["shipping_policy.md"],
        categories=["shipping"],
    ),
    RagGolden(
        input="What is the price of the wireless earbuds?",
        expected_output="The ShopSphere Wireless Earbuds (SP-EARBUDS-01) cost $79.00.",
        expected_context_keywords=["SP-EARBUDS-01", "$79"],
        expected_sources=["product_catalog.md"],
        categories=["product"],
    ),
]
