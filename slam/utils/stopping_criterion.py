from dataclasses import dataclass

@dataclass
class StoppingCriterion():
    is_data_processed = False
    is_time_finished = False
    is_map_diverged = False
    is_solver_error = False

    @classmethod
    def OFF(cls):
        return any(cls.__dict__.values())

    @classmethod
    def reset(cls):
        for attr in cls.__dict__.keys():
            attr = False