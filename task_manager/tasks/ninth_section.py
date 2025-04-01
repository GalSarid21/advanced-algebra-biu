from src.field_elements.operations.finite_field_element import(
    discrete_log_bsgs
)
from task_manager.tasks.abstract import AbstractTask
from src.field_elements import FiniteFieldElement
from common.entities import TaskType
from src.fields import FiniteField

import common.log.logging_handler as log

from typing import List, Dict, Union

import numpy as np


class NinthSectionTask(AbstractTask):
    _TYPE = TaskType.SECTION_9

    def _run(self) -> None:

        fields, h_vals = self._create_fields_and_h_vals()
        log.fields(fields)
        self._test_discrete_log(fields, h_vals)

    def _create_fields_and_h_vals(self) -> List[FiniteField]:
        fields = []
        fields_data = self._data["fields"]
        for i, field in enumerate(fields_data):
            try:
                # creating a finite field with reducible fx raises an error
                fields.append(FiniteField(p=field["p"], fx=field["fx"]))

            except Exception as e:
                err_msg = f"{e}\n" \
                    + f"(P={field['p']} | f(x)={field['fx']})"

                if i != len(fields_data) - 1:
                    err_msg += "\n"
                log.error(err_msg)

        return fields, self._data["h_vals"]

    def _test_discrete_log(
        self,
        fields: List[FiniteField],
        h_vals: Dict[str, Union[int, List[int]]]
    ) -> None:

        for i, field in enumerate(fields, 1):
            key = f"e{i}"
            for j in range(len(h_vals[key])):
                h = np.array(h_vals[key][j]["h"])
                generator_arr = np.array(h_vals[key][j]["gen"])
                generator = FiniteFieldElement(
                    a=generator_arr, p=field.p, fx=field.fx
                )
                
                calculated_log = discrete_log_bsgs(h, generator)

                msg = f"Field: {i} | h: {h} | generator: {generator.a} | discrete log: {calculated_log}\n" \
                    + f"Expected log: {h_vals[key][j]['expected_log']}"
                log.info(msg)
