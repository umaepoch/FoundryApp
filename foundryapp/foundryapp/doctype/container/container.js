// Copyright (c) 2021, yashwanth and contributors
// For license information, please see license.txt
frappe.ui.form.on("Container", "fetch_sales_order_data", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    var foreign_buyer = d.foreign_buyer;
    var final_destination = d.final_destination;
    var warehouse = d.warehouse;
    var scheduled_date=d.scheduled_date;
    var po_no=d.customer_po_no;
    console.log("po_no",po_no)
    if(warehouse==undefined || scheduled_date==undefined )
    {
        frappe.msgprint(`Please select Warehouse and Scheduled_date`)
    }
    cur_frm.clear_table("container_details");
    if (foreign_buyer) {
        cur_frm.clear_table("container_details");
        var details = fetch_so_details_foreign_buyer(foreign_buyer)
        for (var j = 0; j < details.length; j++) {
            var child = cur_frm.add_child("container_details");
          frappe.model.set_value(child.doctype, child.name, "so_no", details[j]['name']);
          frappe.model.set_value(child.doctype, child.name, "item", details[j]['item_code']);
          frappe.model.set_value(child.doctype, child.name, "item_name", details[j]['item_name']);
          frappe.model.set_value(child.doctype, child.name, "pallet_size", details[j]['pch_pallet_size']);
          frappe.model.set_value(child.doctype, child.name, "so_qty", details[j]['qty']);
          frappe.model.set_value(child.doctype, child.name, "qty_left_in_so", details[j]['qty_left_in_so']);
          if (warehouse) {
              frappe.model.set_value(child.doctype, child.name, "container_warehouse", warehouse);
          }
          if (scheduled_date) {
            frappe.model.set_value(child.doctype, child.name, "scheduled_date", scheduled_date);
          }
          frappe.model.set_value(child.doctype, child.name, "final_destination", final_destination);
          frappe.model.set_value(child.doctype, child.name, "customer_po_number", details[j]['po_no']);
          frappe.model.set_value(child.doctype, child.name, "so_date",details[j]['delivery_date']);
         frappe.model.set_value(child.doctype, child.name, "initial_delivery_date", details[j]['transaction_date']);
            cur_frm.refresh_field("container_details");
        }
     }

    if (foreign_buyer && final_destination) {
        cur_frm.clear_table("container_details");
        var details = fetch_so_details_fo_final(foreign_buyer, final_destination)
        for (var j = 0; j < details.length; j++) {
            var child = cur_frm.add_child("container_details");
            // console.log("entered in row");
            // console.log(details[j])
            frappe.model.set_value(child.doctype, child.name, "so_no", details[j]['name']);
          frappe.model.set_value(child.doctype, child.name, "item", details[j]['item_code']);
          frappe.model.set_value(child.doctype, child.name, "item_name", details[j]['item_name']);
          frappe.model.set_value(child.doctype, child.name, "pallet_size", details[j]['pch_pallet_size']);
          frappe.model.set_value(child.doctype, child.name, "so_qty", details[j]['qty']);
          frappe.model.set_value(child.doctype, child.name, "qty_left_in_so", details[j]['qty_left_in_so']);
          if (warehouse) {
              frappe.model.set_value(child.doctype, child.name, "container_warehouse", warehouse);
          }
          if (scheduled_date) {
            frappe.model.set_value(child.doctype, child.name, "scheduled_date", scheduled_date);
        }
          frappe.model.set_value(child.doctype, child.name, "final_destination", final_destination);
          frappe.model.set_value(child.doctype, child.name, "customer_po_number", details[j]['po_no']);
          frappe.model.set_value(child.doctype, child.name, "so_date",details[j]['delivery_date']);
         frappe.model.set_value(child.doctype, child.name, "initial_delivery_date", details[j]['transaction_date']);
            cur_frm.refresh_field("container_details");
        }
        // }
    } 
    if (foreign_buyer && po_no) {
        cur_frm.clear_table("container_details");
        var details = fetch_so_details_po_no(foreign_buyer,po_no)
        for (var j = 0; j < details.length; j++) {
          var child = cur_frm.add_child("container_details");
          frappe.model.set_value(child.doctype, child.name, "so_no", details[j]['name']);
          frappe.model.set_value(child.doctype, child.name, "item", details[j]['item_code']);
          frappe.model.set_value(child.doctype, child.name, "item_name", details[j]['item_name']);
          frappe.model.set_value(child.doctype, child.name, "pallet_size", details[j]['pch_pallet_size']);
          frappe.model.set_value(child.doctype, child.name, "so_qty", details[j]['qty']);
          frappe.model.set_value(child.doctype, child.name, "qty_left_in_so", details[j]['qty_left_in_so']);
          if (warehouse) {
              frappe.model.set_value(child.doctype, child.name, "container_warehouse", warehouse);
          }
          if (scheduled_date) {
            frappe.model.set_value(child.doctype, child.name, "scheduled_date", scheduled_date);
        }
          frappe.model.set_value(child.doctype, child.name, "final_destination", final_destination);
          frappe.model.set_value(child.doctype, child.name, "customer_po_number", details[j]['po_no']);
          frappe.model.set_value(child.doctype, child.name, "so_date",details[j]['delivery_date']);
         frappe.model.set_value(child.doctype, child.name, "initial_delivery_date", details[j]['transaction_date']);
            cur_frm.refresh_field("container_details");
        }
        // }
    }
    if (foreign_buyer && final_destination && po_no) {
        cur_frm.clear_table("container_details");
        var details = fetch_so_details(foreign_buyer, final_destination,po_no);
        console.log("details",details)
        for (var j = 0; j < details.length; j++) {
            var child = cur_frm.add_child("container_details");
            // console.log("entered in row");
            // console.log(details[j])
            frappe.model.set_value(child.doctype, child.name, "so_no", details[j]['name']);
          frappe.model.set_value(child.doctype, child.name, "item", details[j]['item_code']);
          frappe.model.set_value(child.doctype, child.name, "item_name", details[j]['item_name']);
          frappe.model.set_value(child.doctype, child.name, "pallet_size", details[j]['pch_pallet_size']);
          frappe.model.set_value(child.doctype, child.name, "so_qty", details[j]['qty']);
          frappe.model.set_value(child.doctype, child.name, "qty_left_in_so", details[j]['qty_left_in_so']);
          if (warehouse) {
              frappe.model.set_value(child.doctype, child.name, "container_warehouse", warehouse);
          }
          if (scheduled_date) {
            frappe.model.set_value(child.doctype, child.name, "scheduled_date", scheduled_date);
        }
          frappe.model.set_value(child.doctype, child.name, "final_destination", final_destination);
          frappe.model.set_value(child.doctype, child.name, "customer_po_number", details[j]['po_no']);
          frappe.model.set_value(child.doctype, child.name, "so_date",details[j]['delivery_date']);
         frappe.model.set_value(child.doctype, child.name, "initial_delivery_date", details[j]['transaction_date']);
            cur_frm.refresh_field("container_details");
        }
        // }
    } 
    
  });

