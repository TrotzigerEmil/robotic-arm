from gridgraph.graph import GridGraph
from gridgraph.weight_calcs.robotic import RobotWeight
from gridgraph.phi_managers.bounded import BoundedPhiManager as pm
from math import inf


class RoboticGraphBuilder:
    def __init__(self, r, end, base):
        self.robot = r
        self.phi = base
        self.end = end
        self.lower = 1e-12

    def make_graph(self):
        ret = GridGraph(
            RobotWeight(self.robot),
            pm(self.phi, self.lower, inf)
        )

        eps = self.robot.kin_eps

        origin = self.robot.get_effector()
        diff = tuple(self.end[i] - origin[i] for i in range(3))
        endpoint = tuple(round(diff[i] / eps) for i in range(3))

        return ret, (0, 0, 0), endpoint
