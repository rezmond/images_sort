import filecmp

from dependency_injector import containers, providers

from core.entities import Mover, Scanner
from core.model import MoverModel
from core.utils.base import Observable
from core.entities.date_extractor import DateExtractor
from core.use_cases.media_presenters import VideoPresenter, ImagePresenter
from core.use_cases.move_map import MoveMap
from core.system_interfaces import FsManipulator, FolderPathValidator
from core.controllers import ConsoleViewController
from core.views import ConsoleView
from libs import get_exif_data


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    observable = providers.Factory(
        Observable,
    )

    fs_manipulator = providers.Factory(FsManipulator)

    folder_path_validator = providers.Factory(
        FolderPathValidator,
        fs_manipulator=fs_manipulator,
    )

    exif_data_getter = providers.Object(get_exif_data)

    image_presenter = providers.Factory(
        ImagePresenter,
        get_exif_data=exif_data_getter,
    )
    video_presenter = providers.Factory(
        VideoPresenter,
    )

    media_presenters = providers.List(
        providers.Singleton(video_presenter),
        providers.Singleton(image_presenter),
    )

    date_extractor = providers.Factory(
        DateExtractor,
        media_presenters=media_presenters
    )

    move_map = providers.Factory(MoveMap)

    scanner = providers.Factory(
        Scanner,
        date_extractor=date_extractor,
        folder_extractor=fs_manipulator,
        folder_path_validator=folder_path_validator,
        move_map=move_map,
    )

    comparator = providers.Object(filecmp.cmp)

    mover = providers.Factory(
        Mover,
        observable_factory=observable.provider,
        fs_manipulator=fs_manipulator,
        comparator=comparator,
        folder_path_validator=folder_path_validator,
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
