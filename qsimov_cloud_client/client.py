# -*- coding: utf-8 -*-
import json
import logging
import re
import requests
import sympy as sp

from collections.abc import Iterable
from requests.adapters import HTTPAdapter, Retry

from .utils import parse_number


_bin_regex = re.compile(r"^[01]+$")
_services = ["extra_qubits_service",
             "distances_range_service",
             "circuit_service",
             "total_states_superposed_service"]
_ancilla_modes = ['clean', 'noancilla', 'garbage', 'borrowed', 'burnable']
_url = "https://qcaas.qsimov.com/superpositions"
_logger = logging.getLogger("QsimovCloudClient")


class QsimovCloudClient(object):
    """QsimovCloudClient is a Python client for interacting with the Qsimov cloud services."""

    def __init__(self, token):
        """
        Initialize the QsimovCloudClient with a valid access token.

        Args:
            token (str): The access token for authenticating with the Qsimov cloud services.

        Raises:
            ValueError: If the token is not a non-empty string.
        """
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
        """
        Send a request to the Qsimov cloud service.

        Args:
            service (str): The name of the Qsimov cloud service to be invoked.

        Returns:
            dict: The response from the Qsimov cloud service.

        Raises:
            ValueError: If required parameters are not set or an unknown service is specified.
        """
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
        if values["state_bin"] is None:
            del values["state_bin"]
        else:
            del values["state"]
            del values["n_qubits"]
        values["service"] = service
        res = self._post(values)
        return res.json()["response"]

    def _post(self, values):
        """
        Perform a POST request to the Qsimov cloud service.

        Args:
            values (dict): The data to be sent in the request.

        Returns:
            requests.Response: The response from the Qsimov cloud service.

        Raises:
            requests.exceptions.HTTPError: If the request was unsuccessful.
        """
        res = None
        with requests.Session() as s:
            retries = Retry(total=5,
                            backoff_factor=0.1,
                            status_forcelist=[ 500, 502, 503, 504 ])
            s.mount('https://', HTTPAdapter(max_retries=3))
            res = s.post(_url, json=values, timeout=(10, 900))
            if res.status_code // 100 != 2:
                _logger.error(res.json())
            res.raise_for_status()
        return res

    def set_metric(self, metric):
        """
        Set the metric for the quantum superposition.

        Args:
            metric (str): The metric to be used for the superposition. See full documentation for available metrics.

        Raises:
            ValueError: If the metric is not a non-empty string.
        """
        if not isinstance(metric, str) or metric == "":
            raise ValueError("metric has to be a non-empty string")
        self._data["metric"] = metric

    def set_ancilla_mode(self, ancilla_mode):
        """Set the mode for ancilla qubits.

        Args:
            ancilla_mode (str): The mode for ancilla qubits.
                It should be one of the following:

                - 'clean': Clean ancilla qubits mode.

                - 'noancilla': No ancilla qubits mode. This mode may result in exponential growth in the number of gates within the quantum circuit. This approach is not scalable and is limited to circuits with up to 10 qubits. Consider choosing an alternative ancilla mode for larger-scale quantum computations.

        Raises:
            ValueError: If the ancilla_mode is not valid.
        """
        if ancilla_mode not in _ancilla_modes:
            raise ValueError("invalid ancilla mode")
        self._data["ancilla_mode"] = ancilla_mode

    def set_qasm_version(self, qasm_version):
        """Set the version of the QASM (Quantum Assembly) language.

        Args:
            qasm_version (str): The QASM version. It should be one of the following:

                - '2.0': QASM version 2.0.

        Raises:
            ValueError: If the qasm_version is not one of the valid options.
        """
        if qasm_version != "2.0" and qasm_version != "3.0":
            raise ValueError("invalid QASM version")
        self._data["qasm_version"] = qasm_version

    def set_state(self, state_bin=None, num_qubits=None, state=None):
        """Set the reference quantum state for the computation.

        Args:
            state_bin (str): Binary representation of the quantum state.
            num_qubits (int): Number of qubits (if state_bin is not provided).
            state (int): Integer representation of the reference quantum state (if state_bin is not provided).

        Raises:
            ValueError: If the parameters are not valid or out of range.
        """
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
        """Specify whether NaN (0/0) values are inclided in the superposition.

        Args:
            value (bool): True if NaN is included, False otherwise.

        Raises:
            ValueError: If the value is not a boolean.
        """
        if not isinstance(value, bool):
            raise ValueError("expected a boolean value")
        self._data["with_nan"] = value

    def set_range(self, distance_range):
        """Set the range of distances/similarities for the superposition.

        Args:
            distance_range (tuple): A tuple containing the minimum and maximum distances.
                The distances should be provided as strings. If they include decimals, use fraction format (e.g., '3/2' for 1.5).

        Raises:
            ValueError: If the range is not valid.
        """
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
        """Set the specific distances for the superposition.

        Args:
            distances (iterable): A list of distances.
                The distances should be provided as strings. If they include decimals, use fraction format (e.g., '3/2' for 1.5).

        Raises:
            ValueError: If the distances are not a valid list.
        """
        if not isinstance(distances, Iterable) or isinstance(distances, str):
            raise ValueError("expected a list")
        if self._data["min_range"] is not None:
            _logger.info("range info overwritten")
        self._data["distances"] = tuple([parse_number(i) for i in distances])
        self._data["min_range"] = None
        self._data["max_range"] = None

    def calculate_extra_qubits(self):
        """Calculate the extra qubits needed for the superposition.

        Returns:
            int: The number of extra qubits needed.
        """
        data = self._send_request("extra_qubits_service")
        return data["extra_qubits"]

    def calculate_distance_range(self):
        """Calculate the range of distances for the computation.

        Returns:
            tuple: A tuple containing the minimum and maximum distances.
        """
        data = self._send_request("distances_range_service")
        return (data["distances_range_min"], data["distances_range_max"])

    def generate_circuit(self):
        """Generate the quantum circuit based on the specified parameters.

        Returns:
            SuperpositionCircuit: An object representing the generated quantum circuit.
        """
        res = self._send_request("circuit_service")
        if res["qasm_circuit"].startswith('https'):
            try:
                circuit = requests.get(url).text
            except Exception:
                print("Unable to generate the circuit")
                _logger.error(res.json())
                return None
            res["qasm_circuit"] = circuit
        return SuperpositionCircuit(self._data, res)

    def calculate_num_superposed(self):
        """Calculate the total number of superposed states.

        Returns:
            int: The total number of superposed states.
        """
        data = self._send_request("total_states_superposed_service")
        return data["total_states_superposed"]


