import requests
import json
import frappe
from six.moves.urllib.parse import urlparse
from six.moves.urllib.parse import parse_qs

@frappe.whitelist()
def get_container():
    try:
        query_string = urlparse(frappe.request.url).query
        # print(query_string)
        query = parse_qs(query_string)
        print("parameters : ",query)
        # req = json.loads(frappe.request.data)
        # module = str(req.get('foreign_buyer')).strip()
        return "api hit successful...."
    except Exception as ex:
        print("Exception : ",ex)
        return ex
