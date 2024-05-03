from pathlib import Path
import random
import string
import typing
from typing import Dict, List, get_args

from nightskyrunner.status import RunnerStatusDict, StatusDict
import pytest

from nightskycam_serialization.command import (
    CommandResult,
    deserialize_command,
    deserialize_command_result,
    serialize_command,
    serialize_command_result,
)
from nightskycam_serialization.config import (
    deserialize_config_update,
    serialize_config_update,
)
from nightskycam_serialization.fix import deserialize_fix_dict, serialize_fix_dict
from nightskycam_serialization.serialize import (
    ImproperMessage,
    IncorrectToken,
    deserialize,
    serialize,
)
from nightskycam_serialization.status import (
    NightskycamRunner,
    RunnerClasses,
    deserialize_status,
    get_random_status_dict,
    get_runner_status_dict_class,
    get_status_entries_report,
    has_runner_status_dict,
    has_status_entries_report_function,
    serialize_status,
)


def test_serialize() -> None:
    """
    Checking serialize and deserialize functions.
    """

    din = {"A": 1, "B": "message", "C": {"c1": 9.2, "c2": ["c21", "c22"]}}

    message = serialize(din)

    dout = deserialize(message, required_keys=("A", "B", "C"))

    assert dout == din

    token = "supersecrettoken"
    message = serialize(din, token=token)

    with pytest.raises(IncorrectToken):
        deserialize(message, token="notthesametoken")

    dout = deserialize(message, required_keys=("A", "B", "C"))

    assert dout == din


def test_required_keys() -> None:
    """
    Testing deserialize raises an ImproperMessage error
    when a required key is missing.
    """
    message = serialize({str(a): a for a in range(3)})

    deserialize(message, required_keys=[str(a) for a in range(3)])
    deserialize(message, required_keys=("1",))
    deserialize(message, required_keys=[])

    with pytest.raises(ImproperMessage):
        deserialize(message, required_keys=("4",))


def test_fix() -> None:
    """
    Testing serialize_fix_dict and deserialize_fix_dict
    """
    path = "/path/to/file"

    din = {"A": 1, "B": Path(path), "C": None}

    dfixed = serialize_fix_dict(din)

    assert dfixed["C"] is not None
    assert not isinstance(dfixed["B"], Path)

    dout = deserialize_fix_dict(dfixed)

    assert dout["A"] == 1
    assert dout["B"] == path
    assert dout["C"] is None


def test_command() -> None:
    """
    Testing serialize_command and deserialize_command
    """

    command_id = 4
    command = "ls /"

    message = serialize_command(command_id, command)

    command_out = deserialize_command(message)

    assert command_out[0] == command_id
    assert command_out[1] == command


def test_command_result() -> None:
    """
    Testing serialize_command_result and deserialize_command_result
    """
    command_id = 5
    command = "ls /"
    stdout = "all ok"
    stderr = "no error"
    exit_code = "12"
    error = ""

    result_in = CommandResult(command_id, command, stdout, stderr, exit_code, error)
    message = serialize_command_result(result_in)
    result_out = deserialize_command_result(message)

    assert result_in == result_out


def test_config() -> None:
    """
    Testing serialize_config_update and
    deserialize_config_update
    """
    runner = "myrunner"
    config = {"A": "a", "B": None, "C": 0.1}

    message = serialize_config_update(runner, config)

    out = deserialize_config_update(message)

    assert out[0] == runner
    assert out[1]["A"] == "a"
    assert out[1]["B"] is None
    assert out[1]["C"] == 0.1


def test_runner_classes() -> None:
    """
    Testing consistancy between NightskycamRunner literals
    and RunnerClasses enumeration.
    """

    for rc in RunnerClasses:
        assert rc.name == rc.value
        assert rc.name in get_args(NightskycamRunner)
    for nr in get_args(NightskycamRunner):
        assert nr in list(RunnerClasses.__members__.keys())


def test_status() -> None:
    """
    Testing serialize_status and deserialize_status.
    """
    system = "my_system"

    class StatusTest1(RunnerStatusDict, total=False):
        E11: str
        E12: str

    class StatusTest2(RunnerStatusDict, total=False):
        E2: str

    status1 = StatusDict(
        name="status1",
        entries=StatusTest1(E11="e11", E12="e12"),
        activity="taking picture",
        state="running",
        running_for="3 minutes 4 seconds",
    )

    status2 = StatusDict(
        name="status2",
        entries=StatusTest2(E2="e2"),
        activity="waiting",
        state="sleeping",
        running_for="12 minutes 5 seconds",
    )

    message = serialize_status(system, (status1, status2))

    out = deserialize_status(message)

    assert out[0] == system

    all_status = out[1]
    assert len(all_status) == 2

    s1 = all_status["status1"]
    assert s1 == status1

    s2 = all_status["status2"]
    assert s2 == status2


def test_get_status_entries_report():
    runner_classes = tuple(NightskycamRunner.__args__)

    for runner_class_name in runner_classes:
        assert has_runner_status_dict(runner_class_name)

    assert has_status_entries_report_function("CamRunner")
    assert has_status_entries_report_function("CommandRunner")
    assert has_status_entries_report_function("FtpRunner")
    assert has_status_entries_report_function("LocationInfoRunner")
    assert has_status_entries_report_function("SleepyPiRunner")
    assert has_status_entries_report_function("SpaceKeeperRunner")

    assert not has_status_entries_report_function("StatusRunner")
    assert not has_status_entries_report_function("ConfigRunner")

    for runner_class_name in runner_classes:
        for _ in range(5):
            runner_status_dict = get_random_status_dict(runner_class_name)
            assert len(runner_status_dict) != 0
            report = get_status_entries_report({runner_class_name: runner_status_dict})
            if has_status_entries_report_function(runner_class_name):
                assert len(report) != 0
            else:
                assert len(report) == 0

    def generate_random_instances() -> Dict[str, RunnerStatusDict]:
        rc = random.sample(runner_classes, random.randint(0, len(runner_classes)))
        return {r: get_random_status_dict(r) for r in rc}

    for _ in range(50):
        runner_status_dicts = generate_random_instances()

        report = get_status_entries_report(runner_status_dicts)
