import filecmp

from dependency_injector import containers, providers

from core.entities import Mover, Scanner
from core.model import MoverModel
from core.utils.base import Observable
from core.entities.date_extractor import DateExtractor
from core.use_cases.media_presenters import VideoPresenter, ImagePresenter
from core.system_interfaces import FsManipulator
from core.controllers import ConsoleViewController
from core.views import ConsoleView


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

    fs_manipulator = providers.Factory(FsManipulator)

    scanner = providers.Factory(
        Scanner,
        observable=observable,
        date_extractor=date_extractor,
        folder_extractor=fs_manipulator,
    )

    comparator = providers.Singleton(filecmp.cmp)

    mover = providers.Factory(
        Mover,
        observable_factory=observable.provider,
        fs_manipulator=fs_manipulator,
        comparator=comparator,
    )

    model = providers.Singleton(
        MoverModel,
        mover=mover,
        scanner=scanner,
    )

    view_class = providers.Object(
        ConsoleView,
    )

    controller = providers.Factory(
        ConsoleViewController,
        model=model,
        view_class=view_class,
    )
