function currencychart() {
    $.ajax({
      type : 'get',
      url: 'getdataset',
      success: function (resData) {
        var ctx = document.getElementById('currencyset').getContext('2d');
  
        new Chart(ctx, {
          type: 'line',
          data: {
            labels: resData.labels,
            datasets: resData.datasets,
          },
          options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  position: 'bottom',
                  labels: {
                    font: { family: 'Inter', size: 12 }
                  }
                },
                tooltip: {
                  backgroundColor: "rgba(255,255,255,0.9)",
                  titleColor: '#6e707e',
                  bodyColor: "#858796",
                  borderColor: '#dddfeb',
                  borderWidth: 1,
                  padding: 15,
                  displayColors: true,
                  intersect: false,
                  mode: 'index',
                  callbacks: {
                    label: function(context) {
                      let label = context.dataset.label || '';
                      if (label) { label += ': '; }
                      if (context.parsed.y !== null) { 
                        label += '€' + context.parsed.y.toFixed(2);
                      }
                      return label;
                    }
                  }
                }
              },
            scales: {
              x: {
                grid: {
                  display: false,
                },
                ticks: {
                  maxTicksLimit: 7,
                  font: { family: 'Inter' }
                }
              },
              y: {
                beginAtZero: false,
                ticks: {
                  maxTicksLimit: 5,
                  padding: 10,
                  font: { family: 'Inter' },
                  callback: function(value) { return '€' + value.toFixed(2); }
                },
                grid: {
                  color: "rgb(234, 236, 244)",
                  borderDash: [2],
                }
              }
            },
          }
        });
      }
    });
  }
  
$(document).ready(function() {
    currencychart();
});