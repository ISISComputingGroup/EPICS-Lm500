from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply


@has_log
class Lm500StreamInterface(StreamInterface):
    
    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def __init__(self):
        super(Lm500StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder("get_alarm").escape("ALARM?").eos().build(),
            CmdBuilder("get_boost").escape("BOOST?").eos().build(),
            CmdBuilder("get_output").escape("OUT?").eos().build(),
            CmdBuilder("get_type").escape("TYPE?").eos().build(),
            CmdBuilder("get_type").escape("TYPE? ").int().eos().build(),
            CmdBuilder("get_channel").escape("CHAN?").eos().build(),
            CmdBuilder("get_error").escape("ERROR?").eos().build(),
            CmdBuilder("get_fill").escape("FILL?").eos().build(),
            CmdBuilder("get_fill").escape("FILL? ").int().eos().build(),
            CmdBuilder("get_high").escape("HIGH?").eos().build(),
            CmdBuilder("get_identity").escape("IDN?").eos().build(),
            CmdBuilder("get_interval").escape("INTVL?").eos().build(),
            CmdBuilder("get_low").escape("LOW?").eos().build(),
            CmdBuilder("get_measurement").escape("MEAS?").eos().build(),
            CmdBuilder("get_measurement").escape("MEAS? ").int().eos().build(),
            CmdBuilder("get_mode").escape("MODE?").eos().build(),
            CmdBuilder("get_length").escape("LNGTH?").eos().build(),
            CmdBuilder("get_status").escape("STAT?").eos().build(),
            CmdBuilder("get_units").escape("UNITS?").eos().build(),

            CmdBuilder("set_boost").escape("BOOST ").string().eos().build(),
            CmdBuilder("set_output").escape("OUT ").int().eos().build(),
            CmdBuilder("set_channel").escape("CHAN ").int().eos().build(),
            CmdBuilder("set_error").escape("ERROR ").int().eos().build(),
            CmdBuilder("set_fill").escape("FILL ").int().eos().build(),
            CmdBuilder("set_fill").escape("FILL").eos().build(),
            CmdBuilder("set_high").escape("HIGH ").float().eos().build(),
            CmdBuilder("set_interval").escape("INTVL ").int().escape(":").int().escape(":").int().eos().build(),
            CmdBuilder("set_low").escape("LOW ").float().eos().build(),
            CmdBuilder("set_measurement").escape("MEAS ").int().eos().build(),
            CmdBuilder("set_measurement").escape("MEAS").eos().build(),
            CmdBuilder("set_mode").escape("MODE ").char().eos().build(),
            CmdBuilder("set_units").escape("UNITS ").string().eos().build()
        }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def get_alarm(self):
        return self.device.get_alarm_threshold()

    def get_boost(self):
        return self.device.boost_mode

    def get_output(self):
        return self.device.analog_out

    def get_type(self, channel=None):
        if channel is None:
            channel = self.device.channel
        return self.device.type[channel]

    def get_channel(self):
        return self.device.channel

    def get_error(self):
        return self.device.error_response_mode

    def get_fill(self, channel=None):
        if channel is None:
            channel = self.device.channel
        return self.device.fill_status(channel)

    def get_high(self):
        return self.device.get_high_threshold()

    def get_low(self):
        return self.device.get_low_threshold()

    def get_interval(self):
        return self.device.sample_interval

    def get_identity(self):
        return self.device.identity

    def get_length(self):
        return self.device.get_sensor_length()

    def get_measurement(self, channel=None):
        if channel is None:
            channel = self.device.channel
        return self.device.get_measurement(channel)

    def get_mode(self):
        return self.device.sample_mode

    def get_status(self):
        return self.device.status

    def get_units(self):
        return self.device.units

    def set_boost(self, boost):
        self.device.boost_mode = boost
    
    def set_output(self, output):
        self.device.analog_out = output
        
    def set_channel(self, channel=None):
        self.device.channel = channel
        
    def set_error(self, set_error):
        self.device.error_response_mode = set_error
    
    def set_fill(self, channel=None):
        if channel is None:
            channel = self.device.channel
        self.device.fill(channel)
        
    def set_high(self, high):
        self.device.high_threshold = high
        
    def set_interval(self, hour, minute, second):
        self.device.sample_interval = f"{hour:02}:{minute:02}:{second:02}"
        
    def set_low(self, low):
        self.device.low_threshold = low
        
    def set_measurement(self, channel=None):
        if channel is None:
            channel = self.device.channel
        self.device.set_measurement(channel)
        
    def set_mode(self, mode):
        modes = {"0": "Disabled", "S": "Sample/Hold", "C": "Continuous"}
        self.device.set_mode = modes[mode]
        
    def set_units(self, units):
        if units in ["CM", "IN", "%"]:
            self.device.units = units
        else:
            if units == "PERCENT":
                self.device.units = "%"

