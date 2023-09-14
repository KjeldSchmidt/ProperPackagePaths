def bar() -> bool:
    return False


class Sibling:
    def passes_test(self) -> bool:
        _ = self
        return False
