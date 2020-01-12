"""
optimization.match
------------------
Mixed-integer program formulation of this group matching problem.

TODO:
- More general formulation for other chapters' requirements
- Support "mix features" on top of "split features"
    - do not allow mixing of groups by split features (e.g. time, campus)
    - prefer more diverse groups by mix features (e.g. gender, graduation year)

"""

import logging
from timeit import default_timer as timer

import pyomo.environ as pyo


LOG = logging.getLogger(__name__)

# The minimum and maximum size of the groups.
G_MIN = 6
G_MAX = 16

# The minimum number of non-female-identifying students for each group.
# Female-identifying students are the vast majority of participants, so this
# constraint attempts to diversify the groups as much as possible by adding a
# minimum of other students for group.
# GM_MIN = 2


def place_students(A, X, R):
    """
    Place the given students into groups by solving a MIP optimization.

    A, student features
        At, time
        Al, location (campus)
        Ag, graduation standing

    X, student mixing features (unused)
        Xg, gender

    R, room features
        At, time
        Al, location (campus)
        Ag, graduation standing

    """
    At, Al, Ag = A
    Xg = X
    Rt, Rl, Rg = R

    if not (At.shape[0] == Al.shape[0] == Ag.shape[0] == Xg.shape[0]):
        raise ValueError("The data provided does not have a consistent shape")
    if not (Rt.shape[0] == Rl.shape[0] == Rg.shape[0]):
        raise ValueError("The data provided does not have a consistent shape")

    n_students = At.shape[0]
    n_groups = Rt.shape[0]

    LOG.info("Building optimization model...")

    model = pyo.ConcreteModel()

    # Variables
    model.I = pyo.RangeSet(0, n_students - 1)
    model.J = pyo.RangeSet(0, n_groups - 1)

    model.s = pyo.Var(model.I, model.J, domain=pyo.Binary, initialize=0)
    model.g = pyo.Var(model.J, domain=pyo.Binary, initialize=0)

    # Objective
    def obj_expression(model):
        """
        Maximize the number of placed students.

        Due to the group size constraints, we have to do a bit of algebra to
        penalize invalid placements. If the value of a non-placement and an
        invalid placement are the same, the optimization will accept invalid
        placements that enable the creation of a new group. That is, it would
        place someone for +0, because it allows +1 for each member who otherwise
        would have gone unplaced.

        For example, for a group size minimum of 10, we set S[i][j] to:
            -10, if the placement is invalid
            0, if no placement
            1, if the placement is valid

        """
        return sum(
            (
                (-G_MIN * model.s[i, j])
                + (
                    (G_MIN + 1)
                    * model.s[i, j]
                    * At[i][Rt[j]]
                    * Al[i][Rl[j]]
                    * Ag[i][Rg[j]]
                )
            )
            for i in model.I
            for j in model.J
        )

    model.obj = pyo.Objective(rule=obj_expression, sense=pyo.maximize)

    # Constraints

    def one_placement_rule(model, i):
        """Each student may only be assigned to one group."""
        return sum(model.s[i, j] for j in model.J) <= 1

    model.C_OnePlacement = pyo.Constraint(model.I, rule=one_placement_rule)

    def group_size_lower_rule(model, j):
        """Each group (if "on") must have at least G_MIN students."""
        return sum(model.s[i, j] for i in model.I) >= G_MIN * model.g[j]

    def group_size_upper_rule(model, j):
        """Each group (if "on") must not have more than G_MAX students."""
        return sum(model.s[i, j] for i in model.I) <= G_MAX * model.g[j]

    model.C_GroupSizeLower = pyo.Constraint(model.J, rule=group_size_lower_rule)
    model.C_GroupSizeUpper = pyo.Constraint(model.J, rule=group_size_upper_rule)

    # TODO: Find a better/faster way to diversify the groups.
    # def min_non_female(model, j):
    #     """Each group (if "on") must have at least GM_MIN non-female-identifying
    #     students. This does not apply to the smaller graduate student groups."""
    #     return (
    #         sum(sum(Xg[i][1:]) * model.s[i, j] for i in model.I)
    #         >= GM_MIN * model.g[j] * Rg[j]
    #     )
    # model.C_MinNonFemale = pyo.Constraint(model.J, rule=min_non_female)

    # Solve

    opt = pyo.SolverFactory("cbc")

    LOG.info(f"Solving model ({model.nvariables()} variables)...")

    start_time = timer()
    results = opt.solve(model)
    elapsed_s = timer() - start_time

    term_condition = str(results.Solver[0]["Termination condition"])

    LOG.info(
        f"Solver returned after {elapsed_s:.2f}s, "
        f"termination condition: {term_condition}"
    )

    # Extract the returned groups
    s_output = model.s.get_values()
    g_output = model.g.get_values()

    placements = [k for k, v in s_output.items() if v == 1]
    group_ids = [k for k, v in g_output.items() if v == 1]

    group_dict = {g_id: [x for x, y in placements if y == g_id] for g_id in group_ids}
    return group_dict
