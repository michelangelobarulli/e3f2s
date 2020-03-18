import datetime
import numpy as np

sim_scenario_conf_grid = {

    "requests_rate_factor": [1],
    "n_cars_factor": [1],

    "time_estimation": [True],
    "queuing": [True],
    "alpha": np.arange(20, 80, 20),
    "beta": [80, 90, 100],

    "hub": [True],
    "hub_zone_policy": ["num_parkings"],
    "n_poles_n_cars_factor": [0.1],

    "relocation": [True],
    "finite_workers": [False],

    "distributed_cps": [True],
    "cps_placement_policy": ["num_parkings"],

    "cps_zones_percentage": [0.1],

    "user_contribution": [True],
    "system_cps": [True],
    "willingness": [0.99],

    "battery_swap": [True],

}
