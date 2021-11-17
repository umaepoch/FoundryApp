// Copyright (c) 2021, yashwanth and contributors
// For license information, please see license.txt

frappe.ui.form.on('KYC','profile', function(frm, cdt, cdn) {
  var doc = locals[cdt][cdn]
  const capture = new frappe.ui.Capture()
  // opens the camera module api.
  capture.show()

  // captures the image.
  capture.submit((data) => {
    let name = doc.name+'_profile'
    let img_ar = data.split(",")
    let file_url = create_file(img_ar[1], doc.name, doc.doctype)
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
    let file_url = create_file(img_ar[1], doc.name, doc.doctype)
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
    let file_url = create_file(img_ar[1], doc.name, doc.doctype)
  });
});


function create_file(img, name, doc_type) {
  let url;
  frappe.call({
    method: 'foundryapp.foundryapp.doctype.kyc.kyc.create_file',
    args: {
      'image': img,
      'doc_name': name,
      'doctype': doc_type
    },
    async: false,
    callback: function(r) {
      if (r.message) {
        if (r.message.EX) {
          console.log(r.message.EX)
        }
        if (r.message.SC) {
          console.log(r.message.SC)
          url = r.message.url
        }
      }
    }
  });
  return url
}


// frappe.ui.form.on("KYC", "before_save", function(frm, cdt, cdn){
//   cur_frm.set_value("profile_url", "/files/profile_url");
//   cur_frm.set_value("adhaar_url", "/files/adhaar_url");
//   cur_frm.set_value("pan_url", "/files/pan_url");
// })
