from src.fields.operations.finite_field import find_generator
from task_manager.tasks.abstract import AbstractTask
from common.entities import TaskType
from src.fields import FiniteField

import common.log.logging_handler as log
import common.consts as consts

from typing import List, Dict, Union

import numpy as np


class EighthSectionTask(AbstractTask):
    _TYPE = TaskType.SECTION_8

    def _run(self) -> None:

        fields_data = self._create_fields()
        log.fields([field_data["field"] for field_data in fields_data])
        self._test_finite_field_generator(fields_data)

    def _create_fields(self) -> List[FiniteField]:
        fields = []
        fields_data = self._data["fields"]
        for i, field in enumerate(fields_data):
            try:
                # creating a finite field with reducible fx raises an error
                fields.append(
                    {
                        "field": FiniteField(p=field["p"], fx=field["fx"]),
                        "expected_generator": np.array(field["expected_generator"])
                    }
                )

            except Exception as e:
                err_msg = f"Error:\n{e}\n" \
                    + f"(P={field['p']} | f(x)={field['fx']})"

                if i != len(fields_data) - 1:
                    err_msg += "\n"
                log.error(err_msg)

        return fields

    def _test_finite_field_generator(
        self,
        fields_data: List[Dict[str, Union[FiniteField, np.ndarray]]]
    ) -> None:

        for i, field_data in enumerate(fields_data, 1):
            field = field_data["field"]
            generator = find_generator(field)

            log.info(
                f"Generator for Field {i} " +
                f"(p = {field.p} | fx = {field.fx}): {generator.a}\n" + 
                f"Expected generator: {field_data['expected_generator']}"
            )

