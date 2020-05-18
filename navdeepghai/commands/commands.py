
from __future__ import unicode_literals, absolute_import, print_function
import click
import json, os, sys, subprocess
import frappe
from frappe.build import make_asset_dirs, get_node_pacman, check_yarn, app_paths
from os.path import exists as path_exists, join as join_path, abspath, isdir

@click.command('build-navdeepghai')
@click.option('--app', help='Build assets for app')
@click.option('--make-copy', is_flag=True, default=False, help='Copy the files instead of symlinking')
@click.option('--restore', is_flag=True, default=False, help='Copy the files instead of symlinking with force')
@click.option('--verbose', is_flag=True, default=False, help='Verbose')
def build(app=None, make_copy=False, restore = False, verbose=False):
	"Minify + concatenate JS and CSS files, build translations"
	import frappe.build
	import frappe
	frappe.init('')
	# don't minify in developer_mode for faster builds
	no_compress = frappe.local.conf.developer_mode or False
	bundle(no_compress, app="navdeepghai", make_copy=make_copy, restore = restore, verbose=verbose)

def setup():
	pymodules = [frappe.get_module("navdeepghai")]
	return [os.path.dirname(pymodule.__file__) for pymodule in pymodules]


def bundle(no_compress, app=None, make_copy=False, restore=False, verbose=False):
	"""concat / minify js files"""
	app_paths = setup()

	make_asset_dirs(make_copy=make_copy, restore=restore)

	pacman = get_node_pacman()
	mode = 'build' if no_compress else 'production'
	command = '{pacman} run {mode}'.format(pacman=pacman, mode=mode)

	if app:
		command += ' --app {app}'.format(app=app)

	frappe_app_path = abspath(join_path(app_paths[0], '..'))
	check_yarn()
	frappe.commands.popen(command, cwd=frappe_app_path)
