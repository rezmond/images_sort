import filecmp

from dependency_injector import containers, providers

from src.core import Mover, Scanner
from src.utils.base import Observable
from src.core.date_extractor import DateExtractor
from src.use_cases.media_presenters import VideoPresenter, ImagePresenter
from src.use_cases.move_map import SeasonsMoveMap
from src.system_interfaces import FsManipulator
from src.mvc.controllers import ConsoleViewController
from src.mvc.model import MoverModel
from src.mvc.views import ConsoleView
from libs import get_exif_data


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    observable = providers.Factory(
        Observable,
    )

    fs_manipulator = providers.Factory(FsManipulator)

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

    move_map = providers.Factory(SeasonsMoveMap)

    scanner = providers.Factory(
        Scanner,
        date_extractor=date_extractor,
        folder_extractor=fs_manipulator,
        fs_manipulator=fs_manipulator,
        move_map=move_map,
    )

    comparator = providers.Object(filecmp.cmp)

    mover = providers.Factory(
        Mover,
        fs_manipulator=fs_manipulator,
        comparator=comparator,
    )

    model = providers.Singleton(
        MoverModel,
        mover=mover,
        scanner=scanner,
    )

    controller = providers.Singleton(
        ConsoleViewController,
        input_boundary=model,
    )

    view = providers.Singleton(
        ConsoleView,
        controller=controller,
    )
