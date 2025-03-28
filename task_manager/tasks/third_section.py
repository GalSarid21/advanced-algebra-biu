from task_manager.tasks.abstract import AbstractTask
from src.field_elements import FiniteFieldElement
from common.entities import PrintMode, TaskType
from src.fields import FiniteField

import common.log.logging_handler as log

from typing import List


class ThirdSectionTask(AbstractTask):
    _TYPE = TaskType.SECTION_3

    def _run(self) -> None:
        log.info("*** Testing FiniteFields Creation:")
        fields = self._create_fields()
        log.fields(fields)

        log.info(
            "*** Testing 'field' property of FiniteFieldElement:"
        )
        self._test_field_elements_creation()

    def _create_fields(self) -> List[FiniteField]:
        fields = []
        fields_data = self._data["fields"]
        for i, field in enumerate(fields_data):
            try:
                # creating a finite field with reducible fx raises an error
                fields.append(
                    FiniteField(p=field["p"], fx=field["fx"])
                )

            except Exception as e:
                err_msg = f"Error:\n{e}\n" \
                    + f"(P={field['p']} | f(x)={field['fx']})"

                if i != len(fields_data) - 1:
                    err_msg += "\n"
                log.error(err_msg)

        return fields

    def _test_field_elements_creation(self) -> None:
        elements = self._data["elements"]
        for i, element in enumerate(elements):
            try:
                element_obj = FiniteFieldElement(
                    a=element["a"],
                    p=element["p"],
                    fx=element["fx"]
                )

                log_msg = f"{element_obj.pretty_print()} | " \
                    + f"{element_obj.pretty_print(PrintMode.POLYNOMIAL)}\n" \
                    + f"(P={element_obj.p} | f(x)={element_obj.fx} | " \
                    + f"n={element_obj.n} | a_oring={element_obj.a_orig})\n" \
                    + "Element is linked to 'l' by field property:\n" \
                    + f"{element_obj.field}"

                if i != len(elements) - 1:
                    log_msg += "\n"
                log.info(log_msg)

            except Exception as e:
                err_msg = f"Error:\n{e}\n" \
                    + f"(a={element['a']} | P={element['p']} | " \
                    + f"f(x)={element['fx']})"

                if i != len(elements) - 1:
                    err_msg += "\n"
                log.error(err_msg)
