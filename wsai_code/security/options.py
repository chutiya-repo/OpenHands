from wsai_code.security.analyzer import SecurityAnalyzer
from wsai_code.security.grayswan.analyzer import GraySwanAnalyzer
from wsai_code.security.invariant.analyzer import InvariantAnalyzer
from wsai_code.security.llm.analyzer import LLMRiskAnalyzer

SecurityAnalyzers: dict[str, type[SecurityAnalyzer]] = {
    'invariant': InvariantAnalyzer,
    'llm': LLMRiskAnalyzer,
    'grayswan': GraySwanAnalyzer,
}
