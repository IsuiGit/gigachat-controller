from typing import Any, Dict

class GigaChatControllerException(Exception):
    def __init__(
        self,
        message,
        code: int = None,
        tool: str = None,
        scenario: str = None,
        method: Dict[str, Any] = None
    ) -> None:
        super().__init__(message)
        self.code = code
        self.tool = tool
        self.scenario = scenario
        self.method = method

    def __str__(self):
        base = super().__str__()
        return f"[ExCode: {self.code} | {self.__class__.__name__}] {base}" + (f"\nTool: {self.tool}\nScenario: {self.scenario}\nMethod: {self.method})")

class GigaChatControllerHttpException(GigaChatControllerException):
    pass

class GigaChatControllerHttpXException(GigaChatControllerException):
    pass
