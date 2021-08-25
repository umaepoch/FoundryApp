// Copyright (c) 2021, yashwanth and contributors
// For license information, please see license.txt

frappe.ui.form.on("Container","fetch_sales_order_data", function(frm ,cdt , cdn)
{
    var d = locals[cdt][cdn];
    var foreign_buyer = d.foreign_buyer;
    var final_destination = d.final_destination;
    var warehouse = d.warehouse;

    if (foreign_buyer && final_destination) {
        var msg = validate(foreign_buyer, final_destination)
        if (msg.length > 0) {
          var existing = ""
          msg.forEach((cont)=> {
            existing += cont["name"]+" "
          })
          // frappe.msgprint(`The Following Container Plans ${existing}exist for this combination that has not been Finalized yet. Do you want to work with that Document`)
          frappe.confirm(`The Following Container Plans ${existing} exist for this combination that has not been Finalized yet. Do you want to work with that Document?`,
            () => {
              // action to perform if Yes is selected
            }, () => {
              // action to perform if No is selected
            })
        }
        if (msg.length == 0) {
          var details=fetch_so_details(foreign_buyer,final_destination)
          for(var j=0;j<details.length;j++){
        	   var child = cur_frm.add_child("container_details");
        	   // console.log("entered in row");
             // console.log(details[j])
             frappe.model.set_value(child.doctype, child.name, "so_no",details[j]['name']);
             frappe.model.set_value(child.doctype, child.name, "item",details[j]['item_code']);
        	   frappe.model.set_value(child.doctype, child.name, "pallet_size",details[j]['pch_pallet_size']);
             frappe.model.set_value(child.doctype, child.name, "so_qty",details[j]['qty']);
             if (warehouse) {
               frappe.model.set_value(child.doctype, child.name, "container_warehouse",warehouse);
             }
             frappe.model.set_value(child.doctype, child.name, "final_destination",final_destination);
             frappe.model.set_value(child.doctype, child.name, "customer_po_number",details[j]['po_no']);
        	   frappe.model.set_value(child.doctype, child.name, "so_date",details[j]['delivery_date']);
        	   frappe.model.set_value(child.doctype, child.name, "initial_delivery_date",details[j]['transaction_date']);
        	   cur_frm.refresh_field("container_details");
        	}
        }
    } else {
      frappe.msgprint(`please enter the mandatory field Foreign Buyer and Final Destination`)
    }
});

function fetch_so_details(foreign_buyer,final_destination)
{

    console.log("entered into function");
    var selected_so= "";
    frappe.call({
        method: 'foundryapp.foundryapp.doctype.container.container.fetch_so_details',
        args: {
            "foreign_buyer":foreign_buyer,
            "final_destination":final_destination
        },
        async: false,
        callback: function(r) {
            if (r.message) {
                selected_so = r.message;
            }
        }
    });
    return selected_so;
}

frappe.ui.form.on("Container", "after_save", function(frm, cdt, cdn){
  var container = locals[cdt][cdn]
  var sum_quantiy = 0

  container.container_details.forEach((child) => {
    let item = child.item
    let qty_to_be_filled = child.qty_to_be_filled

    let weight_of_item = fetch_item_weight(item)
    let qty = qty_to_be_filled * weight_of_item
    sum_quantiy += qty
  });

  console.log(sum_quantiy)
  sum_quantiy = sum_quantiy/1000
  container.total_planned_net_weight_of_container = sum_quantiy
  console.log(sum_quantiy)

});

function fetch_item_weight(item_code) {
  var weight;

  frappe.call({
      method: 'frappe.client.get_value',
      args: {
          'doctype': 'Item',
          'fieldname': 'weight_per_unit',

          'filters': {
             'item_code':item_code,
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

// frappe.ui.form.on("Container", "onload", function(frm, cdt, cdn) {
//   var prev_route = frappe.get_prev_route();
//   console.log(prev_route)
//   var container = locals[cdt][cdn]
//   var foreign_buyer = container.foreign_buyer
//   var final_destination = container.final_destination
//   // console.log(foreign_buyer)
//   // console.log(final_destination)
//
//   if (foreign_buyer && final_destination) {
//     var msg = validate(foreign_buyer, final_destination)
//     if (msg.length > 0) {
//       var existing = ""
//       msg.forEach((cont)=> {
//         existing += cont["name"]+" "
//       })
//       frappe.msgprint(`The Following Container Plans ${existing}exist for this combination that has not been Finalized yet. Do you want to work with that Document`)
//     }
//   }
// })

function validate(foreign_buyer, final_destination) {
  var print;
  frappe.call({
    method: 'foundryapp.foundryapp.doctype.container.container.validate_container_exist',
    args: {
      "foreign_buyer": foreign_buyer,
      "final_destination": final_destination
    },
    async: false,
    callback: function(r) {
      if(r.message){
        // console.log(r.message[0]["name"])
        print = r.message
      }
    }
  })
  return print
}

frappe.ui.form.on("Container", "validate", function(frm, cdt, cdn) {
	$.each(frm.doc.container_details || [], function(i, d) {
		console.log("enterd in for loop");
		if(d.so_qty%d.pallet_size!=0 || d.qty_to_be_filled%d.pallet_size!=0){
			console.log("enterd in for loop",d.so_qty);
			frappe.msgprint("So Qty and Qty To Be Filled must be multiple of Pallet Size.Please correct Row"+ '"'+d.idx+'"'+"  ")
			frappe.validated = false;
		}
	})
});
