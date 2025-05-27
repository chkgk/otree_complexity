function predecessor_info_success(units, timeout_seconds) {
    predecessorTransferStatus.innerHTML = "<b>Request successful</b>";
    predecessorTransferUnits.innerHTML = "Inventory: +" + units;
    predecessorInfo.style.backgroundColor = "#648FFF";
    setTimeout(function () {
        predecessorTransferStatus.innerHTML = "";
        predecessorTransferUnits.innerHTML = "";
        predecessorInfo.style.backgroundColor = "";
    }, timeout_seconds * 1000);
}

function predecessor_info_failure(timeout_seconds) {
    predecessorTransferStatus.innerHTML = "<b>Request failed</b>";
    predecessorTransferUnits.innerHTML = "Inventory: No change";
    predecessorInfo.style.backgroundColor = "#FFB000";
    setTimeout(function () {
        predecessorTransferStatus.innerHTML = "";
        predecessorTransferUnits.innerHTML = "";
        predecessorInfo.style.backgroundColor = "";
    }, timeout_seconds * 1000);
}

function successor_info_success(units, cash, timeout_seconds) {
    successorTransferStatus.innerHTML = "<b>Request successful</b>";
    successorTransferUnits.innerHTML = "Inventory: -" + units;
    successorTransferCash.innerHTML = "Balance: +" + cash;
    successorInfo.style.backgroundColor = "#648FFF";
    setTimeout(function () {
        successorTransferStatus.innerHTML = "";
        successorTransferUnits.innerHTML = "";
        successorTransferCash.innerHTML = "";
        successorInfo.style.backgroundColor = "";
    }, timeout_seconds * 1000);
}

function successor_info_failure(timeout_seconds) {
    successorTransferStatus.innerHTML = "<b>Request failed</b>";
    successorTransferUnits.innerHTML = "Inventory: No change";
    successorTransferCash.innerHTML = "Balance: No change";
    successorInfo.style.backgroundColor = "#FFB000";
    setTimeout(function () {
        successorTransferStatus.innerHTML = "";
        successorTransferUnits.innerHTML = "";
        successorTransferCash.innerHTML = "";
        successorInfo.style.backgroundColor = "";
    }, timeout_seconds * 1000);
}

function highlight_successor(transferred, units, cash, timeout_seconds) {
    if (transferred) {
        successor_info_success(units, cash, timeout_seconds);
    } else {
        successor_info_failure(timeout_seconds);
    }
}

function highlight_predecessor(transferred, units, timeout_seconds) {
    if (transferred) {
        predecessor_info_success(units, timeout_seconds);
    } else {
        predecessor_info_failure(timeout_seconds);
    }
}