// Copyright (c) 2021, yashwanth and contributors
// For license information, please see license.txt

var day_of_week = {
	1:'Sunday',
	2:'Monday',
	3:'Tuesday',
	4:'Wednesday',
	5:'Thursday',
	6:'Friday',
	7:'Saturday'
 }
var move_day = 6

frappe.ui.form.on('FoundryApp Settings','weekly_planning_cycle_begins_on', function(frm, cdt, cdn) {
var weekly_settings = locals[cdt][cdn]
for (const [key, value] of Object.entries(day_of_week)) {
var c_day = day_of_week[key]
var cur_day = weekly_settings.weekly_planning_cycle_begins_on

if (c_day === cur_day) {
var set = move_day + parseInt(key)
if (set > Object.keys(day_of_week).length) {
var new_set = set - Object.keys(day_of_week).length
var change_day = day_of_week[new_set]

change_value(weekly_settings.doctype, change_day, c_day, frm)

}
if (set == Object.keys(day_of_week).length) {
change_value(weekly_settings.doctype, day_of_week[set], c_day, frm)
}
}
}
});

frappe.ui.form.on('FoundryApp Settings','weekly_planning_cycle_ends_on', function(frm, cdt, cdn) {
var weekly_settings = locals[cdt][cdn]
for (const [key, value] of Object.entries(day_of_week)) {
var c_day = day_of_week[key]
var cur_day = weekly_settings.weekly_planning_cycle_ends_on
if (c_day === cur_day) {
var set = parseInt(key) - move_day
if (set <= 0) {
var new_set = set + Object.keys(day_of_week).length
var change_day = day_of_week[new_set]

change_value(weekly_settings.doctype,c_day, change_day, frm)

}
if (set == 1) {
change_value(weekly_settings.doctype,c_day, day_of_week[set], frm)
}
}
}
});

function change_value(name,cw_day, cc_day, frm) {
frappe.call({
method: 'frappe.client.set_value',
args: {
'doctype': name,
'name': name,
'fieldname': {
'weekly_planning_cycle_ends_on': cw_day,
'weekly_planning_cycle_begins_on': cc_day
},
async: false,
callback: function(r) {
console.log("callback")
frm.reload_doc()
}
}
})
}