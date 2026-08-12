// Chart.js Dashboard Charts Initialization

document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('weeklyProgressChart');
    if (!ctx) return;

    fetch('/api/progress-chart')
        .then(response => response.json())
        .then(data => {
            new Chart(ctx.getContext('2d'), {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Reading',
                            data: data.reading,
                            borderColor: '#4f46e5',
                            backgroundColor: 'rgba(79, 70, 229, 0.1)',
                            tension: 0.4,
                            fill: true
                        },
                        {
                            label: 'Listening',
                            data: data.listening,
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            tension: 0.4,
                            fill: true
                        },
                        {
                            label: 'Writing',
                            data: data.writing,
                            borderColor: '#f59e0b',
                            backgroundColor: 'rgba(245, 158, 11, 0.1)',
                            tension: 0.4,
                            fill: true
                        },
                        {
                            label: 'Speaking',
                            data: data.speaking,
                            borderColor: '#ef4444',
                            backgroundColor: 'rgba(239, 68, 68, 0.1)',
                            tension: 0.4,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            min: 4.0,
                            max: 9.0,
                            ticks: { stepSize: 0.5 }
                        }
                    },
                    plugins: {
                        legend: { position: 'top' }
                    }
                }
            });
        })
        .catch(err => console.error("Error fetching progress chart data:", err));
});
