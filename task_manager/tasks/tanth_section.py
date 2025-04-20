from src.field_elements.operations.finite_field_element import (
    discrete_log_bsgs, discrete_log_lifting
)
from task_manager.tasks.abstract import AbstractTask
from src.field_elements import FiniteFieldElement
from common.entities import TaskType
import common.log.logging_handler as log

from typing import Optional, List
import time


class TenthSectionTask(AbstractTask):
    _TYPE = TaskType.SECTION_10

    def _run(self) -> None:
        elements = self._data["elements"]
        for i, element in enumerate(elements):
            self._compare_bsgs_lift_discrete_log(
                p=element["p"],
                s=element["s"],
                x_target=element["x_target"],
                g_int=element["g_int"],
                fx=element["fx"],
                description=element["description"]
            )
            if i != len(elements) - 1:
                log.info("")

    def _compare_bsgs_lift_discrete_log(
        self,
        p: int,
        s: int,
        x_target: int,
        g_int: int,
        fx: List[int],
        description: Optional[str] = None,
        log_inner_steps: Optional[bool] = True
    ) -> None:

        start_log_msg = "Test case data: " \
            + f"p={p}, s={s}, x_target={x_target}, g_int={g_int}, fx={fx}"
        if description is not None:
            start_log_msg += f"\nScenario: {description}"
        log.info(start_log_msg)
        modulus = p ** s

        # Compute h = g^x_target mod p^s
        h_lift = pow(g_int, x_target, modulus)
        if log_inner_steps is True:
            log.info(
                f"Working in U_(p^s) with p = {p}, s = {s} (modulus = {modulus}).\n" +
                f"Chosen base g = {g_int}, secret exponent x = {x_target}, " +
                f"computed h = {h_lift}"
            )

        # Lifting Attack in U_{p^s}
        start = time.perf_counter()
        x_lift = discrete_log_lifting(g_int, h_lift, p, s, log_inner_steps=False)
        time_lift = time.perf_counter() - start
        if x_lift is not None:
            log.info(f"[Lifting] Found x = {x_lift} in {time_lift:.10f} seconds.")
        else:
            log.error(f"[Lifting] FAILED to calculate discrete log.")

        # BSGS in GF(p)
        h_field_val = h_lift % p
        # Create field elements for generator and h.
        generator_field = FiniteFieldElement([g_int % p], p, fx)
        h_field = FiniteFieldElement([h_field_val], p, fx)
        start = time.perf_counter()
        x_bsgs = discrete_log_bsgs(h_field.a, generator_field)
        time_bsgs = time.perf_counter() - start
        if x_bsgs is not None:
            log.info(f"[BSGS] Found x = {x_bsgs} in {time_bsgs:.10f} seconds.")
        else:
            log.error(f"[BSGS] FAILED to calculate discrete log.")
