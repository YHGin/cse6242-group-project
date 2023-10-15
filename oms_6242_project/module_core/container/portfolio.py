from typing import List


class Portfolio():

    def __int__(self):
        raise NotImplemented

    @property
    def position(self) -> List[Stock]:
        raise NotImplemented