class SuperpositionCircuit(object):
    """Represents a superposition circuit generated by the Qsimov cloud service.

    This class provides access to various properties and information about the
    generated superposition circuit."""
    def __init__(self, data, res):
        """
        Initialize the SuperpositionCircuit with the data received.

        Args:
            data (dict): A dictionary containing input data for the circuit generation.
            res (dict): A dictionary containing the response data from the Qsimov service.

        """
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
        """Get the metric used for the superposition.

        Returns:
            str: The metric used.
        """
        return self._metric

    def get_state(self):
        """Get the number of qubits and the reference quantum state.

        Returns:
            tuple: A tuple containing the number of qubits and the reference quantum state.
        """
        return (self._n_qubits, self._state)

    def get_state_bin(self):
        """Get the binary representation of the reference quantum state.

        Returns:
            str: The binary representation.
        """
        return self._bin

    def get_range(self):
        """Get the range of distances used for the superposition.

        Returns:
            tuple or None: A tuple containing the minimum and maximum distances,
            or None if no range is specified.
        """
        if self._min_range is None:
            return None
        return (self._min_range, self._max_range)

    def get_distances(self):
        """Get the distances used for the superposition.

        Returns:
            tuple: The distances used.
        """
        return self._distances

    def is_nan_allowed(self):
        """Check if NaN values are included in the superposition.

        Returns:
            bool: True if NaN values are included, False otherwise.
        """
        return self._with_nan

    def get_extra_qubits(self):
        """Get the number of extra qubits required for the circuit.

        Returns:
            int: The number of extra qubits.
        """
        return self._extra_qubits

    def get_num_superposed(self):
        """Get the total number of states superposed.

        Returns:
            int: The total number of states superposed.
        """
        return self._total_states_superposed

    def get_qasm_code(self):
        """Get the QASM code representing the generated superposition circuit.

        Returns:
            str: The QASM code.
        """
        return self._qasm

    def get_qasm_version(self):
        """Get the version of QASM used for the circuit generation.

        Returns:
            str: The QASM version.
        """
        return self._qasm_version

    def get_ancilla_mode(self):
        """Get the mode for ancilla qubits in the circuit.

        Returns:
            str: The ancilla mode.
        """
        return self._ancilla_mode
