let dates = [];

function validateDate(month, day) {
    let months = {
        январь: 31,
        февраль: 28,
        март: 31,
        апрель: 30,
        май: 31,
        июнь: 30,
        июль: 31,
        август: 31,
        сентябрь: 30,
        октябрь: 31,
        ноябрь: 30,
        декабрь: 31,
    };

    if (!(month.toLowerCase() in months)) {
        return false;
    }

    if (+day > months[month]) {
        return false;
    }

    return true;
}

class BaseDate {
    constructor() {
    }

    getMonth(date) {
        return date.month;
    }

    setMonth(date, month) {
        date.month = month;
    }

    getDay(date) {
        return date.day;
    }

    setDay(date, day) {
        date.day = day;
    }

    addDateFromForm(month, day) {
        dates.push({ month: month.toLowerCase(), day: +day });
    }

    showAllDates() {
        const el = document.getElementById("dateList");
        el.innerHTML = "";
        dates.forEach((d) => {
            el.innerHTML += `<li>${d.month} ${d.day}</li>`;
        });
    }

    showResult() {
        const summerMonths = ["июнь", "июль", "август"];
        const winterMonths = ["декабрь", "январь", "февраль"];
        const summerDates = dates.filter(d => summerMonths.includes(d.month));
        const winterDates = dates.filter(d => winterMonths.includes(d.month));

        const summerStr = summerDates.map(d => `${d.month} ${d.day}`).join(", ");
        const winterStr = winterDates.map(d => `${d.month} ${d.day}`).join(", ");

        const res = `Летние даты: ${summerStr || "Нет"}\nЗимние даты: ${winterStr || "Нет"}`;
        document.getElementById("result").textContent = res;
    }
}

class ExtendedDate extends BaseDate {
    constructor() {
        super();
    }

    addDateFromForm(month, day, comment) {
        if (!validateDate(month, day)) {
            alert("Неверная дата");
        }
        else {
            dates.push({ month: month.toLowerCase(), day: +day, comment: comment });
        }
    }

    showAllDates() {
        const el = document.getElementById("dateList");
        el.innerHTML = "";
        dates.forEach((d) => {
            el.innerHTML += `<li>${d.month} ${d.day} ${d.comment ? "- " + d.comment : ""}</li>`;
        });
    }
}

const dateManager = new ExtendedDate();

document.getElementById("addButton").addEventListener("click", function() {
    const m = document.getElementById("month").value.trim();
    const d = document.getElementById("day").value;
    const c = document.getElementById("comment").value.trim();
    dateManager.addDateFromForm(m, d, c);
    dateManager.showAllDates();
});

document.getElementById("showResult").onclick = function() {
    dateManager.showResult();
};
