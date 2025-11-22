let pieChart, lineChart;

async function fetchChartData() {
  try {
    const resp = await fetch('/api/chart-data');
    const data = await resp.json();
    return data;
  } catch (e) {
    console.error("Chart fetch error", e);
    return { pie: {}, line: {} };
  }
}

function renderPie(pie) {
  const ctx = document.getElementById('categoryChart');
  if (!ctx) return;

  if (pieChart) pieChart.destroy();

  pieChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: Object.keys(pie),
      datasets: [{
        data: Object.values(pie),
        backgroundColor: ['#e74c3c','#3498db','#2ecc71','#f1c40f','#9b59b6']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
}

function renderLine(line) {
  const ctx = document.getElementById('trendChart');
  if (!ctx) return;

  if (lineChart) lineChart.destroy();

  lineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: Object.keys(line),
      datasets: [{
        label: 'Amount Spent',
        data: Object.values(line),
        borderColor: '#00cec9',
        backgroundColor: 'rgba(0,236,201,0.12)',
        tension: 0.25,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: { color: '#fff' } },
        y: { ticks: { color: '#fff' } }
      }
    }
  });
}

// Initialize charts
document.addEventListener('DOMContentLoaded', async () => {
  const data = await fetchChartData();
  renderPie(data.pie);
  renderLine(data.line);
});

