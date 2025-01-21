// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example for Focal Length Distribution
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Zoom", "Telephoto", "Wide-Angle", "Normal", "Extreme Wide-Angle", "Extreme Telephoto"],
    datasets: [{
      data: [126, 109, 51, 47, 36, 27], // Counts for each focal length
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#f4b619', '#e02d1b', '#6e707e'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var dataset = chart.datasets[tooltipItem.datasetIndex];
          var total = dataset.data.reduce((a, b) => a + b, 0);
          var currentValue = dataset.data[tooltipItem.index];
          var percentage = Math.round((currentValue / total) * 100);
          return chart.labels[tooltipItem.index] + ': ' + currentValue + ' (' + percentage + '%)';
        }
      }
    },
    legend: {
      display: false // 隐藏默认的图表图例
    },
    cutoutPercentage: 80,
  },
});
