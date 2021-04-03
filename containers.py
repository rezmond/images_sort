import filecmp

from dependency_injector import containers, providers

from core.entities import Mover, Scanner
from core.model import MoverModel
from core.utils.base import Observable
from core.entities.date_extractor import DateExtractor
from core.use_cases.media_presenters import VideoPresenter, ImagePresenter
from core.use_cases.move_map import MoveMap
from core.system_interfaces import FsManipulator, validate_folder_path
from core.controllers import ConsoleViewController
from core.views import ConsoleView
from libs import get_exif_data


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    observable = providers.Factory(
        Observable,
    )

    folder_path_validator = providers.Object(validate_folder_path)

    exif_data_getter = providers.Object(get_exif_data)

    image_presenter = providers.Factory(
        ImagePresenter,
        get_exif_data=exif_data_getter,
    )

    media_presenters = providers.List(
        providers.Singleton(VideoPresenter),
        providers.Singleton(image_presenter),
    )

    date_extractor = providers.Factory(
        DateExtractor,
        media_presenters=media_presenters
    )

    fs_manipulator = providers.Factory(FsManipulator)

    move_map = providers.Factory(MoveMap)

    scanner = providers.Factory(
        Scanner,
        observable=observable,
        date_extractor=date_extractor,
        folder_extractor=fs_manipulator,
        validate_folder_path=folder_path_validator,
        move_map=move_map,
    )

    comparator = providers.Object(filecmp.cmp)

    mover = providers.Factory(
        Mover,
        observable_factory=observable.provider,
        fs_manipulator=fs_manipulator,
        comparator=comparator,
        validate_folder_path=folder_path_validator,
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
