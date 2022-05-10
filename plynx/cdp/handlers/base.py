# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

from abc import ABC, abstractmethod


class BaseHandler(ABC):
    @abstractmethod
    def process(self):
        raise NotImplementedError("Subclasses should implement this!")
