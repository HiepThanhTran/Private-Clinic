//Table choosing in analytics.html
const salesBtn = document.querySelector(".salesBtn");
const medicineBtn = document.querySelector(".medicineBtn");
const salesChart = document.querySelector(".sales__chart");
const medicineChart = document.querySelector(".medicine__chart");
const salesTable = document.querySelector(".sales__table");
const medicineTable = document.querySelector(".medicine__table");

salesBtn.addEventListener('click', function () {
    salesBtn.classList.add("is__choose");
    salesChart.style.display = "block";
    salesTable.style.display = "block";
    medicineChart.style.display = "none";
    medicineTable.style.display = "none";
    medicineBtn.classList.remove("is__choose");
})

medicineBtn.addEventListener('click', function () {
    salesBtn.classList.remove("is__choose");
    salesChart.style.display = "none";
    salesTable.style.display = "none";
    medicineChart.style.display = "block";
    medicineTable.style.display = "block";
    medicineBtn.classList.add("is__choose");
})

let colors = []
let borderColors = []
const generateRandomColor = () => {
    let r = Math.random() * 255
    let g = Math.random() * 255
    let b = Math.random() * 255
    return {
        color: `rgba(${r}, ${g}, ${b}, 0.2)`,
        borderColor: `rgba(${r}, ${g}, ${b}, 1)`
    }
}

const generateChart = (ctx, type, label, labels, data) => {
    return new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderWidth: 1,
                backgroundColor: colors,
                borderColor: borderColors,
            }]
        },
    })
}

window.onload = (event) => {
    const medicineChart = document.getElementById('medicine__chart')
    chart = generateChart(medicineChart, 'bar', 'Statistics on frequency of drug use by month', medicineLabels, medicineData)

    const loadMedicineStatsTable = (data) => {
        const medicineStatsTable = document.getElementById('medicine-stats-table')
        const medicineStatsTableBody = medicineStatsTable.querySelector('tbody')
        const rowsToDelete = document.getElementsByClassName('medicine-stats-row')
        medicineLabels = []
        medicineData = []
        colors = []
        borderColors = []

        while (rowsToDelete.length > 0) rowsToDelete[0].remove()

        for (let i = 0; i < data.length; i++) {
            const newRow = document.createElement('tr')
            newRow.classList.add('medicine-stats-row')
            newRow.innerHTML = `<td>${i + 1}</td>
                                        <td>${data[i].medicine_name}</td>
                                        <td>${data[i].unit_name}</td>
                                        <td>${data[i].amount}</td>
                                        <td>${data[i].usage_count}</td>`
            medicineStatsTableBody.appendChild(newRow)

            medicineLabels.push(data[i].medicine_name)
            medicineData.push(data[i].usage_count)

            let medicineColor = generateRandomColor()
            colors.push(medicineColor.color)
            borderColors.push(medicineColor.borderColor)
        }
    }

    const medicineStatsMonth = document.getElementById('medicine_stats_month')
    medicineStatsMonth.addEventListener('change', (e) => {
        showPreLoading()

        fetch('/api/authentication/load-chart-stats-medicine-by-month', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'month': e.target.value.toString(),
            })
        }).then(response => response.json())
            .then(data => {
                loadMedicineStatsTable(data, chart, medicineChart)
                if (chart)
                    chart.destroy()
                medicineChart.style.display = 'block'
                chart = generateChart(medicineChart, 'bar', 'Statistics on frequency of drug use by month', medicineLabels, medicineData)
            })
            .catch(error => {
                console.log(error)
            })
            .finally(() => {
                hidePreLoading()
            })
    })

    const medicineSearchForm = document.getElementById('medicine-search-form')
    medicineSearchForm.addEventListener('submit', (e) => {
        e.preventDefault()
        showPreLoading()

        const searchInput = document.querySelector('.search__table')

        fetch('/api/authentication/load-chart-stats-medicine-by-month', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'medicine_name': searchInput.value.toString(),
            })
        }).then(response => response.json())
            .then(data => {
                loadMedicineStatsTable(data)
                if (chart)
                    chart.destroy()
                medicineChart.style.display = 'block'
                chart = generateChart(medicineChart, 'bar', 'Statistics on frequency of drug use by month', medicineLabels, medicineData)
            })
            .catch(error => {
                console.log(error)
            })
            .finally(() => {
                hidePreLoading()
            })
    })
}