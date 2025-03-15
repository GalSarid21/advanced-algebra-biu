from task_manager.tasks.abstract import AbstractTask
from src.field_elements import FiniteFieldElement
from common.log import LoggingHandler


class FourthSectionTask(AbstractTask):

    def __init__(self) -> None:
        super().__init__("./data/fourth_section.yaml")

    def _run(self) -> None:
        elements = self._create_field_elements(FiniteFieldElement)
        LoggingHandler.log_elements(
            elements=elements,
            # id we're printing only 1 element - 
            # there is no need for empty line
            end_with_empty_line=False,
            add_element_image=True
        )
