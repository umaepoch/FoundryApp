// Copyright (c) 2021, yashwanth and contributors
// For license information, please see license.txt

let images = {}

frappe.ui.form.on('KYC','profile', function(frm, cdt, cdn) {
  var doc = locals[cdt][cdn]
  const capture = new frappe.ui.Capture()

  capture.show()
  // captures the image.
  capture.submit((data) => {
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
    let img_ar = data.split(",")
    images.pan = img_ar[1]
  });
});


frappe.ui.form.on("KYC", "after_save", function(frm, cdt, cdn) {
  var doc = locals[cdt][cdn]
  var kyc = {
    "user": doc.user_name,
    "name": doc.name,
    "type": doc.doctype,
    "images": images
  }
  var file_url = create_file(JSON.stringify(kyc))
  if (file_url) {
    var flag = set_image_url(file_url['profile'], file_url['adhaar'], file_url['pan'], doc.name, doc.doctype)
    console.log(flag)
    if (flag === 1) {
      frm.reload_doc()
    }
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
          frappe.throw(__(r.message.EX))
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


function set_image_url(profile, adhaar, pan, name, type){
  let flag;
  frappe.call({
    method: 'foundryapp.foundryapp.doctype.kyc.kyc.set_image_url',
    args: {
      "profile_url": profile,
      "adhaar_url": adhaar,
      "pan_url": pan,
      "doc_name": name,
      "doctype": type
    },
    async: false,
    callback: function(r) {
      if (r.message) {
        if (r.message.EX) {
          frappe.throw(__(r.message.EX))
        }
        if (r.message.SC) {
          flag = r.message.SC
        }
      }
    }
  })
  return flag
}


frappe.ui.form.on("KYC", "validate", function(frm, cdt, cdn) {
  if (!frm.doc.user_name) {
    frappe.throw(__("Please enter User Name. To continue."))
    frappe.validated = false;
  }
})


frappe.ui.form.on("KYC", "refresh", function(frm, cdt, cdn) {
  var doc = locals[cdt][cdn]
  if (doc) {
    // For Profile image preview.
    if (doc.profile_url) {
      var wrapper = frm.get_field("profile_preview").$wrapper;
      var is_viewable = frappe.utils.is_image_file(doc.profile_url);

      frm.toggle_display("upload_documents_section", is_viewable);
      frm.toggle_display("profile_preview", is_viewable);

      if(is_viewable){
        wrapper.html('<div class="img_preview">\
        <img class="img-responsive" src="'+doc.profile_url+'"></img>\
        </div>');
      } else {
        wrapper.empty();
      }
    } else {
      var wrapper = frm.get_field("profile_preview").$wrapper;
      var is_viewable = frappe.utils.is_image_file(doc.profile_url);

      frm.toggle_display("profile_preview", is_viewable);

      if (!is_viewable) {
        wrapper.empty();
      }
    }

    // For ADHAAR image preview.
    if (doc.adhaar_url) {
      var wrapper = frm.get_field("adhaar_preview").$wrapper;
      var is_viewable = frappe.utils.is_image_file(doc.adhaar_url);

      frm.toggle_display("upload_documents_section", is_viewable);
      frm.toggle_display("profile_preview", is_viewable);

      if(is_viewable){
        wrapper.html('<div class="img_preview">\
        <img class="img-responsive" src="'+doc.adhaar_url+'"></img>\
        </div>');
      } else {
        wrapper.empty();
      }
    } else {
      var wrapper = frm.get_field("adhaar_preview").$wrapper;
      var is_viewable = frappe.utils.is_image_file(doc.adhaar_url);

      frm.toggle_display("profile_preview", is_viewable);

      if (!is_viewable) {
        wrapper.empty();
      }
    }

    // For PAN image preview.
    if (doc.pan_url) {
      var wrapper = frm.get_field("pan_preview").$wrapper;
      var is_viewable = frappe.utils.is_image_file(doc.pan_url);

      frm.toggle_display("upload_documents_section", is_viewable);
      frm.toggle_display("profile_preview", is_viewable);

      if(is_viewable){
        wrapper.html('<div class="img_preview">\
        <img class="img-responsive" src="'+doc.pan_url+'"></img>\
        </div>');
      } else {
        wrapper.empty();
      }
    } else {
      var wrapper = frm.get_field("pan_preview").$wrapper;
      var is_viewable = frappe.utils.is_image_file(doc.pan_url);

      frm.toggle_display("profile_preview", is_viewable);

      if (!is_viewable) {
        wrapper.empty();
      }
    }
  }
});