import unittest

from parameterized import parameterized
from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim

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
        self.ca.assert_setting_setpoint_sets_readback(
            mode, readback_pv="BOOST", set_point_pv="BOOST:SP"
        )

    @parameterized.expand(["Remote Select", "Channel 1", "Channel 2"])
    def test_that_WHEN_analog_output_is_set_THEN_rb_matches(self, channel):
        self.ca.assert_setting_setpoint_sets_readback(
            channel, readback_pv="OUTPUT", set_point_pv="OUTPUT:SP"
        )

    @parameterized.expand([("Disable", "Reporting Disabled"), ("Enable", "Reporting Enabled")])
    def test_that_WHEN_error_mode_is_set_THEN_rb_matches(self, mode_set, mode_read):
        self.ca.assert_setting_setpoint_sets_readback(
            mode_set, readback_pv="ERROR", set_point_pv="ERROR:SP", expected_value=mode_read
        )

    @parameterized.expand([("_zero_test", 0), ("_float_test", 0.65), ("_large_test", 6000)])
    def test_that_WHEN_high_threshold_is_set_THEN_rb_matches(self, _, threshold):
        self.ca.assert_setting_setpoint_sets_readback(
            threshold, readback_pv="HIGH", set_point_pv="HIGH:SP"
        )

    @parameterized.expand([("_zero_test", 0), ("_float_test", 0.65), ("_large_test", 6000)])
    def test_that_WHEN_low_threshold_is_set_THEN_rb_matches(self, _, threshold):
        self.ca.assert_setting_setpoint_sets_readback(
            threshold, readback_pv="LOW", set_point_pv="LOW:SP"
        )

    @parameterized.expand(
        [
            ("_below_0_test", -10, "00:00:00"),
            ("_zero_test", 0, "00:00:00"),
            ("_thirty_test", 30, "30:00:00"),
            ("_above_60_test", 70, "70:00:00"),
            ("_above_99_test", 200, "99:00:00"),
        ]
    )
    def test_that_WHEN_hour_intrvl_setpoint_set_THEN_correct_time_set_and_readback(
        self, _, hour, time
    ):
        self.ca.set_pv_value("INTRVL:HOUR:SP", hour)

        self.ca.assert_that_pv_is("INTRVL:SP.VAL", time)
        self.ca.assert_that_pv_is("INTRVL", time)

    @parameterized.expand(
        [
            ("_below_0_test", -10, "00:00:00"),
            ("_zero_test", 0, "00:00:00"),
            ("_thirty_test", 30, "00:30:00"),
            ("_above_60_test", 70, "00:60:00"),
            ("_above_99_test", 200, "00:60:00"),
        ]
    )
    def test_that_WHEN_min_intrvl_setpoint_set_THEN_correct_time_set_and_readback(
        self, _, minute, time
    ):
        self.ca.set_pv_value("INTRVL:MIN:SP", minute)

        self.ca.assert_that_pv_is("INTRVL:SP.VAL", time)
        self.ca.assert_that_pv_is("INTRVL", time)

    @parameterized.expand(
        [
            ("_below_0_test", -10, "00:00:00"),
            ("_zero_test", 0, "00:00:00"),
            ("_thirty_test", 30, "00:00:30"),
            ("_above_60_test", 70, "00:00:60"),
            ("_above_99_test", 200, "00:00:60"),
        ]
    )
    def test_that_WHEN_sec_intrvl_setpoint_set_THEN_correct_time_set_and_readback(
        self, _, sec, time
    ):
        self.ca.set_pv_value("INTRVL:SEC:SP", sec)

        self.ca.assert_that_pv_is("INTRVL:SP.VAL", time)
        self.ca.assert_that_pv_is("INTRVL", time)

    @parameterized.expand(
        [
            ("_just_hour", 10, 0, 0, "10:00:00"),
            ("_just_minute", 0, 10, 0, "00:10:00"),
            ("_just_second", 0, 0, 10, "00:00:10"),
            ("_hour_and_minute", 10, 20, 0, "10:20:00"),
            ("_hour_and_second", 10, 0, 20, "10:00:20"),
            ("_minute_and_second", 0, 10, 20, "00:10:20"),
            ("_all", 10, 20, 30, "10:20:30"),
        ]
    )
    def test_that_WHEN_multiple_intrvls_set_THEN_correct_time_set_and_readback(
        self, _, hour, minute, sec, time
    ):
        self.ca.set_pv_value("INTRVL:HOUR:SP", hour)
        self.ca.set_pv_value("INTRVL:MIN:SP", minute)
        self.ca.set_pv_value("INTRVL:SEC:SP", sec)

        self.ca.assert_that_pv_is("INTRVL:SP.VAL", time)
        self.ca.assert_that_pv_is("INTRVL", time)

    @parameterized.expand(["Disabled", "Sample/Hold", "Continuous"])
    def test_that_WHEN_mode_is_set_THEN_rb_matches(self, mode):
        self.ca.assert_setting_setpoint_sets_readback(
            mode, readback_pv="MODE", set_point_pv="MODE:SP"
        )

    @parameterized.expand(["Channel 1", "Channel 2"])
    def test_that_WHEN_default_channel_is_set_THEN_rb_matches(self, channel):
        self.ca.assert_setting_setpoint_sets_readback(
            channel, readback_pv="CHANNEL", set_point_pv="CHANNEL:SP"
        )

    def test_that_WHEN_default_channel_is_changed_THEN_channel_type_matches(self):
        type_1 = self.ca.get_pv_value("TYPE:CHAN1")
        type_2 = self.ca.get_pv_value("TYPE:CHAN2")

        self.ca.assert_setting_setpoint_sets_readback(
            "Channel 1", readback_pv="TYPE", set_point_pv="CHANNEL:SP", expected_value=type_1
        )
        self.ca.assert_setting_setpoint_sets_readback(
            "Channel 2", readback_pv="TYPE", set_point_pv="CHANNEL:SP", expected_value=type_2
        )

    @parameterized.expand(["CM", "IN", "%"])
    @skip_if_recsim("Gets correct EGU setting from device, so will fail in recsim")
    def test_that_WHEN_units_set_THEN_readback_AND_egu_updates(self, units):
        self.ca.assert_setting_setpoint_sets_readback(
            units, readback_pv="UNITS", set_point_pv="UNITS:SP"
        )
        self.ca.assert_that_pv_is("HIGH.EGU", units)
        self.ca.assert_that_pv_is("LOW.EGU", units)
        self.ca.assert_that_pv_is("MEAS.EGU", units)
        self.ca.assert_that_pv_is("MEAS:CHAN1.EGU", units)
        self.ca.assert_that_pv_is("MEAS:CHAN2.EGU", units)
        self.ca.assert_that_pv_is("LENGTH.EGU", units)
        self.ca.assert_that_pv_is("ALARM.EGU", units)

    @parameterized.expand(
        [
            ("_all_0", "00000000", "00000000", 0, [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]),
            ("_all_1", "01111111", "01111111", 1, [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]),
            (
                "_chan_1_all_1",
                "01111111",
                "00000000",
                0,
                [1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0],
            ),
            (
                "_chan_2_all_1",
                "00000000",
                "01111111",
                0,
                [0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1],
            ),
            (
                "burnout_detected",
                "01000000",
                "00000000",
                0,
                [1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ),
            (
                "open_sensor",
                "00100000",
                "00000000",
                0,
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ),
            (
                "alarm_limit",
                "00010000",
                "00000000",
                0,
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ),
            (
                "auto_refill",
                "00001000",
                "00000000",
                0,
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ),
            (
                "refill_timeout",
                "00000100",
                "00000000",
                0,
                [0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ),
            (
                "refill_active",
                "00000010",
                "00000000",
                0,
                [0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ),
            (
                "read_in_progress",
                "00000001",
                "00000000",
                0,
                [0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0],
            ),
        ]
    )
    @skip_if_recsim("Uses emulator backdoor")
    def test_that_WHEN_status_bits_set_THEN_correctly_seperated(
        self, _, int1, int2, int3, first_bits, second_bits
    ):
        modes = ["Operate Mode", "Menu Mode"]
        self._lewis.backdoor_set_on_device("status", f"{int(int1, 2)},{int(int2, 2)},{int3}")
        self.ca.assert_that_pv_is_number("STATUS:BIT:0", int(int1, 2))
        self.ca.assert_that_pv_is_number("STATUS:BIT:1", int(int2, 2))
        self.ca.assert_that_pv_is("MENU:MODE", modes[int3])
        pvs = [
            "BURNOUT",
            "SENSOR:STATUS",
            "ALARM:STATUS",
            "REFILL:INHIBITED",
            "REFILL:TIMEOUT",
            "REFILL",
            "READ",
        ]
        pv = 0
        for bit in first_bits:
            self.ca.assert_that_pv_is_number(f"CHAN1:{pvs[pv]}.RVAL", bit)
            pv = pv + 1

        pv = 0
        for bit in second_bits:
            self.ca.assert_that_pv_is_number(f"CHAN2:{pvs[pv]}.RVAL", bit)
            pv = pv + 1
