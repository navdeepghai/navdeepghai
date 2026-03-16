# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "navdeepghai"
app_title = "NavdeepGhai"
app_publisher = "NavdeepGhai"
app_description = "NavdeepGhai"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "navdeepghai1@gmail.com"
app_license = "MIT"

app_logo_url = '/assets/navdeepghai/images/social-logo.jpg'
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
    "https://fonts.googleapis.com/css?family=Montserrat",
    "navdeepghai.bundle.css",
]

app_include_js = [
    "navdeepghai.bundle.js",
]

# include js, css files in header of web template
web_include_css = [
]

web_include_js = [
]


# Update website context
update_website_context = "navdeepghai.website.website.update_website_context"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

boot_session = "navdeepghai.boot.update_boot_context"
# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "navdeepghai.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "navdeepghai.install.before_install"
# after_install = "navdeepghai.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "navdeepghai.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "*": {
        "validate": "navdeepghai.document_controllers.base_controller.handler"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
 		"navdeepghai.tracking.utils.phone_tracking.sync_location_data"
 	]
}

# Testing
# -------

# before_tests = "NavdeepGhai.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "NavdeepGhai.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "navdeepghai.task.get_dashboard_data"
# }
