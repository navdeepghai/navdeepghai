
import json
import os
import subprocess
import sys
import typing
from shutil import which

import click

import frappe
from frappe import _
from frappe.commands import get_site, pass_context
from frappe.coverage import CodeCoverage
from frappe.exceptions import SiteNotSpecifiedError
from frappe.utils import cint, update_progress_bar

EXTRA_ARGS_CTX = {"ignore_unknown_options": True, "allow_extra_args": True}

if typing.TYPE_CHECKING:
	from IPython.terminal.embed import InteractiveShellEmbed


@click.command("build")
@click.option("--app", help="Build assets for app")
@click.option("--apps", help="Build assets for specific apps")
@click.option(
	"--hard-link",
	is_flag=True,
	default=False,
	help="Copy the files instead of symlinking",
	envvar="FRAPPE_HARD_LINK_ASSETS",
)
@click.option("--production", is_flag=True, default=False, help="Build assets in production mode")
@click.option("--verbose", is_flag=True, default=False, help="Verbose")
@click.option(
	"--force", is_flag=True, default=False, help="Force build assets instead of downloading available"
)
@click.option(
	"--save-metafiles",
	is_flag=True,
	default=False,
	help="Saves esbuild metafiles for built assets. Useful for analyzing bundle size. More info: https://esbuild.github.io/api/#metafile",
)
def build(
	app=None,
	apps=None,
	hard_link=False,
	production=False,
	verbose=False,
	force=False,
	save_metafiles=False,
):
	"Compile JS and CSS source files"
	from frappe.build import bundle, download_frappe_assets
	from frappe.utils.synchronization import filelock

	frappe.init("")

	if not apps and app:
		apps = app

	with filelock("bench_build", is_global=True, timeout=10):
		# dont try downloading assets if force used, app specified or running via CI
		if not (force or apps or os.environ.get("CI")):
			# skip building frappe if assets exist remotely
			skip_frappe = download_frappe_assets(verbose=verbose)
		else:
			skip_frappe = False

		# don't minify in developer_mode for faster builds
		development = frappe.local.conf.developer_mode or frappe.local.dev_server
		mode = "development" if development else "production"
		if production:
			mode = "production"

		bundle(
			mode,
			apps=apps,
			hard_link=hard_link,
			verbose=verbose,
			skip_frappe=skip_frappe,
			save_metafiles=save_metafiles,
		)
