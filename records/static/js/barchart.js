var myChart;

function barchart(filterData) {
  var url = 'getdataset/';
  var data = {};

  if (filterData) {
    url = 'getfiltereddataset/';
    data = filterData;
  }

  console.log('Requesting chart data from:', url);
  console.log('Filter data:', data);

  $.ajax({
    type: 'get',
    url: url,
    data: data,
    success: function (resData) {
      if (myChart) {
        myChart.destroy();
      }

      var ctx = document.getElementById('dataset').getContext('2d');

      myChart = new Chart(ctx, {
        type: 'bar',
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
              callbacks: {
                label: function(context) {
                  let label = context.dataset.label || '';
                  if (label) { label += ': '; }
                  if (context.parsed.y !== null) { 
                    label += '€' + context.parsed.y.toLocaleString();
                  }
                  return label;
                }
              }
            }
          },
          scales: {
            x: {
              stacked: true,
              grid: {
                display: false,
              },
              ticks: {
                 font: { family: 'Inter' }
              }
            },
            y: {
              stacked: true,
              beginAtZero: true,
              ticks: {
                 font: { family: 'Inter' },
                 callback: function(value) { return '€' + value; }
              }
            }
          },
        }
      });
    }
  });
}

$(document).ready(function () {
  barchart();

  $('#filterForm').on('submit', function (e) {
    e.preventDefault();
    var formData = $(this).serialize();
    barchart(formData);
  });
});