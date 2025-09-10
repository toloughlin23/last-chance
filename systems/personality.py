from dataclasses import dataclass


@dataclass
class PersonalityProfile:
    risk_tolerance: float  # 0.0 (low) .. 1.0 (high)
    decision_speed: float  # 0.0 (slow) .. 1.0 (fast)
    aggression: float      # 0.0 (low) .. 1.0 (high)


class AuthenticPersonalitySystem:
    """Authentic mathematical personality parameters (no labels)."""

    def __init__(self, profile: PersonalityProfile):
        self.profile = profile
        # Precompute effect factors
        self._alpha_multiplier = 0.8 + 0.6 * profile.risk_tolerance
        self._confidence_bias = -0.05 + 0.10 * profile.aggression
        self._exploration_bias = -0.10 + 0.20 * profile.decision_speed

    def alpha_multiplier(self) -> float:
        return max(0.5, min(1.8, self._alpha_multiplier))

    def confidence_bias(self) -> float:
        return max(-0.10, min(0.10, self._confidence_bias))

    def exploration_bias(self) -> float:
        return max(-0.15, min(0.25, self._exploration_bias))

