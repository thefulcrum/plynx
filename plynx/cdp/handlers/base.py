# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

from abc import ABC, abstractmethod

from plynx.cdp import get_logger

class BaseHandler(ABC):

    def __init__(self):
        self.logger = get_logger()

    @abstractmethod
    def process(self):
        raise NotImplementedError("Subclasses should implement this!")
