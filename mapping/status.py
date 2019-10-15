# -*- coding: utf-8 -*-

from typing import NamedTuple


class Status(NamedTuple):
    onyma_id: int
    crm_id: int
    description: str


active = Status(0, 930660000, "Active")
closed = Status(4, 930660004, "Closed")
inactive = Status(1, 930660001, "Inactive")
paused_by_operator = Status(3, 930660003, "Paused by operator")
paused_by_system = Status(2, 930660002, "Paused by system")
