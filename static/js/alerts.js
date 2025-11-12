let dateString = prompt("Please enter your birth date:", "yyyy-mm-dd");

let date = parseDateStrict(dateString)

let age = calculateAge(date)

if (age > 18) {
    alert(`Your birthday was on ${getWeekdayName(date)}`);
}
else {
    alert("Вам меньше восемнадцати! Покиньте этот богомерзкий сайт ради своего же блага!");
}

function getWeekdayName(date, locale = 'en-US') {
    return date.toLocaleDateString(locale, { weekday: 'long' });
}

function calculateAge(birthDate) {
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();

    const monthDiff = today.getMonth() - birthDate.getMonth();
    const dayDiff = today.getDate() - birthDate.getDate();
    if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
        age--;
    }

    return age;
}

function parseDateStrict(input) {
    const pattern = /^\d{4}-\d{2}-\d{2}$/;
    if (!pattern.test(input)) {
        alert("Invalid date format");
        return null;
    }
    const [year, month, day] = input.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    if (
        date.getFullYear() === year &&
        date.getMonth() === month - 1 &&
        date.getDate() === day
    ) {
        if (date > new Date()) {
            alert("Invalid date: provided date is after today");
            return null;
        }

        return date;
    }


    alert("Invalid date: provided date is invalid");
    return null;
}
