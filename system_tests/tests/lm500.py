import unittest

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim
from parameterized import parameterized


DEVICE_PREFIX = "LM500_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("LM500"),
        "macros": {},
        "emulator": "Lm500",
    },
]


TEST_MODES = [TestModes.RECSIM, TestModes.DEVSIM]


class Lm500Tests(unittest.TestCase):
    """
    Tests for the Lm500 IOC.
    """
    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("Lm500", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)
        self.ca.set_pv_value("INTRVL:HOUR:SP", 0)
        self.ca.set_pv_value("INTRVL:MIN:SP", 0)
        self.ca.set_pv_value("INTRVL:SEC:SP", 0)

    @parameterized.expand(["Off", "On", "Smart"])
    def test_that_WHEN_boost_mode_is_set_THEN_rb_matches(self, mode):
        self.ca.assert_setting_setpoint_sets_readback(mode, readback_pv="BOOST:RB", set_point_pv="BOOST:SP")

    @parameterized.expand(["Remote Select", "Channel 1", "Channel 2"])
    def test_that_WHEN_analog_output_is_set_THEN_rb_matches(self, channel):
        self.ca.assert_setting_setpoint_sets_readback(channel, readback_pv="OUTPUT:RB", set_point_pv="OUTPUT:SP")

    @parameterized.expand([("Disable", "Reporting Disabled"), ("Enable", "Reporting Enabled")])
    def test_that_WHEN_error_mode_is_set_THEN_rb_matches(self, mode_set, mode_read):
        self.ca.assert_setting_setpoint_sets_readback(mode_set, readback_pv="ERROR:RB", set_point_pv="ERROR:SP",
                                                      expected_value=mode_read)

    @parameterized.expand([("_zero_test", 0), ("_float_test", 0.65), ("_large_test", 6000)])
    def test_that_WHEN_high_threshold_is_set_THEN_rb_matches(self, _, threshold):
        self.ca.assert_setting_setpoint_sets_readback(threshold, readback_pv="HIGH:RB", set_point_pv="HIGH:SP")

    @parameterized.expand([("_zero_test", 0), ("_float_test", 0.65), ("_large_test", 6000)])
    def test_that_WHEN_low_threshold_is_set_THEN_rb_matches(self, _, threshold):
        self.ca.assert_setting_setpoint_sets_readback(threshold, readback_pv="LOW:RB", set_point_pv="LOW:SP")

    @parameterized.expand([("_below_0_test", -10, "00:00:00"),("_zero_test", 0, "00:00:00"),
                           ("_thirty_test", 30, "30:00:00"), ("_above_60_test", 70, "70:00:00"),
                           ("_above_99_test", 200, "99:00:00")])
    def test_that_WHEN_hour_intrvl_setpoint_set_THEN_correct_time_set_and_readback(self, _, hour, time):
        self.ca.set_pv_value("INTRVL:HOUR:SP", hour)

        self.ca.assert_that_pv_is("INTRVL:SP.SVAL", time)
        self.ca.assert_that_pv_is("INTRVL:RB", time)

    @parameterized.expand([("_below_0_test", -10, "00:00:00"), ("_zero_test", 0, "00:00:00"),
                           ("_thirty_test", 30, "00:30:00"), ("_above_60_test", 70, "00:60:00"),
                           ("_above_99_test", 200, "00:60:00")])
    def test_that_WHEN_min_intrvl_setpoint_set_THEN_correct_time_set_and_readback(self, _, minute, time):
        self.ca.set_pv_value("INTRVL:MIN:SP", minute)

        self.ca.assert_that_pv_is("INTRVL:SP.SVAL", time)
        self.ca.assert_that_pv_is("INTRVL:RB", time)

    @parameterized.expand([("_below_0_test", -10, "00:00:00"), ("_zero_test", 0, "00:00:00"),
                           ("_thirty_test", 30, "00:00:30"), ("_above_60_test", 70, "00:00:60"),
                           ("_above_99_test", 200, "00:00:60")])
    def test_that_WHEN_sec_intrvl_setpoint_set_THEN_correct_time_set_and_readback(self, _, sec, time):
        self.ca.set_pv_value("INTRVL:SEC:SP", sec)

        self.ca.assert_that_pv_is("INTRVL:SP.SVAL", time)
        self.ca.assert_that_pv_is("INTRVL:RB", time)

    @parameterized.expand([("_just_hour", 10, 0, 0,  "10:00:00"), ("_just_minute", 0, 10, 0, "00:10:00"),
                           ("_just_second", 0, 0, 10, "00:00:10"), ("_hour_and_minute", 10, 20, 0, "10:20:00"),
                           ("_hour_and_second", 10, 0, 20, "10:00:20"), ("_minute_and_second", 0, 10, 20, "00:10:20"),
                           ("_all", 10, 20, 30, "10:20:30")])
    def test_that_WHEN_multiple_intrvls_set_THEN_correct_time_set_and_readback(self, _, hour, minute, sec, time):
        self.ca.set_pv_value("INTRVL:HOUR:SP", hour)
        self.ca.set_pv_value("INTRVL:MIN:SP", minute)
        self.ca.set_pv_value("INTRVL:SEC:SP", sec)

        self.ca.assert_that_pv_is("INTRVL:SP.SVAL", time)
        self.ca.assert_that_pv_is("INTRVL:RB", time)

    @parameterized.expand([("Disabled", "0"), ("Sample/Hold", "S"), ("Continuous", "C")])
    def test_that_WHEN_mode_is_set_THEN_rb_matches(self, mode_set, mode):
        self.ca.assert_setting_setpoint_sets_readback(mode_set, readback_pv="MODE:RB", set_point_pv="MODE:SP",
                                                      expected_value=mode)

    @parameterized.expand(["Channel 1", "Channel 2"])
    def test_that_WHEN_default_channel_is_set_THEN_rb_matches(self, channel):
        self.ca.assert_setting_setpoint_sets_readback(channel, readback_pv="CHANNEL:RB", set_point_pv="CHANNEL:SP")

    def test_that_WHEN_default_channel_is_changed_THEN_channel_type_matches(self):
        type_1 = self.ca.get_pv_value("TYPE:CHAN1:RB")
        type_2 = self.ca.get_pv_value("TYPE:CHAN2:RB")

        self.ca.assert_setting_setpoint_sets_readback("Channel 1", readback_pv="TYPE:RB", set_point_pv="CHANNEL:SP",
                                                      expected_value=type_1)
        self.ca.assert_setting_setpoint_sets_readback("Channel 2", readback_pv="TYPE:RB", set_point_pv="CHANNEL:SP",
                                                      expected_value=type_2)

    @skip_if_recsim("Gets correct EGU setting from device, so will fail in recsim")
    @parameterized.expand(["CM", "IN", "%"])
    def test_that_WHEN_units_set_THEN_readback_AND_egu_updates(self, units):
        self.ca.assert_setting_setpoint_sets_readback(units, readback_pv="UNITS:RB", set_point_pv="UNITS:SP")
        self.ca.assert_that_pv_is("HIGH:RB.EGU", units)
        self.ca.assert_that_pv_is("LOW:RB.EGU", units)
        self.ca.assert_that_pv_is("MEAS:RB.EGU", units)
        self.ca.assert_that_pv_is("MEAS:CHAN1:RB.EGU", units)
        self.ca.assert_that_pv_is("MEAS:CHAN2:RB.EGU", units)
        self.ca.assert_that_pv_is("LENGTH:RB.EGU", units)
        self.ca.assert_that_pv_is("ALARM:RB.EGU", units)










