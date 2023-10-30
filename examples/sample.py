# -*- coding: utf-8 -*-
import qsimov_cloud_client as qcc


cc = qcc.QsimovCloudClient("aaa")
cc.set_state(n_qubits=8, state=27)
cc.set_state(bin="00011011")
#cc.set_state(n_qubits=8, state=27)
cc.set_metric("hamming")

extra = cc.calculate_extra_qubits()
print(extra)

range = cc.calculate_distance_range()
print(range)

cc.can_have_nan(False)
cc.set_range(("1/3", 2.15))
cc.set_distances(["1/3", 2.15, "inf", "nan", 1])
#cc.set_range(range)

num = cc.calculate_num_superposed()
print(num)

sc = cc.generate_circuit()
print("Metric:", sc.get_metric())
print("State:", sc.get_state())  # This returns a tuple (n_qubits, state_value)
print("State Bin:", sc.get_state_bin())
print("Extra Qubits:", sc.get_extra_qubits())
print("Range:", sc.get_range())
print("Distances:", sc.get_distances())
print("0/0 allowed:", sc.is_nan_allowed())
print("# states superposed:", sc.get_num_superposed())
print("QASM:", sc.get_qasm_code())
