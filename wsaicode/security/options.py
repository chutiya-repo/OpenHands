from wsaicode.security.analyzer import SecurityAnalyzer
from wsaicode.security.grayswan.analyzer import GraySwanAnalyzer
from wsaicode.security.invariant.analyzer import InvariantAnalyzer
from wsaicode.security.llm.analyzer import LLMRiskAnalyzer

SecurityAnalyzers: dict[str, type[SecurityAnalyzer]] = {
    'invariant': InvariantAnalyzer,
    'llm': LLMRiskAnalyzer,
    'grayswan': GraySwanAnalyzer,
}
