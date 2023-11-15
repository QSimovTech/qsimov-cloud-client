import logging
import qsimov_cloud_client as qcc
import random as rnd
import string
import sympy as sp
import json
import jsonschema
import os

from jsonschema import validate
from unittest import TestCase, main, mock
from requests.exceptions import HTTPError


_valid_chars = string.ascii_lowercase + string.digits
_logger = logging.getLogger("QsimovCloudClient")

schemas_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'schemas')

request_schema = None
with open(os.path.join(schemas_path, "request_schema.json")) as f:
    request_schema = json.load(f)
responses = {}
with open(os.path.join(schemas_path, "response_distances_service.json")) as f:
    responses["distances_range_service"] = json.load(f)
with open(os.path.join(schemas_path, "response_extra_service.json")) as f:
    responses["extra_qubits_service"] = json.load(f)
with open(os.path.join(schemas_path, "response_total_service.json")) as f:
    responses["total_states_superposed_service"] = json.load(f)
with open(os.path.join(schemas_path, "response_circuit_service.json")) as f:
    responses["circuit_service"] = json.load(f)


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def raise_for_status(self):
            if self.status_code // 100 != 2:
                raise HTTPError(self.status_code)

        def json(self):
            return self.json_data

    if args[0] == 'https://qcaas.qsimov.com/superpositions':
        data = kwargs["json"]
        validate(instance=data, schema=request_schema)
        res = responses[data["service"]]
        res["params"] = data
        return MockResponse(res, 200)

    return MockResponse(None, 404)


