// Dashboard Charts
document.addEventListener('DOMContentLoaded', function() {
    // Monthly Trends Chart
    const monthlyCtx = document.getElementById('monthlyChart');
    if (monthlyCtx) {
        const monthsData = JSON.parse(document.getElementById('months-data')?.textContent || '[]');

        new Chart(monthlyCtx, {
            type: 'line',
            data: {
                labels: monthsData.map(item => item.month),
                datasets: [{
                    label: 'Income',
                    data: monthsData.map(item => item.income),
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'Expenses',
                    data: monthsData.map(item => item.expense),
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'Profit',
                    data: monthsData.map(item => item.profit),
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Monthly Financial Trends'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '₹' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    // Department Chart
    const deptCtx = document.getElementById('departmentChart');
    if (deptCtx) {
        const deptData = JSON.parse(document.getElementById('dept-data')?.textContent || '[]');

        new Chart(deptCtx, {
            type: 'doughnut',
            data: {
                labels: deptData.map(item => item.name),
                datasets: [{
                    data: deptData.map(item => (item.total_income || 0) - (item.total_expense || 0)),
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF',
                        '#FF9F40'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }
});
