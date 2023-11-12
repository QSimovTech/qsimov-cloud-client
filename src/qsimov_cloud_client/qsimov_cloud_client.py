# -*- coding: utf-8 -*-
import json
import logging
import re
import requests
import sympy as sp

from collections.abc import Iterable
from requests.adapters import HTTPAdapter, Retry


_bin_regex = re.compile(r"^[01]+$")
_services = ["extra_qubits_service",
             "distances_range_service",
             "circuit_service",
             "total_states_superposed_service"]
_ancilla_modes = ['clean', 'noancilla', 'garbage', 'borrowed', 'burnable']
_url = "https://qcaas.qsimov.com/superpositions"
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
                or service == "total_states_superposed_service"
                or service == "extra_qubits_service"):
            if self._data["with_nan"] is None:
                raise ValueError("with_nan has to be set when using circuit, "
                                 "extra_qubits and total_states_superposed "
                                 "services")
            if (self._data["distances"] is None
                    and self._data["min_range"] is None):
                raise ValueError("either distances or min/max distance have "
                                 "to be set when using circuit, extra_qubits "
                                 "and total_states_superposed services")
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
        res = self._post(values)
        if res.status_code // 100 != 2:
            _logger.error(res.json())
        return res.json()["response"]

    def _post(self, values):
        res = None
        with requests.Session() as s:
            retries = Retry(total=5,
                            backoff_factor=0.1,
                            status_forcelist=[ 500, 502, 503, 504 ])
            s.mount('https://', HTTPAdapter(max_retries=3))
            res = s.post(_url, json=values, timeout=(10, 600))
            res.raise_for_status()
        return res

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

    def set_state(self, state_bin=None, num_qubits=None, state=None):
        if state_bin is None:
            if num_qubits is None or state is None:
                raise ValueError("either state_bin or num_qubits and state "
                                 "have to be specified")
            if state < 0 or state >= 2**num_qubits:
                raise ValueError("the state is out of range")
            if self._data["state_bin"] is not None:
                _logger.info("state bin info overwritten")
            self._data["n_qubits"] = num_qubits
            self._data["state"] = state
            self._data["state_bin"] = None
        else:
            if not isinstance(state_bin, str) or _bin_regex.match(state_bin) is None:
                raise ValueError("state_bin is not a string of bits")
            if num_qubits is not None or state is not None:
                print("[WARNING] num_qubits and state parameter will be "
                      "ignored since state_bin has been specified")
            if self._data["n_qubits"] is not None:
                _logger.info("state and num_qubits info overwritten")
            self._data["n_qubits"] = None
            self._data["state"] = None
            self._data["state_bin"] = state_bin

    def can_have_nan(self, value):
        if not isinstance(value, bool):
            raise ValueError("expected a boolean value")
        self._data["with_nan"] = value

    def set_range(self, distance_range):
        min_range = parse_number(distance_range[0])
        max_range = parse_number(distance_range[1])
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