function fetch_so_details_foreign_buyer(foreign_buyer) {
    console.log("entered into function");
    var selected_so = "";
    frappe.call({
        method: 'foundryapp.foundryapp.doctype.container.container.fetch_so_details_foriegn_buyer',
        args: {
            "foreign_buyer": foreign_buyer
        },
        async: false,
        callback: function(r) {
            if (r.message) {
                // console.log(r.message)
                selected_so = r.message;
            }
        }
    });
    return selected_so;
}

function fetch_so_details_po_no(foreign_buyer,po_no) {
    console.log("entered into function");
    var selected_so = "";
    frappe.call({
        method: 'foundryapp.foundryapp.doctype.container.container.fetch_so_details_po_no',
        args: {
            "foreign_buyer": foreign_buyer,
            "po_no": po_no
        },
        async: false,
        callback: function(r) {
            if (r.message) {
                // console.log(r.message)
                selected_so = r.message;
            }
        }
    });
    return selected_so;
}

function fetch_so_details_fo_final(foreign_buyer, final_destination) {
    console.log("entered into function");
    var selected_so = "";
    frappe.call({
        method: 'foundryapp.foundryapp.doctype.container.container.fetch_so_details_final_foreign',
        args: {
            "foreign_buyer": foreign_buyer,
            "final_destination": final_destination
        },
        async: false,
        callback: function(r) {
            if (r.message) {
                // console.log(r.message)
                selected_so = r.message;
            }
        }
    });
    return selected_so;
}

