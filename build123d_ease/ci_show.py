"""Create a version of the `show()` function which runs silently in a CI environment."""

# pyright: reportMissingTypeStubs=information, reportUnknownMemberType=information

import os

import build123d as bd

if os.getenv("CI"):

    def show(*args: object) -> bd.Part:
        """Do nothing (dummy function) to skip showing the CAD model in CI."""
        if not isinstance(args[0], bd.Part):
            msg = "The first argument must be a Part object."
            raise TypeError(msg)

        return args[0]
else:
    import ocp_vscode

    def show(*args: object) -> bd.Part:
        """Show the CAD model in the CAD viewer."""
        if not isinstance(args[0], bd.Part):
            msg = "The first argument must be a Part object."
            raise TypeError(msg)

        ocp_vscode.show(*args)
        return args[0]
