import filecmp
import os
import shutil

from dependency_injector import containers, providers

from core.entities import Mover, Scanner
from core.model import MoverModel
from core.utils.base import Observable
from core.applied.identifiers import ImagesIdentifier

print("ImagesIdentifier", ImagesIdentifier)


class FsManipulator:
    move = shutil.move
    copy = shutil.copy2
    delete = os.remove
    makedirs = os.makedirs


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    observable = providers.Factory(
        Observable,
    )

    identifier = providers.Factory(
        ImagesIdentifier,
    )

    scanner = providers.Factory(
        Scanner,
        observable=observable,
        identifier=identifier,
    )
    scanner.add_attributes(subscanner=scanner.provider)

    fs_manipulator = providers.Factory(FsManipulator)

    comparator = providers.Singleton(filecmp.cmp)

    mover = providers.Factory(
        Mover,
        observable_factory=observable.provider,
        fs_manipulator=fs_manipulator,
        comparator=comparator,
    )

    model = providers.Factory(
        MoverModel,
        mover=mover,
        scanner=scanner,
    )
