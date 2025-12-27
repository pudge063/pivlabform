from ._cli_logic import create_click_command


def main():
    cli = create_click_command()
    cli()


if __name__ == "__main__":
    main()
