from collections import OrderedDict
from .states import FillingChan1State, FillingChan2State, FillingBothState
from lewis.core.logging import has_log
from lewis.core.statemachine import State
from lewis.devices import StateMachineDevice

@has_log
class SimulatedLm500(StateMachineDevice):

    def _initialize_data(self):
        self.alarm_threshold = "10"
        self.boost_mode = "Off"
        self.analog_out = 0
        self.type = {1: 1, 2: 0}
        self.channel = 1
        self.error_response_mode = 0
        self.high_threshold = 0
        self.low_threshold = 0
        self.sample_interval = "00:00:00"
        self.sensor_length = 0
        self.measurement = {1: 0, 2: 0}
        self.value = {1: 0, 2: 0}
        self.fill_time = {1: 0, 2: 0}
        self.fill_start = {1: 0, 2: 0}
        self.sample_mode = "Sample/Hold"
        self.units = "CM"
        self.status = "0,0,0"
        self.filling = {1: False, 2: False}
        self.fill_speed = 1.0
        self.max_fill_time = 1
        self.fill_status_val = {1: "Off", 2: "Off"}

    def _get_state_handlers(self):
        return {
            'idle': State(),
            'chan1': FillingChan1State(),
            'chan2': FillingChan2State(),
            'both': FillingBothState()
        }

    def _get_initial_state(self):
        return 'idle'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('idle', 'chan1'),
             lambda: self.filling[1] is True and self.value[1] < self.high_threshold ),
            (('chan1', 'idle'), lambda: self.value[1] == self.high_threshold or self.fill_time[1] > self.max_fill_time),
            (('idle', 'chan2'),
             lambda: self.filling[2] is True and self.value[2] < self.high_threshold and self.fill_time[
                 2] < self.max_fill_time),
            (('chan2', 'idle'), lambda: self.value[2] == self.high_threshold or self.fill_time[2] > self.max_fill_time),
            (('chan1', 'both'),
             lambda: self.filling[2] is True and self.value[2] < self.high_threshold and self.fill_time[
                 2] < self.max_fill_time),
            (('chan2', 'both'),
             lambda: self.filling[1] is True and self.value[1] < self.high_threshold and self.fill_time[
                 1] < self.max_fill_time),
            (('both', 'idle'), lambda: self.value[1] == self.high_threshold and self.value[2] == self.high_threshold or
                (self.fill_time[1] > self.max_fill_time and self.fill_time[2] > self.max_fill_time)),
            (('both', 'chan1'), lambda: self.value[2] == self.high_threshold or self.fill_time[2] > self.max_fill_time),
            (('both', 'chan2'), lambda: self.value[1] == self.high_threshold or self.fill_time[1] > self.max_fill_time)
        ])

    @property
    def state(self):
        return self._csm.state

    def fill(self, channel):
        self.filling[channel] = True

    def fill_status(self, channel):
        if self.filling[channel]:
            return f"{self.fill_time[channel]} min"
        else:
            return self.fill_status_val[channel]

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
        self.measurement[channel] = self.value[channel]
