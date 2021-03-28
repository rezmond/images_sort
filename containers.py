import filecmp
import os
import shutil

from dependency_injector import containers, providers

from core.entities import Mover, Scanner
from core.model import MoverModel
from core.utils.base import Observable
from core.entities.date_extractor import DateExtractor
from core.use_cases.media_presenters import VideoPresenter, ImagePresenter


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

    media_presenters = providers.List(
        providers.Singleton(VideoPresenter),
        providers.Singleton(ImagePresenter),
    )

    date_extractor = providers.Factory(
        DateExtractor,
        media_presenters=media_presenters
    )

    scanner = providers.Factory(
        Scanner,
        observable=observable,
        date_extractor=date_extractor,
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