function fetch_so_details(foreign_buyer, final_destination,po_no) {

    console.log("entered into function");
    var selected_so = "";
    frappe.call({
        method: 'foundryapp.foundryapp.doctype.container.container.fetch_so_details',
        args: {
            "foreign_buyer": foreign_buyer,
            "final_destination": final_destination,
            "po_no":po_no
        },
        async: false,
        callback: function(r) {
            if (r.message) {
                console.log(r.message)
                selected_so = r.message;

            }
        }
    });
    return selected_so;
 }
  
  
frappe.ui.form.on("Container Child", "qty_to_be_filled", function(frm, cdt, cdn) {
    var child = locals[cdt][cdn]
    var qty_to_be_filled = child.qty_to_be_filled
    var qty_left_in_so = child.qty_left_in_so
    console.log(child)
    if (qty_to_be_filled > qty_left_in_so) {
        frappe.msgprint(`Quantity to be filled is greater than quantity left in sales order: ${qty_left_in_so}`)
    }


})




function check_for_existing(foreign_buyer, final_destination) {
    var print;
    frappe.call({
        method: 'foundryapp.foundryapp.doctype.container.container.validate_container_exist',
        args: {
            "foreign_buyer": foreign_buyer,
            "final_destination": final_destination
        },
        async: false,
        callback: function(r) {
            if (r.message) {
                // console.log(r.message[0]["name"])
                print = r.message
            }
        }
    })
    return print
}

frappe.ui.form.on("Container", "validate", function(frm, cdt, cdn) {
    $.each(frm.doc.container_details || [], function(i, d) {
        // console.log("enterd in for loop");
        if (d.so_qty % d.pallet_size != 0 || d.qty_to_be_filled % d.pallet_size != 0) {
            console.log("enterd in for loop", d.so_qty);
            frappe.msgprint("So Qty and Qty To Be Filled must be multiple of Pallet Size.Please correct Row" + '"' + d.idx + '"' + "  ")
            frappe.validated = false;
        }
})
});


frappe.ui.form.on("Container", "after_save", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    var parent = frm.doc.name;
    var foreign_buyer = d.foreign_buyer;
    var final_destination = d.final_destination;
    var container_child = frm.doc.container_details;
    var scheduled_date=d.scheduled_date;
    var warehouse = d.warehouse;
    var item = "";
    var so_no = "";
    var sum_quantiy = 0
    for (var i = 0; i < container_child.length; i++) {
        var qty_to_be_filled = container_child[i].qty_to_be_filled
        var qty_left_in_so = container_child[i].qty_left_in_so
        if (scheduled_date) {
        container_child[i].scheduled_date = scheduled_date
        }
        if (warehouse) {
        container_child[i].container_warehouse = warehouse
        }
        item = container_child[i].item;
        so_no = container_child[i].so_no;
        console.log("qty_to_be_filled",qty_to_be_filled)
        console.log("qty_left_in_so",qty_left_in_so)
        container_child[i]['so_quantity_not_placed_in_containers_before_this_container'] = qty_left_in_so;
        var qty_not_placed_in_container = qty_left_in_so-qty_to_be_filled;
        console.log("qty_not_placed_in_container", qty_not_placed_in_container)
        container_child[i]['so_quantity_not_placed_in_containers_after_this_container'] = qty_not_placed_in_container;
        var qty = sum_of_qty(parent, item);
        console.log("qty", qty);
        container_child[i].total_quantity_of_item_in_container = qty;
        let weight_of_item = fetch_item_weight(item)
        let total_qty = qty_to_be_filled * weight_of_item
        sum_quantiy += total_qty
    } //end of for loop
    sum_quantiy = sum_quantiy / 1000
    d.total_planned_net_weight_of_container = sum_quantiy
    
});

