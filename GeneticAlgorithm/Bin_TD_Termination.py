from pymoo.core.termination import Termination
from pymoo.termination.cv import ConstraintViolationTermination
from pymoo.termination.ftol import SingleObjectiveSpaceTermination
from pymoo.termination.robust import RobustTermination
from pymoo.termination.xtol import DesignSpaceTermination
from pymoo.termination.max_time import TimeBasedTermination



class Bin_TD_Termination(Termination):
    def __init__(self, xtol=1e-8, cvtol=1e-8, ftol=1e-6, period=30, max_time = "01:00:00") -> None:
        super().__init__()
        self.x = RobustTermination(DesignSpaceTermination(xtol), period=period)
        self.cv = RobustTermination(ConstraintViolationTermination(cvtol, terminate_when_feasible=False), period=period)
        self.f = RobustTermination(SingleObjectiveSpaceTermination(ftol, only_feas=True), period=period)
        self.time = TimeBasedTermination(max_time)

        self.criteria = [self.x, self.cv, self.f, self.time]

    def _update(self, algorithm):
        p = [criterion.update(algorithm) for criterion in self.criteria]
        return max(p)
