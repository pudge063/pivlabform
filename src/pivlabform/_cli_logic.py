import click
import typing_extensions
from .pivlabform import Pivlabform
from . import _helpers
from ._helpers import LOGGER


def create_click_command():
    @click.command()
    @click.option(
        "--list",
        "-l",
        default="configurations/custom_config.yaml",
        help="list with configuration",
    )
    @click.option(
        "--ci",
        is_flag=True,
        help="on ci run",
    )
    @click.option(
        "--manual",
        "-m",
        is_flag=True,
        help="manual run for single group or project path",
    )
    @click.option(
        "--project",
        "type",
        flag_value="project",
        help="path of project or group in gitlab (example: `sandbox/test/project-1`)",
    )
    @click.option(
        "--group",
        "type",
        flag_value="group",
        help="",
    )
    @click.option(
        "--path",
        help="path of project or group in gitlab (example: `sandbox/test/project-1`)",
    )
    @click.option(
        "--id",
        help="ID of project or group in gitlab (example: `1001`)",
    )
    @click.option(
        "--config-file",
        "-c",
        default="configurations/manual.yaml",
        help="config file path",
    )
    @click.option(
        "--recursive",
        "-r",
        is_flag=True,
        help="apply configuration recursive for subgroups and projects in subgroups",
    )
    @click.option(
        "--gitlab-host",
        default=_helpers.get_gitlab_host(),
        help="gitlab host url (example: `https://pivlab.space`)",
    )
    def process(
        list: str,
        manual: typing_extensions.Optional[bool],
        type: typing_extensions.Optional[str],
        path: typing_extensions.Optional[str],
        id: typing_extensions.Optional[str],
        config_file: str,
        recursive: bool,
        gitlab_host: str,
        ci: bool = False,
    ):
        if not ci:
            try:
                from dotenv import load_dotenv

                load_dotenv()
                print("local dotenv loaded successfully")
            except ImportError:
                print("python-dotenv not installed, skipping .env loading")
                pass

        pl = Pivlabform(gitlab_host)

        if manual:
            LOGGER.info("process manual run")
            pl.process_manual_configuration(
                path_type=type,
                path=path,
                id=id,
                config_file=config_file,
                recursive=recursive,
            )

    return process
