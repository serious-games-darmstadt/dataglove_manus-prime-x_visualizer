"""
Joint constraints.
"""

# Normalized Ranges
CONSTRAINT_NORM = (0.0, 1.0)
SPREAD_FINGER_CONSTRAINT_NORM = (-1.0, 1.0)

# Thumb constraints in degrees
SPREAD_THUMB_CMC_CONSTRAINT_DEGR = (5.0, 50.0)  # old: (0.0, 45.0)
STRETCH_THUMB_CMC_CONSTRAINT_DEGR = (-20.0, 25.0)  # old: (-40.0, 5.0)
STRETCH_THUMB_MCP_CONSTRAINT_DEGR = (-20.0, 45.0)  # old: (0.0, 55.0)
STRETCH_THUMB_IP_CONSTRAINT_DEGR = (-15.0, 80.0)  # old: (0.0, 80.0)

# Finger constraints in degrees
SPREAD_FINGER_CONSTRAINT_DEGR = (-20.0, 20.0)
STRETCH_FINGER_MCP_REST_CONSTRAINT_DEGR = (0.0, 80.0)  # old: (-40.0, 5.0)
STRETCH_FINGER_PIP_CONSTRAINT_DEGR = (0.0, 100.0)  # old: (-40.0, 5.0)
STRETCH_FINGER_DIP_CONSTRAINT_DEGR = (0.0, 90.0)  # old: (-40.0, 5.0)


"""
Conversion from normalized values to degrees.
"""
def scale_range_for_value(from_min: float, from_max: float, to_min: float,
                          to_max: float, x: float) -> float:
    """
    Transforms a given value from one range into another. Used to convert
    normalized values into degrees.
    https://stackoverflow.com/questions/5294955/how-to-scale-down-a-range-of-numbers-with-a-known-min-and-max-value
    :param from_min: Lower bound of first range.
    :param from_max: Upper bound of first range.
    :param to_min: Lower bound of second range.
    :param to_max: Upper bound of second range.
    :param x: The value that should be scaled into another range.
    :return: Scaled value into the second range.
    """
    return ((to_max - to_min) * (x - from_min)) / (from_max - from_min) + to_min


def get_spread_thumb_cmc_constraint_degree(norm_value: float) -> float:
    """
    Transforms the normalized bend/flex value into degrees.
    :param norm_value: Normalized value.
    :return: Value in degree.
    """
    from_lower_bound = CONSTRAINT_NORM[0]
    from_upper_bound = CONSTRAINT_NORM[1]
    to_lower_bound = SPREAD_THUMB_CMC_CONSTRAINT_DEGR[0]
    to_upper_bound = SPREAD_THUMB_CMC_CONSTRAINT_DEGR[1]
    return scale_range_for_value(from_lower_bound, from_upper_bound,
                                 to_lower_bound, to_upper_bound, norm_value)


def get_spread_finger_constraint_degree(norm_value: float) -> float:
    from_lower_bound = SPREAD_FINGER_CONSTRAINT_NORM[0]
    from_upper_bound = SPREAD_FINGER_CONSTRAINT_NORM[1]
    to_lower_bound = SPREAD_FINGER_CONSTRAINT_DEGR[0]
    to_upper_bound = SPREAD_FINGER_CONSTRAINT_DEGR[1]
    return scale_range_for_value(from_lower_bound, from_upper_bound,
                                 to_lower_bound, to_upper_bound, norm_value)


def get_stretch_thumb_cmc_constraint_degree(norm_value: float) -> float:
    from_lower_bound = CONSTRAINT_NORM[0]
    from_upper_bound = CONSTRAINT_NORM[1]
    to_lower_bound = STRETCH_THUMB_CMC_CONSTRAINT_DEGR[0]
    to_upper_bound = STRETCH_THUMB_CMC_CONSTRAINT_DEGR[1]
    return scale_range_for_value(from_lower_bound, from_upper_bound,
                                 to_lower_bound, to_upper_bound, norm_value)


def get_stretch_thumb_mcp_constraint_degree(norm_value: float) -> float:
    from_lower_bound = CONSTRAINT_NORM[0]
    from_upper_bound = CONSTRAINT_NORM[1]
    to_lower_bound = STRETCH_THUMB_MCP_CONSTRAINT_DEGR[0]
    to_upper_bound = STRETCH_THUMB_MCP_CONSTRAINT_DEGR[1]
    return scale_range_for_value(from_lower_bound, from_upper_bound,
                                 to_lower_bound, to_upper_bound, norm_value)


def get_stretch_thumb_ip_constraint_degree(norm_value: float) -> float:
    from_lower_bound = CONSTRAINT_NORM[0]
    from_upper_bound = CONSTRAINT_NORM[1]
    to_lower_bound = STRETCH_THUMB_IP_CONSTRAINT_DEGR[0]
    to_upper_bound = STRETCH_THUMB_IP_CONSTRAINT_DEGR[1]
    return scale_range_for_value(from_lower_bound, from_upper_bound,
                                 to_lower_bound, to_upper_bound, norm_value)


def get_stretch_finger_pip_constraint_degree(norm_value: float) -> float:
    from_lower_bound = CONSTRAINT_NORM[0]
    from_upper_bound = CONSTRAINT_NORM[1]
    to_lower_bound = STRETCH_FINGER_PIP_CONSTRAINT_DEGR[0]
    to_upper_bound = STRETCH_FINGER_PIP_CONSTRAINT_DEGR[1]
    return scale_range_for_value(from_lower_bound, from_upper_bound,
                                 to_lower_bound, to_upper_bound, norm_value)


def get_stretch_finger_dip_constraint_degree(norm_value: float) -> float:
    from_lower_bound = CONSTRAINT_NORM[0]
    from_upper_bound = CONSTRAINT_NORM[1]
    to_lower_bound = STRETCH_FINGER_DIP_CONSTRAINT_DEGR[0]
    to_upper_bound = STRETCH_FINGER_DIP_CONSTRAINT_DEGR[1]
    return scale_range_for_value(from_lower_bound, from_upper_bound,
                                 to_lower_bound, to_upper_bound, norm_value)


def get_stretch_finger_mcp_rest_constraint_degree(norm_value: float) -> float:
    from_lower_bound = CONSTRAINT_NORM[0]
    from_upper_bound = CONSTRAINT_NORM[1]
    to_lower_bound = STRETCH_FINGER_MCP_REST_CONSTRAINT_DEGR[0]
    to_upper_bound = STRETCH_FINGER_MCP_REST_CONSTRAINT_DEGR[1]
    return scale_range_for_value(from_lower_bound, from_upper_bound,
                                 to_lower_bound, to_upper_bound, norm_value)
