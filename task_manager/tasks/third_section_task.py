from task_manager.tasks.abstract_task import AbstractTask
from src.field_elements import FiniteFieldElement
from src.fields import FiniteField
from common.log import LoggingHandler

from typing import List


class ThirdSectionTask(AbstractTask):
    
    def __init__(self) -> None:
        super().__init__("./data/third_section.yaml")

    def _run(self) -> None:
        LoggingHandler.log_info("*** Testing FiniteFields Creation:")
        fields = self._create_fields()
        LoggingHandler.log_fields(fields)

        LoggingHandler.log_info(
            "*** Testing 'field' property of FiniteFieldElement:"
        )
        self._test_field_elements_creation()

    def _create_fields(self) -> List[FiniteField]:
        fields = []
        for field in self._data["fields"]:
            try:
                # creating a finite field with reducible fx raises an error
                fields.append(
                    FiniteField(p=field["p"], fx=field["fx"])
                )
            except Exception as e:
                LoggingHandler.log_error(str(e))
        return fields

    def _test_field_elements_creation(self) -> None:
        for element in self._data["elements"]:
            try:
                element_obj = FiniteFieldElement(
                    a=element["a"],
                    p=element["p"],
                    fx=element["fx"]
                )
                # creating a finite field element with reducible fx
                # raises an error
                LoggingHandler.log_error(
                    f"FiniteFieldElement: {element_obj.a}\n"
                    f"Element is linked to 'l' by field property:\n" +
                    f"{element_obj.field}"
                )
            except Exception as e:
                LoggingHandler.log_error(str(e))