class TestCloudMethods(TestCase):
    def setUp(self):
        self.token = ''.join(rnd.choices(_valid_chars, k=16))
        self.cli = qcc.QsimovCloudClient(self.token)

    def test_constructor(self):
        self.assertEqual(self.cli._data["token"], self.token)
        self.assertIsNone(self.cli._data["metric"])
        self.assertIsNone(self.cli._data["n_qubits"])
        self.assertIsNone(self.cli._data["state"])
        self.assertIsNone(self.cli._data["state_bin"])
        self.assertIsNone(self.cli._data["distances"])
        self.assertIsNone(self.cli._data["min_range"])
        self.assertIsNone(self.cli._data["max_range"])
        self.assertIsNone(self.cli._data["with_nan"])
        self.assertEqual(self.cli._data["ancilla_mode"], "clean")
        self.assertEqual(self.cli._data["qasm_version"], "2.0")
        with self.assertRaises(ValueError):
            qcc.QsimovCloudClient("")
        with self.assertRaises(ValueError):
            qcc.QsimovCloudClient(None)
        with self.assertRaises(TypeError):
            qcc.QsimovCloudClient()

    def test_set_metric(self):
        metric = ''.join(rnd.choices(_valid_chars, k=8))
        self.cli.set_metric(metric)
        self.assertEqual(self.cli._data["metric"], metric)
        with self.assertRaises(ValueError):
            self.cli.set_metric("")
        with self.assertRaises(ValueError):
            self.cli.set_metric(3)
        with self.assertRaises(ValueError):
            self.cli.set_metric(None)
        with self.assertRaises(TypeError):
            self.cli.set_metric()

    def test_set_ancilla_mode(self):
        for amode in qcc._ancilla_modes:
            self.cli.set_ancilla_mode(amode)
            self.assertEqual(self.cli._data["ancilla_mode"], amode)
        anc = ''.join(rnd.choices(_valid_chars, k=8))
        with self.assertRaises(ValueError):
            self.cli.set_ancilla_mode(anc)
        with self.assertRaises(ValueError):
            self.cli.set_ancilla_mode(None)
        with self.assertRaises(TypeError):
            self.cli.set_ancilla_mode()

    def test_set_qasm_version(self):
        for ver in ["2.0", "3.0"]:
            self.cli.set_qasm_version(ver)
            self.assertEqual(self.cli._data["qasm_version"], ver)
        ver = ''.join(rnd.choices(_valid_chars, k=3))
        with self.assertRaises(ValueError):
            self.cli.set_qasm_version(ver)
        with self.assertRaises(ValueError):
            self.cli.set_qasm_version(None)
        with self.assertRaises(TypeError):
            self.cli.set_qasm_version()

    def test_set_state(self):
        isFirst = True
        for i in range(1, 9):
            state_bin = ''.join(rnd.choices(['0', '1'], k=i))
            if isFirst:
                with self.assertNoLogs(_logger, level=logging.INFO) as cm:
                    self.cli.set_state(state_bin=state_bin)
                isFirst = False
            else:
                with self.assertLogs(_logger, level=logging.INFO) as cm:
                    self.cli.set_state(state_bin=state_bin)
                    self.assertEqual(cm.output, ['INFO:QsimovCloudClient:state and num_qubits info overwritten'])
            self.assertEqual(self.cli._data["state_bin"], state_bin)
            self.assertIsNone(self.cli._data["state"])
            self.assertIsNone(self.cli._data["n_qubits"])
            sta = 2**i - 1
            with self.assertLogs(_logger, level=logging.INFO) as cm:
                self.cli.set_state(num_qubits=i, state=sta)
                self.assertEqual(cm.output, ['INFO:QsimovCloudClient:state bin info overwritten'])
            self.assertIsNone(self.cli._data["state_bin"])
            self.assertEqual(self.cli._data["state"], sta)
            self.assertEqual(self.cli._data["n_qubits"], i)
            with self.assertRaises(ValueError):
                self.cli.set_state(num_qubits=i, state=-1)
            with self.assertRaises(ValueError):
                self.cli.set_state(num_qubits=i, state=sta+1)
        with self.assertRaises(ValueError):
            self.cli.set_state(state_bin=None, num_qubits=None, state=None)
        with self.assertRaises(ValueError):
            self.cli.set_state()

    def test_can_have_nan(self):
        self.cli.can_have_nan(True)
        self.assertEqual(self.cli._data["with_nan"], True)
        self.cli.can_have_nan(False)
        self.assertEqual(self.cli._data["with_nan"], False)
        with self.assertRaises(ValueError):
            self.cli.can_have_nan(2)
        with self.assertRaises(ValueError):
            self.cli.can_have_nan(None)
        with self.assertRaises(TypeError):
            self.cli.can_have_nan()

    def test_distances(self):
        a = rnd.random() * 10
        b = rnd.random() * 10
        if a > b:
            a, b = b, a
        a_num = rnd.randint(1, 10)
        a_den = rnd.randint(1, 10)
        a_frac = str(sp.Rational(f"{a_num}/{a_den}"))
        b_num = rnd.randint(1, 10)
        b_den = rnd.randint(1, 10)
        b_frac = str(sp.Rational(f"{b_num}/{b_den}"))
        if a_num / a_den > b_num / b_den:
            a_frac, b_frac = b_frac, a_frac
        d = [rnd.random() * 10 if i % 3 != 0 else str(sp.Rational(f"{rnd.randint(1, 10)}/{rnd.randint(1, 10)}")) for i in range(10)]
        d += [float("nan"), "0/0"]
        with self.assertNoLogs(level='INFO') as cm:
            self.cli.set_range((a, b))
        self.assertEqual(float(self.cli._data["min_range"]), a)
        self.assertEqual(float(self.cli._data["max_range"]), b)
        self.assertIsNone(self.cli._data["distances"])
        with self.assertRaises(ValueError):
            self.cli.set_range((b, a))
        self.assertEqual(float(self.cli._data["min_range"]), a)
        self.assertEqual(float(self.cli._data["max_range"]), b)
        self.assertIsNone(self.cli._data["distances"])
        with self.assertLogs(_logger, level=logging.INFO) as cm:
            self.cli.set_distances(d)
            self.assertEqual(cm.output, ['INFO:QsimovCloudClient:range info overwritten'])
        self.assertIsNone(self.cli._data["min_range"])
        self.assertIsNone(self.cli._data["max_range"])
        self.assertEqual([float(self.cli._data["distances"][i]) if i % 3 != 0
                          else str(self.cli._data["distances"][i])
                          for i in range(10)] + list(self.cli._data["distances"][10:]), d[:10] + [sp.nan, sp.nan])
        with self.assertRaises(ValueError):
            self.cli.set_distances("123")
        self.assertIsNone(self.cli._data["min_range"])
        self.assertIsNone(self.cli._data["max_range"])
        self.assertEqual([float(self.cli._data["distances"][i]) if i % 3 != 0
                          else str(self.cli._data["distances"][i])
                          for i in range(10)] + list(self.cli._data["distances"][10:]), d[:10] + [sp.nan, sp.nan])
        with self.assertLogs(_logger, level=logging.INFO) as cm:
            self.cli.set_range((a_frac, b_frac))
            self.assertEqual(cm.output, ['INFO:QsimovCloudClient:distances info overwritten'])
        self.assertEqual(str(self.cli._data["min_range"]), a_frac)
        self.assertEqual(str(self.cli._data["max_range"]), b_frac)
        self.assertIsNone(self.cli._data["distances"])
        with self.assertRaises(ValueError):
            self.cli.set_range((b_frac, a_frac))
        with self.assertRaises(TypeError):
            self.cli.set_range(None, None)
        with self.assertRaises(TypeError):
            self.cli.set_range()
        with self.assertRaises(ValueError):
            self.cli.set_distances(None)
        with self.assertRaises(TypeError):
            self.cli.set_distances()

    @mock.patch("qsimov_cloud_client.requests.Session.post", side_effect=mocked_requests_post)
    def test_requests(self, mock_post):
        self.cli.set_metric("ample")
        self.cli.set_state(state_bin="0110")
        r = self.cli.calculate_distance_range()
        self.cli.set_state(state=4, num_qubits=3)
        r = self.cli.calculate_distance_range()
        self.cli.set_range(r)
        self.cli.can_have_nan(False)
        ex = self.cli.calculate_extra_qubits()
        ns = self.cli.calculate_num_superposed()
        sc = self.cli.generate_circuit()
        self.cli.can_have_nan(True)
        ns = self.cli.calculate_num_superposed()
        ex = self.cli.calculate_extra_qubits()
        sc2 = self.cli.generate_circuit()

if __name__ == '__main__':
    main()
