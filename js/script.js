const votes = {};

const socket = new WebSocket("ws://localhost:8080"); // Adjust the URL as necessary

socket.onmessage = (event) => {
	const data = JSON.parse(event.data);
	if (!votes[data.option]) {
		votes[data.option] = 0;
	}
	votes[data.option]++;
	updateVoteDisplay(data.option);
};

// Initialize a dictionary to store added options and their counts
let optionsDictionary = {};

function addOption(event) {
	event.preventDefault(); // Prevent the default form submission
	const newOption = document.getElementById("new-option").value.trim();

	// Check if the option is unique
	if (newOption === "") {
		alert("Option cannot be empty.");
		return;
	}

	if (votes[newOption]) {
		alert("This option already exists. Please enter a unique option.");
		return;
	}

	// Initialize the vote count for the new option
	votes[newOption] = 0;
	optionsDictionary[newOption] = votes[newOption]; // Save to dictionary
	const optionDiv = document.createElement("div");
	optionDiv.className = "option";
	optionDiv.innerHTML = `
        <span>${newOption}</span>
        <button onclick="vote('${newOption}')">Vote</button>
        <span id="${newOption}-count">0</span>
    `;
	document.getElementById("options").appendChild(optionDiv);
	document.getElementById("new-option").value = ""; // Clear the input field
	updateVotingStats(); // Update the stats table
	updateAddedOptionsList(newOption); // Update the added options list
}

function saveOptions(event) {
	event.preventDefault(); // Prevent the default form submission
	console.log("Saving options:", optionsDictionary); // Log the options dictionary
	alert("Options saved! Check the console for details.");
}

// Optional: Function to clear options if needed
function clearOptions(event) {
	event.preventDefault();
	optionsDictionary = {}; // Clear the dictionary
	votes = {}; // Reset votes
	document.getElementById("options").innerHTML = ""; // Clear displayed options
	document.getElementById("added-options-list").innerHTML = ""; // Clear added options list
	alert("All options cleared!");
}
