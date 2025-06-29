class BinaryIndicatorMetric(IndicatorMetric[int]):
    """
    Represents a binary (boolean) state indicator.

    Provides methods to set, get, and represent the state.
    """

    def __init__(self):
        """
        Initialize a BinaryIndicator.
        """
        super().__init__(initial=0)

    def toggle(self):
        self.value = 1 if self.value == 0 else 0

    def collect(self) -> V:
        return self.value

    def __str__(self):
        """
        String representation of the indicator state.

        Returns:
            str: Name and state ("Yes" or "No").
        """
        return f"{self.name}: {'Yes' if self.state else 'No'}"

    def as_int(self) -> int:
        """
        Get the indicator state as int (1 or 0).

        Returns:
            int: 1 if True, else 0.
        """
        return 1 if self.state else 0
