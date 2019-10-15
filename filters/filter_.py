# -*- coding: utf-8 -*-
"""This module provide class for transform values to comparison."""

import re
import string
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional

import mapping


class Filter(ABC):
    """Filter Interface."""

    @abstractmethod
    def set_filter(self, filter_: "Filter") -> "Filter":
        pass

    @abstractmethod
    def filtrate(self, key, value) -> Optional[str]:
        pass


class AbstractFilter(Filter):
    """Abstract Filter."""

    _filter: Filter = None  # type: ignore

    def set_filter(self, filter_: Filter) -> Filter:
        self._filter = filter_
        return filter_

    @abstractmethod
    def filtrate(self, key: str, value: str) -> str:
        if self._filter:
            return self._filter.filtrate(key, value)  # type: ignore
        else:
            return value
