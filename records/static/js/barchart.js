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
    success: function (data) {

      ctx = 'dataset';

      if (myChart) {
        myChart.destroy();
      }

      myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels, datasets: data.datasets,
        },
        options: {
          responsive: true,
          legend: {
            position: 'bottom',
          },
          scales: {
            xAxes: [{
              stacked: true,
              gridLines: {
                display: false,
              }
            }],
            yAxes: [{
              stacked: true,
              ticks: {
                beginAtZero: true,
              },
              type: 'linear',
            }]
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