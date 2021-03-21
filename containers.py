from dependency_injector import containers, providers

from core.utils.base import Observable
from core.entities import Scanner


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    observable = providers.Factory(
        Observable,
    )

    scanner = providers.Factory(
        Scanner,
        observable=observable,
    )
    scanner.add_attributes(subscanner=scanner.provider)
