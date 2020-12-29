const dateTimes = document.querySelectorAll(".published-date");

// date and time localization
dateTimes.forEach(function (element) {
    let utcDate = moment.utc(element.textContent);
    let stillUtc = moment.utc(utcDate).toDate();
    let localDateTime = moment(stillUtc).local().calendar();
    element.innerHTML = localDateTime;
})

let msg = document.querySelector("#alertMessage")
if (msg) {
    msgStyle = msg.style;
    setTimeout(function () {
        (function fade() {
            (msgStyle.opacity -= .1) < 0 ? msgStyle.display = "none" : setTimeout(fade, 100)
        })();
    }, 5000);
}