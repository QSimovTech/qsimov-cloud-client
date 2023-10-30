# -*- coding: utf-8 -*-
import json
import logging
import re
import requests
import sympy as sp

from collections.abc import Iterable


_bin_regex = re.compile(r"^[01]+$")
_services = ["extra_qubits_service",
             "distances_range_service",
             "circuit_service",
             "total_states_superposed_service"]
_ancilla_modes = ['clean', 'noancilla', 'garbage', 'borrowed', 'burnable']
_url = "https://jkv6ys0nv6.execute-api.eu-west-1.amazonaws.com/test"
_logger = logging.getLogger("QsimovCloudClient")


class QsimovCloudClient(object):
    def __init__(self, token):
        if not isinstance(token, str) or token == "":
            raise ValueError("token has to be a non-empty string")
        self._data = {}
        self._data["token"] = token
        self._data["metric"] = None
        self._data["n_qubits"] = None
        self._data["state"] = None
        self._data["state_bin"] = None
        self._data["distances"] = None
        self._data["min_range"] = None
        self._data["max_range"] = None
        self._data["with_nan"] = None
        self._data["ancilla_mode"] = "clean"
        self._data["qasm_version"] = "2.0"

    def _send_request(self, service):
        if self._data["metric"] is None:
            raise ValueError("a metric has to be specified prior to sending "
                             "any request")
        if self._data["state_bin"] is None and self._data["n_qubits"] is None:
            raise ValueError("either bin or n_qubits and state have to be "
                             "specified")
        if service not in _services:
            raise ValueError("unknown service")
        values = self._data.copy()
        if (service == "circuit_service"
                or service == "total_states_superposed_service"):
            if self._data["with_nan"] is None:
                raise ValueError("with_nan has to be set when using circuit "
                                 "and total_states_superposed services")
            if (self._data["distances"] is None
                    and self._data["min_range"] is None):
                raise ValueError("either distances or min/max distance have "
                                 "to be set when using circuit and "
                                 "total_states_superposed services")
            if values["distances"] is None:
                del values["distances"]
                values["min_range"] = str(values["min_range"])
                values["max_range"] = str(values["max_range"])
            else:
                del values["min_range"]
                del values["max_range"]
                values["distances"] = [str(i) for i in values["distances"]]
        else:
            del values["with_nan"]
            del values["distances"]
            del values["min_range"]
            del values["max_range"]
            del values["ancilla_mode"]
            del values["qasm_version"]
        if values["state_bin"] is None:
            del values["state_bin"]
        else:
            del values["state"]
            del values["n_qubits"]
        values["service"] = service
        res = requests.post(_url,
                            json={"body": json.dumps(values)})
        res.raise_for_status()
        return json.loads(res.json()["body"])["response"]

    def set_metric(self, metric):
        if not isinstance(metric, str) or metric == "":
            raise ValueError("metric has to be a non-empty string")
        self._data["metric"] = metric

    def set_ancilla_mode(self, ancilla_mode):
        if ancilla_mode not in _ancilla_modes:
            raise ValueError("invalid ancilla mode")
        self._data["ancilla_mode"] = ancilla_mode

    def set_qasm_version(self, qasm_version):
        if qasm_version != "2.0" and qasm_version != "3.0":
            raise ValueError("invalid QASM version")
        self._data["qasm_version"] = qasm_version

    def set_state(self, bin=None, n_qubits=None, state=None):
        if bin is None:
            if n_qubits is None or state is None:
                raise ValueError("either bin or n_qubits and state have to be "
                                 "specified")
            if state < 0 or state >= 2**n_qubits:
                raise ValueError("the state is out of range")
            if self._data["state_bin"] is not None:
                _logger.info("state bin info overwritten")
            self._data["n_qubits"] = n_qubits
            self._data["state"] = state
            self._data["state_bin"] = None
        else:
            if not isinstance(bin, str) or _bin_regex.match(bin) is None:
                raise ValueError("bin is not a string of bits (0s and 1s)")
            if n_qubits is not None or state is not None:
                print("[WARNING] n_qubits and state parameter will be ignored "
                      "since bin has been specified")
            if self._data["n_qubits"] is not None:
                _logger.info("state and n_qubits info overwritten")
            self._data["n_qubits"] = None
            self._data["state"] = None
            self._data["state_bin"] = bin

    def can_have_nan(self, value):
        if not isinstance(value, bool):
            raise ValueError("expected a boolean value")
        self._data["with_nan"] = value

    def set_range(self, range):
        min_range = parse_number(range[0])
        max_range = parse_number(range[1])
        if min_range != sp.nan and max_range != sp.nan and min_range > max_range:
            raise ValueError("min_range is greater than max_range")
        if self._data["distances"] is not None:
            _logger.info("distances info overwritten")
        self._data["distances"] = None
        self._data["min_range"] = min_range
        self._data["max_range"] = max_range

    def set_distances(self, distances):
        if not isinstance(distances, Iterable) or isinstance(distances, str):
            raise ValueError("expected a list")
        if self._data["min_range"] is not None:
            _logger.info("range info overwritten")
        self._data["distances"] = tuple([parse_number(i) for i in distances])
        self._data["min_range"] = None
        self._data["max_range"] = None

    def calculate_extra_qubits(self):
        data = self._send_request("extra_qubits_service")
        return data["extra_qubits"]

    def calculate_distance_range(self):
        data = self._send_request("distances_range_service")
        return (data["distances_range_min"], data["distances_range_max"])

    def generate_circuit(self):
        res = self._send_request("circuit_service")
        return SuperpositionCircuit(self._data, res)

    def calculate_num_superposed(self):
        data = self._send_request("total_states_superposed_service")
        return data["total_states_superposed"]


class SuperpositionCircuit(object):
    def __init__(self, data, res):
        self._metric = data["metric"]
        self._n_qubits = data["n_qubits"]
        self._state = data["state"]
        self._bin = data["state_bin"]
        if self._bin is None:
            self._bin = ("{:0" + str(self._n_qubits) + "b}").format(self._state)
        else:
            self._n_qubits = len(self._bin)
            self._state = int(self._bin, 2)
        self._distances = data["distances"]
        self._min_range = data["min_range"]
        self._max_range = data["max_range"]
        self._with_nan = data["with_nan"]
        self._qasm_version = data["qasm_version"]
        self._ancilla_mode = data["ancilla_mode"]
        self._qasm = res["qasm_circuit"]
        self._extra_qubits = res["extra_qubits"]
        self._total_states_superposed = res["total_states_superposed"]

    def get_metric(self):
        return self._metric

    def get_state(self):
        return (self._n_qubits, self._state)

    def get_state_bin(self):
        return self._bin

    def get_range(self):
        if self._min_range is None:
            return None
        return (self._min_range, self._max_range)

    def get_distances(self):
        return self._distances

    def is_nan_allowed(self):
        return self._with_nan

    def get_extra_qubits(self):
        return self._extra_qubits

    def get_num_superposed(self):
        return self._total_states_superposed

    def get_qasm_code(self):
        return self._qasm

    def get_qasm_version(self):
        return self._qasm_version

    def get_ancilla_mode(self):
        return self._ancilla_mode


def parse_number(number):
    number = str(number)
    if number.lower() == "nan" or number == "0/0":
        return sp.Rational(0, 0)
    elif number.lower() == "inf":
        return float('inf')
    else:
        return sp.Rational(number)