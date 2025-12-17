class DuplicatePlanError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class SubscriptionNotFoundError(Exception):
    pass


class PlanNotFoundError(Exception):
    pass


class SubscriptionConflictError(Exception):
    pass