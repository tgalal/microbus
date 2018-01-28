from microbus.scheduler import BusScheduler


class DisjointRoutesBusScheduler(BusScheduler):
    def __init__(self, bus):
        super(DisjointRoutesBusScheduler, self).__init__(bus)
        self.scheduledAssignments = []
        self.currentAssignment = None

    def verify_route(self, route):
        if self.currentAssignment is not None and route in self.currentAssignment:
            # logger.info("Route in current assignment")
            return False

        for assignment in self.scheduledAssignments:
            if route in assignment.route:
                # logger.info("Route in scheduled assignments")
                return False

        return True

    def schedule_assignment(self, assignment):
        if self.verify_route(assignment.route):
            self.scheduledAssignments.append(assignment)
            super(DisjointRoutesBusScheduler, self).schedule_assignment(lambda: self.execute_assignment(assignment))

    def execute_assignment(self, assignment):
        self.currentAssignment = assignment
        self.remove_scheduled_assignment(assignment)
        assignment()
        self.currentAssignment = None

    def remove_scheduled_assignment(self, assignment):
        self.scheduledAssignments.pop(self.scheduledAssignments.index(assignment))
