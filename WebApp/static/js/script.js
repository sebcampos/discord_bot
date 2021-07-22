console.log("Working");

var list_elements = document.getElementById("data-list");

function displayData() {
	d3.json("https://34.102.16.154/json_data", function(data) {
		console.log(data);
	}
}
