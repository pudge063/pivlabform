import click
import sys
import typing_extensions

from .utils import _consts

from .utils import _helpers
from .utils._helpers import LOGGER
from .pivlabform import Pivlabform


def cli():
    @click.command()
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
        default=_consts.Files.manual_default_config.value,
        help="config file path",
    )
    @click.option(
        "--recursive",
        "-r",
        is_flag=True,
        help="apply configuration recursive for subgroups and projects in subgroups",
    )
    @click.option(
        "--validate",
        "-v",
        is_flag=True,
        help="only validate configurations",
    )
    @click.option(
        "--gitlab-host",
        default=_helpers.get_gitlab_host(),
        help="gitlab host url (example: `https://pivlab.space`)",
    )
    def process(
        manual: typing_extensions.Optional[bool],
        type: typing_extensions.Optional[str],
        path: typing_extensions.Optional[str],
        id: typing_extensions.Optional[int],
        config_file: str,
        recursive: bool,
        gitlab_host: str,
        validate: bool,
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

        pl = Pivlabform(config_file, gitlab_host)

        if manual:
            LOGGER.info("process manual run")
            pl.process_manual_configuration(
                path_type=type,
                path=path,
                id=id,
                recursive=recursive,
                validate=validate,
            )
        else:
            pl.process_auto_configuration(
                recursive=recursive,
                validate=validate,
            )

    return process(sys.argv[1:]) if len(sys.argv) > 1 else ["--help"]
