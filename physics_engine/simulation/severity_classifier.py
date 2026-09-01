class SeverityClassifier:
    """
    Classifies Physics Engine anomalies into
    LOW, MEDIUM, HIGH, or CRITICAL severity.
    """

    LOW_THRESHOLD = 0.25
    MEDIUM_THRESHOLD = 0.50
    HIGH_THRESHOLD = 0.75

    def classify(self, anomaly_score: float) -> str:
        """
        Convert anomaly score into severity level.

        Score range:
        0.00 - 0.24  -> LOW
        0.25 - 0.49  -> MEDIUM
        0.50 - 0.74  -> HIGH
        0.75 - 1.00  -> CRITICAL
        """

        if not 0 <= anomaly_score <= 1:
            raise ValueError(
                "Anomaly score must be between 0 and 1."
            )

        if anomaly_score < self.LOW_THRESHOLD:
            return "LOW"

        if anomaly_score < self.MEDIUM_THRESHOLD:
            return "MEDIUM"

        if anomaly_score < self.HIGH_THRESHOLD:
            return "HIGH"

        return "CRITICAL"