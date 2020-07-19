'''
    Developer Navdeep
'''

import frappe
from frappe import _

no_cache = 1

def get_context(context):
    settings = frappe.get_doc("Websites Settings", "Websites Settings").as_dict()
    context.update({
        "title": _("Germbustomer"),
        "germbusters_settings": settings,
        "body_cards": get_cards("/"),
        "images": get_images("/"),
        "carousels": get_carousels('/')
    })

def get_cards(website_route='/'):
    cards = []
    for card in frappe.db.get_values("Website Card", filters={"website_route": website_route}, as_dict=True):
        cards.append(frappe.get_doc("Website Card", card.get("name")))
    return cards

def get_carousels(website_route='/'):
    carousels = []
    for carousel in frappe.db.get_values("Website Carousel", filters={"website_route": website_route}, as_dict=True):
        carousels.append(frappe.get_doc("Website Carousel", carousel.get("name")).as_dict())
    return carousels


def get_images(website_route):
    images = []
    for image in frappe.db.sql("""SELECT * FROM `tabWebsite Image` WHERE website_route='%s' """%(website_route), as_dict=True):
        if(image.image_set and frappe.db.exists("Website Image Set", "Website Image Set")):
            image.image_set = frappe.get_doc("Website Image Set", image.image_set).as_dict().get("images")
        else:
            image.image_set = []
        image.images = frappe.db.sql("""SELECT * FROM `tabWebsite Image Item` WHERE
                    `tabWebsite Image Item`.parent='%s' """%(image.name), as_dict=True)
        images.append(image)
    return images
