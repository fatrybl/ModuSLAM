class BackendManagerParameters(ObjectParameters):
    def __init__(self) -> None:
        super().__init__()
        self.solver_type = str()
        self.num_iterations = int()
        self.convergence_tolerance = float()
