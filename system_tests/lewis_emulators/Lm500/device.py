from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedLm500(StateMachineDevice):

    def _initialize_data(self):
        self.alarm_threshold = 10
        self.boost_mode = "OFF"
        self.analog_out = 0
        self.type = {1: 0, 2: 0}
        self.channel = 1
        self.error_response_mode = 0
        self.high_threshold = 0
        self.low_threshold = 0
        self.sample_interval = 0
        self.sensor_length = 0
        self.measurement = {1: 0, 2: 0}
        self.sample_mode = "Sample/Hold"
        self.units = "cm"
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

