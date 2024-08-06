from datetime import datetime

from lewis.core import approaches
from lewis.core.statemachine import State


class resetState(State):
    def reset_fill(self, channel):
        self._context.fill_start[channel] = 0
        self._context.filling[channel] = False
        self._context.fill_time[channel] = 0
        if self._context.fill_status_val[channel] != "Timeout":
            self._context.fill_status_val[channel] = "Off"

class IdleState(resetState):
    def on_entry(self, dt):
        self.reset_fill(1)
        self.reset_fill(2)

class FillingChan1State(resetState):
    def on_entry(self, dt):
        self._context.fill_start[1] = datetime.now()
        self.reset_fill(2)
        self._context.log.info(f"Start 1 {self._context.fill_start[1]}")
        self._context.log.info(f"Start 2 {self._context.fill_start[2]}")

    def in_state(self, dt):
        old_position = self._context.value[1]
        self._context.value[1] = approaches.linear(old_position, self._context.high_threshold,
                                                   self._context.fill_speed, dt)
        self.log.info('Filled from (%s -> %s), target=%s, speed=%s, dt=%s', old_position,
                      self._context.value[1], self._context.high_threshold, self._context.fill_speed, dt)
        self._context.fill_time[1] = round((datetime.now() - self._context.fill_start[1]).total_seconds()/60)

    def on_exit(self, dt):
        if self._context.fill_time[1] > self._context.max_fill_time:
            self._context.fill_status_val[1] = "Timeout"


class FillingChan2State(resetState):
    def on_entry(self, dt):
        self._context.fill_start[2] = datetime.now()
        self.reset_fill(1)
        self._context.log.info(f"Start 1 {self._context.fill_start[1]}")
        self._context.log.info(f"Start 2 {self._context.fill_start[2]}")

    def in_state(self, dt):
        old_position = self._context.value[2]
        self._context.value[2] = approaches.linear(old_position, self._context.high_threshold,
                                                   self._context.fill_speed, dt)
        self.log.info('Filled from (%s -> %s), target=%s, speed=%s, dt=%s', old_position,
                      self._context.value[2], self._context.high_threshold, self._context.fill_speed, dt)

        self._context.fill_time[2] = round((datetime.now() - self._context.fill_start[2]).total_seconds() / 60)

    def on_exit(self, dt):
        if self._context.fill_time[2] > self._context.max_fill_time:
            self._context.fill_status_val[2] = "Timeout"



class FillingBothState(State):
    def on_entry(self, dt):
        self._context.log.info(f"Start 1 {self._context.fill_start[1]}")
        self._context.log.info(f"Start 2 {self._context.fill_start[2]}")
        if self._context.fill_start[1] == 0:
            self._context.fill_start[1] = datetime.now()
        else:
            self._context.fill_start[2] = datetime.now()
        self._context.log.info(f"Start 1 {self._context.fill_start[1]}")
        self._context.log.info(f"Start 2 {self._context.fill_start[2]}")

    def in_state(self, dt):
        old_position = self._context.value[1]
        self._context.value[1] = approaches.linear(old_position, self._context.high_threshold,
                                                   self._context.fill_speed, dt)
        self.log.info('Filled from (%s -> %s), target=%s, speed=%s', old_position,
                      self._context.value[1], self._context.high_threshold, self._context.fill_speed)
        old_position = self._context.value[2]
        self._context.value[2] = approaches.linear(old_position, self._context.high_threshold,
                                                   self._context.fill_speed, dt)
        self.log.info('Filled from (%s -> %s), target=%s, speed=%s', old_position,
                      self._context.value[2], self._context.high_threshold, self._context.fill_speed)
        self._context.fill_time[1] = round((datetime.now() - self._context.fill_start[1]).total_seconds() / 60)
        self._context.fill_time[2] = round((datetime.now() - self._context.fill_start[2]).total_seconds() / 60)

    def on_exit(self, dt):
        if self._context.value[1] == self._context.high_threshold:
            if self._context.fill_time[1] > self._context.max_fill_time:
                self._context.fill_status_val[1] = "Timeout"
        if self._context.value[2] == self._context.high_threshold:
            if self._context.fill_time[2] > self._context.max_fill_time:
                self._context.fill_status_val[2] = "Timeout"
