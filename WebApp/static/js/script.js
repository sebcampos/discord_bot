console.log("Working");

var list_elements = document.getElementById("data-list");
var data = d3.json("../data/json_data/data.js");

function displayData() {
    for (var i = 0; len = list_elements.length; i++) {
        console.log(list_elements[i])
    }
}