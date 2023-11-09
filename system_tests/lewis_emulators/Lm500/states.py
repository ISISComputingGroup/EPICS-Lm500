from lewis.core.statemachine import State
from lewis.core import approaches
from datetime import datetime


class FillingChan1State(State):
    def on_entry(self, dt):
        self._context.fill_start[1] = datetime.now()

    def in_state(self, dt):
        old_position = self._context.value[1]
        self._context.value[1] = approaches.linear(old_position, self._context.high_threshold,
                                                   self._context.fill_speed, dt)
        self.log.info('Filled from (%s -> %s), target=%s, speed=%s, dt=%s', old_position,
                      self._context.value[1], self._context.high_threshold, self._context.fill_speed, dt)
        self._context.fill_time[1] = round((datetime.now() - self._context.fill_start[1]).total_seconds()/60)

    def on_exit(self, dt):
        self._context.filling[1] = False
        self._context.fill_start[1] = 0
        if self._context.fill_time[1] > self._context.max_fill_time:
            self._context.fill_status[1] = "Timeout"
        else:
            self._context.fill_status[1] = "Off"
        self._context.fill_time[1] = 0


class FillingChan2State(State):
    def on_entry(self, dt):
        self._context.fill_start[2] = datetime.now()

    def in_state(self, dt):
        old_position = self._context.value[2]
        self._context.value[2] = approaches.linear(old_position, self._context.high_threshold,
                                                   self._context.fill_speed, dt)
        self.log.info('Filled from (%s -> %s), target=%s, speed=%s, dt=%s', old_position,
                      self._context.value[2], self._context.high_threshold, self._context.fill_speed, dt)

        self._context.fill_time[2] = round((datetime.now() - self._context.fill_start[1]).total_seconds() / 60)

    def on_exit(self, dt):
        self._context.filling[2] = False
        self._context.fill_start[2] = 0
        if self._context.fill_time[2] > self._context.max_fill_time:
            self._context.fill_status[2] = "Timeout"
        else:
            self._context.fill_status[2] = "Off"
        self._context.fill_time[2] = 0


class FillingBothState(State):
    def on_entry(self, dt):
        if self._context.fill_start[1] == 0:
            self._context.fill_start[1] = datetime.now()
        else:
            self._context.fill_start[2] = datetime.now()

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

    def on_exit(self, dt):
        if self._context.value[1] == self._context.high_threshold:
            self._context.filling[1] = False
            self._context.fill_start[1] = 0
            if self._context.fill_time[1] > self._context.max_fill_time:
                self._context.fill_status[1] = "Timeout"
            else:
                self._context.fill_status[1] = "Off"
            self._context.fill_time[1] = 0
        if self._context.value[2] == self._context.high_threshold:
            self._context.filling[2] = False
            self._context.fill_start[2] = 0
            if self._context.fill_time[2] > self._context.max_fill_time:
                self._context.fill_status[2] = "Timeout"
            else:
                self._context.fill_status[2] = "Off"
            self._context.fill_time[2] = 0