//dispatch item
frappe.ui.form.on("Container", "fetch_dispatch_items", function(frm, cdt, cdn) {
    var cont = locals[cdt][cdn]
    var container_child = cont.container_details;
    // console.log(container_child)
    cur_frm.clear_table("dispatch_items");
    var parent=cont.name;
        let dispatch = fetch_dispatch(parent)
       console.log("dispatch",dispatch)
       dispatch.forEach((details) => {
        console.log("entering dispatch loo")
        var child = cur_frm.add_child("dispatch_items");
        frappe.model.set_value(child.doctype, child.name, "invoice_item", details['item']);
        frappe.model.set_value(child.doctype, child.name, "item_name", details['item_name']);
        frappe.model.set_value(child.doctype, child.name, "pallet_size", details['pch_pallet_size']);
        frappe.model.set_value(child.doctype, child.name, "quantity_planned_in_container", details['total_quantity_of_item_in_container']);
        frappe.model.set_value(child.doctype, child.name, "dispatch_item", details['dispatch_items']);
        frappe.model.set_value(child.doctype, child.name, "quantity", details['total_quantity_of_item_in_container']);

        // cur_frm.refresh_field("dispatch_items");
    });

    //frm.save();
})


//OPEN PO and CLOSED PO VALIDATION
frappe.ui.form.on("Container", "validate", function(frm, cdt, cdn) {
    var checked_so = {};
    var is_po_matching = true;
    var d = locals[cdt][cdn];
    var container_child = frm.doc.container_details;
    var open_po_count = 0;
    var closed_po_count = 0;
    for (var i = 0; i < container_child.length; i++) {
        var so_number = container_child[i]['so_no'];
        console.log("selected sales order number", so_number);
        var pch_po_type = fetch_pch_details(so_number);
        if (pch_po_type.pch_po_type == "Open PO") {
            open_po_count++;
            if (open_po_count >= 2) {
                is_po_matching = true;
            }
        }
        if (pch_po_type.pch_po_type == "Closed PO") {
            if (checked_so[so_number] !== "X") {
                checked_so[so_number] = "X";
                closed_po_count++;
            }
            if (closed_po_count > 1) {
                is_po_matching = false;
                break;
            }
        }

        if (i == 0) {
            var po_status = pch_po_type.pch_po_type;
        }
        console.log("pch_po_type ", pch_po_type);
        if (pch_po_type.pch_po_type !== po_status) {
            is_po_matching = false;
        }
    }
    if (is_po_matching) {
        //frappe.msgprint("You can save your container");
        frappe.validated = true;
    } else {
        frappe.msgprint("You cannot save container.Please check Po Type of sales order");
        frappe.validated = false;
    }
});

function fetch_pch_details(so_number) {
    console.log("entered into function");
    var fetched_details = "";
    frappe.call({
        method: 'frappe.client.get_value',
        args: {
            'doctype': 'Sales Order',
            'fieldname': 'pch_po_type',

            'filters': {
                'name': so_number,
            }
        },
        async: false,
        callback: function(r) {
            if (r.message) {
                fetched_details = r.message;
                console.log("readings-----------" + JSON.stringify(r.message));

            }
        }
    });
    return fetched_details;
}
function fetch_item_weight(item_code) {
    var weight;
    frappe.call({
        method: 'frappe.client.get_value',
        args: {
            'doctype': 'Item',
            'fieldname': 'weight_per_unit',

            'filters': {
                'item_code': item_code,
            }
        },
        async: false,
        callback: function(r) {
            if (r.message) {
                weight = r.message.weight_per_unit
            }
        }
    });
    return weight;
}

function fetch_dispatch(parent) {
    let items;
    frappe.call({
        method: 'foundryapp.foundryapp.doctype.container.container.get_container_dispatch_items',
        args: {
            "parent": parent
        },
        async: false,
        callback: function(r) {
            if (r.message) {
                // console.log(r.message)
                items = r.message
            }
        }
    })
    return items
}



function sum_of_qty(parent, item) {
    var qty;
    frappe.call({
        method: 'foundryapp.foundryapp.doctype.container.container.qty_sum',
        args: {
            "parent": parent,
            "item": item
        },
        async: false,
        callback: function(r) {
            if (r.message) {
                // console.log(r.message[0]["name"])
                qty = r.message
            }
        }
    })
    return qty
}



function qty_in_container(foreign_buyer, final_destination, so_no, item) {
    var qty;
    frappe.call({
        method: 'foundryapp.foundryapp.doctype.container.container.container_details',
        args: {
            "foreign_buyer": foreign_buyer,
            "final_destination": final_destination,
            "so_no": so_no,
            "item": item,
        },
        async: false,
        callback: function(r) {
            if (r.message) {
                // console.log(r.message[0]["name"])
                qty = r.message
            }
        }
    })
    return qty
}


