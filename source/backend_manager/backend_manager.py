class BackendManager():
    def __init__(self):
        """
        base attributes
        """
        self.solver = GraphSolver()

    def solve(self):
        pass
    
    def setup(self):
        cfg = Config()
        if cfg.use_something:
            self.something = Something()