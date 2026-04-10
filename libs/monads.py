from typing import TypeAlias

from pymonad.either import Either as Either_
from pymonad.either import Left as Left_
from pymonad.either import Right as Right_
from returns.result import Failure, Result, Success
from typing_extensions import deprecated

Left = deprecated('Use "Failure" instead')(Left_)

Right = deprecated('Use "Success" instead')(Right_)

Either: TypeAlias = deprecated('Use "Result" instead')(Either_)

__all__ = ['Left', 'Right', 'Either', 'Result', 'Success', 'Failure']
