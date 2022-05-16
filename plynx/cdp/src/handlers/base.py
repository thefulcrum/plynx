# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

import logging
from abc import ABC, abstractmethod


class BaseHandler(ABC):
    """Base event handler."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def process(self):
        raise NotImplementedError("Subclasses should implement this!")
