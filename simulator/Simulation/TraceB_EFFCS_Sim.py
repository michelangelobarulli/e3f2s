import itertools
import datetime

import numpy as np

from simulator.utils.car_utils import *
from simulator.Simulation.EFFCS_Sim import EFFCS_Sim

class TraceB_EFFCS_Sim (EFFCS_Sim):

    def init_data_structures(self):

        self.booking_request_arrival_rates = \
            self.simInput.request_rates
        self.trip_kdes = self.simInput.trip_kdes
        self.od_distances = self.simInput.od_distances
        self.valid_zones = self.simInput.valid_zones
        self.update_data_structures()

    def update_time_info(self):

        self.hours_spent += 1

        self.current_datetime = self.start + \
                                datetime.timedelta(seconds=self.env.now)
        self.current_hour = self.current_datetime.hour
        self.current_weekday = \
            self.current_datetime.weekday()
        if self.current_weekday in [5, 6]:
            self.current_daytype = "weekend"
        else:
            self.current_daytype = "weekday"

    def update_data_structures(self):

        self.current_arrival_rate = \
            self.booking_request_arrival_rates \
                [self.current_daytype] \
                [self.current_hour]

        self.current_trip_kde = \
            self.trip_kdes \
                [self.current_daytype] \
                [self.current_hour]

    def update_req_time_info (self, booking_request):

        booking_request["date"] = \
            booking_request["start_time"].date()
        booking_request["hour"] = \
            booking_request["start_time"].hour
        booking_request["weekday"] = \
            booking_request["start_time"].weekday()
        if booking_request["weekday"] in [5, 6]:
            booking_request["daytype"] = "weekend"
        else:
            booking_request["daytype"] = "weekday"
        return booking_request

    def fuel_to_electric (self, booking_request):

        booking_request["euclidean_distance_trace"] = \
            booking_request["euclidean_distance"]            

        booking_request["soc_delta_trace"] = \
            -get_soc_delta(booking_request["euclidean_distance_trace"])

        booking_request["euclidean_distance"] = \
            self.od_distances.loc\
            [booking_request["origin_id"], 
             booking_request["destination_id"]] / 1000

        booking_request["soc_delta"] = \
            -get_soc_delta(booking_request["euclidean_distance"])

        booking_request["soc_delta_kwh"] = \
            soc_to_kwh(booking_request["soc_delta"])        

        return booking_request
    
    def mobility_requests_generator(self):

        self.od_distances = self.simInput.od_distances
        self.init_data_structures()

        for booking_request in self.simInput.booking_requests_list:
            self.update_time_info()
            self.update_data_structures()
            booking_request = self.update_req_time_info(booking_request)
            booking_request = self.fuel_to_electric(booking_request)
            timeout_sec = \
                (np.random.exponential \
                     (1 / self.simInput.sim_scenario_conf \
                         ["requests_rate_factor"] \
                      / self.current_arrival_rate))

            yield self.env.timeout(timeout_sec)
            self.process_booking_request(booking_request)
