// Copyright (c) 2021, yashwanth and contributors
// For license information, please see license.txt

frappe.ui.form.on("Container","fetch_sales_order_data", function(frm ,cdt , cdn)
{
    var d = locals[cdt][cdn];
    var foreign_buyer = d.foreign_buyer;
    var final_destination = d.final_destination;
    var warehouse = d.warehouse;

    if (foreign_buyer && final_destination) {
        // var msg = check_for_existing(foreign_buyer, final_destination)
        // if (msg.length > 0) {
        //   var existing = ""
        //   msg.forEach((cont)=> {
        //     existing += cont["name"]+" "
        //   })
        //   // frappe.msgprint(`The Following Container Plans ${existing}exist for this combination that has not been Finalized yet. Do you want to work with that Document`)
        //   frappe.confirm(`The Following Container Plans ${existing} exist for this combination that has not been Finalized yet. Do you want to work with that Document?`,
        //     () => {
        //       // action to perform if Yes is selected
        //     }, () => {
        //       // action to perform if No is selected
        //     })
        // }
        // if (msg.length == 0) {
          var details=fetch_so_details(foreign_buyer,final_destination, cdt)
          for(var j=0;j<details.length;j++){
        	   var child = cur_frm.add_child("container_details");
        	   // console.log("entered in row");
             // console.log(details[j])
             frappe.model.set_value(child.doctype, child.name, "so_no",details[j]['name']);
             frappe.model.set_value(child.doctype, child.name, "item",details[j]['item_code']);
        	   frappe.model.set_value(child.doctype, child.name, "pallet_size",details[j]['pch_pallet_size']);
             frappe.model.set_value(child.doctype, child.name, "so_qty",details[j]['qty']);
             frappe.model.set_value(child.doctype, child.name, "qty_left_in_so",details[j]['quantity_left_in_so']);
             if (warehouse) {
               frappe.model.set_value(child.doctype, child.name, "container_warehouse",warehouse);
             }
             frappe.model.set_value(child.doctype, child.name, "final_destination",final_destination);
             frappe.model.set_value(child.doctype, child.name, "customer_po_number",details[j]['po_no']);
        	   frappe.model.set_value(child.doctype, child.name, "so_date",details[j]['delivery_date']);
        	   frappe.model.set_value(child.doctype, child.name, "initial_delivery_date",details[j]['transaction_date']);
        	   cur_frm.refresh_field("container_details");
        	}
        // }
    } else {
      frappe.msgprint(`please enter the mandatory field Foreign Buyer and Final Destination`)
    }
});

function fetch_so_details(foreign_buyer,final_destination, cdt)
{

    console.log("entered into function");
    var selected_so= "";
    frappe.call({
        method: 'foundryapp.foundryapp.doctype.container.container.fetch_so_details',
        args: {
            "document": cdt,
            "foreign_buyer":foreign_buyer,
            "final_destination":final_destination
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

/*frappe.ui.form.on("Container Child", "qty_to_be_filled", function(frm, cdt, cdn){
  var child = locals[cdt][cdn]
  var qty_to_be_filled = child.qty_to_be_filled
  var qty_left_in_so = child.qty_left_in_so
  console.log(child)
  if (qty_to_be_filled > qty_left_in_so) {
    frappe.msgprint(`Quantity to be filled is greater than quantity left in sales order: ${qty_left_in_so}`)
  }
  if (qty_left_in_so !== 0 && qty_left_in_so >= qty_to_be_filled){
    let so_no = child.so_no
    let item = child.item
    let so_qty_left = child.qty_left_in_so - child.qty_to_be_filled
    update_so_qty_left(so_no, item, so_qty_left)
  }

})*/

frappe.ui.form.on("Container", "after_save", function(frm, cdt, cdn){
  var container = locals[cdt][cdn]
  var sum_quantiy = 0

  container.container_details.forEach((child) => {
    let item = child.item
    let so_no = child.so_no
    let qty_to_be_filled = child.qty_to_be_filled
    let qty_left_in_so = child.qty_left_in_so
    let so_qty_left = 0

    let weight_of_item = fetch_item_weight(item)
    let qty = qty_to_be_filled * weight_of_item
    sum_quantiy += qty
  });

  // console.log(sum_quantiy)
  sum_quantiy = sum_quantiy/1000
  container.total_planned_net_weight_of_container = sum_quantiy
  // console.log(sum_quantiy)

});

frappe.ui.form.on("Container Child", "validate", function(frm, cdt, cdn) {
  var child = locals[cdt][cdn]
  console.log(child)
})

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

function update_so_qty_left(so_no, item, so_qty_left) {
  let flag;
  frappe.call({
    method: 'foundryapp.foundryapp.doctype.container.container.update_so_for_qty',
    args: {
      "so_no": so_no,
      "item": item,
      "so_qty_left": so_qty_left
    },
    async: false,
    callback: function(r) {
      if(r.message) {
        console.log(r.message)
        flag = r.message
      }
    }
  })
  return flag
}

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
		// console.log("enterd in for loop");
		if(d.so_qty%d.pallet_size!=0 || d.qty_to_be_filled%d.pallet_size!=0){
			console.log("enterd in for loop",d.so_qty);
			frappe.msgprint("So Qty and Qty To Be Filled must be multiple of Pallet Size.Please correct Row"+ '"'+d.idx+'"'+"  ")
			frappe.validated = false;
		}
	})
});

frappe.ui.form.on("Container", "after_save", function(frm, cdt, cdn) {
  var cont = locals[cdt][cdn]
  var container_child = cont.container_details;
  // console.log(container_child)
  container_child.forEach((child) => {
    console.log("entering child loop")
    let so_no = child.so_no
    let item_code = child.item
    let parent = child.parent

    let dispatch = fetch_dispatch(so_no, item_code,parent)
    dispatch.forEach((details) => {
      console.log("entering dispatch loo")
      var child = cur_frm.add_child("dispatch_items");
      frappe.model.set_value(child.doctype, child.name, "invoice_item",details['item']);
      frappe.model.set_value(child.doctype, child.name, "pallet_size",details['pallet_size']);
      frappe.model.set_value(child.doctype, child.name, "quantity_planned_in_container",details['quantity_planned_in_container']);
      frappe.model.set_value(child.doctype, child.name, "dispatch_item",details['dispatch_items']);
      frappe.model.set_value(child.doctype, child.name, "quantity",details['quantity']);

      // cur_frm.refresh_field("dispatch_items");
    });
  })
})

function fetch_dispatch(so_no, item_code, parent) {
  let items;
  frappe.call({
    method: 'foundryapp.foundryapp.doctype.container.container.get_container_dispatch_items',
    args: {
      "so_no": so_no,
      "item_code": item_code,
      "parent": parent
    },
    async: false,
    callback: function(r) {
      if(r.message) {
        // console.log(r.message)
        items = r.message
      }
    }
  })
  return items
}

frappe.ui.form.on("Container","after_save", function(frm ,cdt , cdn)
{
        var d = locals[cdt][cdn];
        var parent=frm.doc.name;
	    var container_child = frm.doc.container_details;
	   
	    var item="";
	    for (var i = 0; i < container_child.length; i++)
        {
             
            item=container_child[i].item;
          
           var qty=sum_of_qty(parent, item);
           console.log("qty",qty);
         
          container_child[i].total_quantity_of_item_in_container=qty;
	}//end of for loop
});

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
      if(r.message){
        // console.log(r.message[0]["name"])
        qty = r.message
      }
    }
  })
  return qty
}