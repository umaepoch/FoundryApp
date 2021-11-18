// Copyright (c) 2021, yashwanth and contributors
// For license information, please see license.txt

let images = {}

frappe.ui.form.on('KYC','profile', function(frm, cdt, cdn) {
  var doc = locals[cdt][cdn]
  const capture = new frappe.ui.Capture()

  capture.show()
  // captures the image.
  capture.submit((data) => {
    let name = doc.name+'_profile'
    let img_ar = data.split(",")
    images.profile = img_ar[1]
  });
});

frappe.ui.form.on('KYC','adhaar', function(frm, cdt, cdn) {
  var doc = locals[cdt][cdn]
  const capture = new frappe.ui.Capture()
  // opens the camera module api.
  capture.show()

  // captures the image.
  capture.submit((data) => {
    let name = doc.name+'_adhaar'
    let img_ar = data.split(",")
    images.adhaar = img_ar[1]
  });
});

frappe.ui.form.on('KYC','pan', function(frm, cdt, cdn) {
  var doc = locals[cdt][cdn]
  const capture = new frappe.ui.Capture()
  // opens the camera module api.
  capture.show()

  // captures the image.
  capture.submit((data) => {
    let name = doc.name+'_pan'
    let img_ar = data.split(",")
    images.pan = img_ar[1]
  });
});


frappe.ui.form.on("KYC", "after_save", function(frm, cdt, cdn) {
  var doc = locals[cdt][cdn]
  var kyc = {
    "name": doc.name,
    "type": doc.doctype,
    "images": images
  }
  console.log(kyc)
  var file_url = create_file(JSON.stringify(kyc))
  if (file_url) {
    // cur_frm.set_value("profile_url", file_url[])
    console.log(file_url)
    // frm.reload_doc()
  }
})

function create_file(doc) {
  let url;
  frappe.call({
    method: 'foundryapp.foundryapp.doctype.kyc.kyc.create_file',
    args: {
      'doc': doc
    },
    async: false,
    callback: function(r) {
      if (r.message) {
        if (r.message.EX) {
          console.log(r.message.EX)
        }
        if (r.message.SC) {
          console.log(r.message.SC)
          url = r.message.SC
        }
      }
    }
  });
  return url
}

// frappe.ui.form.on("KYC", "before_save", function(frm, cdt, cdn){
//   // cur_frm.set_value("profile_url", "/files/profile_url");
//   // cur_frm.set_value("adhaar_url", "/files/adhaar_url");
//   // cur_frm.set_value("pan_url", "/files/pan_url");
//   cur_frm.set_value("profile_preview", "");
// })

// frappe.ui.form.on("KYC", "refresh", function(frm, cdt, cdn) {
//   var img = new Image()
//   img.src = data
//   console.log($('.profile_preview'))
//   $('.profile_preview').html(`<img src=${img.src}>`)
// })
