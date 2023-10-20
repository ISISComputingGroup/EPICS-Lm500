from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedLm500(StateMachineDevice):

    def _initialize_data(self):
        self.alarm_threshold = "10"
        self.boost_mode = "Off"
        self.analog_out = 0
        self.type = {1: 1, 2: 0}
        self.channel = 1
        self.error_response_mode = 0
        self.high_threshold = "0"
        self.low_threshold = "0"
        self.sample_interval = "00:00:00"
        self.sensor_length = "0"
        self.measurement = {1: "0", 2: "0"}
        self.sample_mode = "Sample/Hold"
        self.units = "CM"
        self.status = "0,0,0"
        self.filling = {1: False, 2: False}

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def fill(self, channel):
        self.filling[channel] = True

    def fill_status(self, channel):
        if self.filling[channel]:
            return "2 min"
        else:
            return "Off"

    def get_alarm_threshold(self):
        return f"{self.alarm_threshold} {self.units}"

    def get_high_threshold(self):
        return f"{self.high_threshold} {self.units}"

    def get_low_threshold(self):
        return f"{self.low_threshold} {self.units}"

    def get_sensor_length(self):
        return f"{self.sensor_length} {self.units}"

    def get_measurement(self, channel):
        return f"{self.measurement[channel]} {self.units}"

    def set_measurement(self, channel):
        self.measurement[channel] = "25"

