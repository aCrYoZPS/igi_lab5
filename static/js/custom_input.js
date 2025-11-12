custom_input = localStorage.getItem("custom_input");
document.getElementById("deleteInput").addEventListener("click", deleteInput);
document.getElementById("createInput").addEventListener("click", createInput);

if (custom_input != null) {
    custom_input = JSON.parse(custom_input);
    renderInput(custom_input);
}

function validateColor(colorString) {
    const pattern = /^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$/
    return pattern.test(colorString)
}

function createInput() {
    isDisabled = document.getElementById("disabled").checked;
    useList = document.getElementById("useList").checked;
    elementName = document.getElementById("name").value;
    colorValue = document.getElementById("value").value.trim();
    if (!validateColor(colorValue)) {
        errorMsg.textContent = "Please enter a valid color code (e.g., #fff or #ffffff).";
        errorMsg.style.display = "block";
        return;
    }

    errorMsg.textContent = "";
    errorMsg.style.display = "none";
    renderInput({ isDisabled: isDisabled, useList: useList, name: elementName, value: colorValue });
}

function deleteInput() {
    const oldInput = document.getElementById("customInput")
    if (oldInput) {
        oldInput.remove();
    }
}

function renderInput(input) {
    deleteInput();
    const newInput = document.createElement("input");
    newInput.id = "customInput"
    newInput.setAttribute("type", "color");
    newInput.value = input.value;
    newInput.name = input.name;
    if (input.isDisabled) {
        newInput.disabled = true;
    }
    if (input.useList) {
        newInput.setAttribute("list", "colors")
    }

    inputContainer = document.getElementById("inputContainer");
    inputContainer.appendChild(newInput);
    localStorage.setItem("custom_input", JSON.stringify(input));
}
