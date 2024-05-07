from dataclasses import dataclass


@dataclass
class State:
    memory_limit: bool = False
    data_processed: bool = False
    time_finished: bool = False
    solver_error: bool = False


class StoppingCriterion:
    """High level criteria to stop mapping process."""

    state = State()

    @classmethod
    def is_active(cls) -> bool:
        """Checks if any of stopping criteria is active."""
        return any(cls.state.__dict__.values())

    @classmethod
    def reset(cls):
        """Resets all criteria to default values."""
        for key in cls.state.__dict__.keys():
            cls.state.__dict__[key] = False
