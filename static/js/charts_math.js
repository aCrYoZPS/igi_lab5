let chart = null;
const xValues = [];

(async function() {
    const fValues = [];
    const fTaylorValues = [];
    for (let x = 1.1; x <= 5; x += 0.1) {
        xValues.push(x.toFixed(1));
        fValues.push(f(x));
        fTaylorValues.push(fTaylor(x, 1));
    }
    chart = new Chart(document.getElementById("chart"), {
        type: 'line',
        data: {
            labels: xValues,
            datasets: [
                {
                    label: 'f(x)',
                    data: fValues,
                    borderColor: 'red',
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'fTaylor(x)',
                    data: fTaylorValues,
                    borderColor: 'blue',
                    fill: false,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: { display: true, text: 'x' }
                },
                y: {
                    title: { display: true, text: 'f(x)' }
                }
            }
        }
    });
    // new Chart(
    //     document.getElementById('acquisitions'),
    //     {
    //         type: 'bar',
    //         data: {
    //             labels: data.map(row => row.year),
    //             datasets: [
    //                 {
    //                     label: 'Acquisitions by year',
    //                     data: data.map(row => row.count)
    //                 }
    //             ]
    //         }
    //     }
    // );
})();

const tableBody = document.querySelector("#myTable tbody");
for (let x = 1.1; x <= 3; x += 0.1) {
    let nValues = [1, 5, 10, 50];
    nValues.forEach(n => {
        let row = document.createElement("tr");

        let cellX = document.createElement("td");
        cellX.textContent = x.toFixed(1);

        let cellN = document.createElement("td");
        cellN.textContent = n;

        let fXVal = f(x);
        let fTaylorXVal = fTaylor(x, n);

        let cellFx = document.createElement("td");
        cellFx.textContent = fXVal.toFixed(3);

        let cellFTaylorx = document.createElement("td");
        cellFTaylorx.textContent = fTaylorXVal.toFixed(3);

        let cellEps = document.createElement("td");
        cellEps.textContent = (Math.abs(fXVal - fTaylorXVal))

        row.appendChild(cellX);
        row.appendChild(cellN);
        row.appendChild(cellFx);
        row.appendChild(cellFTaylorx);
        row.appendChild(cellEps);

        tableBody.appendChild(row);
    });
}

function f(x) {
    if (Math.abs(x) < 1) {
        return null;
    }
    return Math.log((x + 1) / (x - 1));
}

function fTaylor(x, n) {
    let res = 0
    for (let i = 0; i < n; ++i) {
        res += 1 / ((2 * i + 1) * Math.pow(x, (2 * i + 1)));
    }

    return 2 * res;
}

document.getElementById('taylorIters').addEventListener('change', function() {
    let n = parseInt(this.value);
    let counter = document.getElementById("iterationNumber");
    counter.innerText = `Number of iterations: ${n}`;
    chart.data.datasets[1].data = xValues.map(x => fTaylor(x, n));
    chart.update();
});
