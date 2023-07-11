// Implementation of asycnhronous JavaScript technices

async function lineChart(endpoint1, endpoint2, message) {
  try {
    const response1 = await fetch(endpoint1);
    const data1 = await response1.json();

    const response2 = await fetch(endpoint2);
    const data2 = await response2.json();

    console.log(data1);
    console.log(data2);
    

    const DATA_COUNT = data1.tags.length;
    const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};


    // Remove the previous views
    $('#chart').remove();
    $('.container').append('<canvas id="chart" width="400" height="400" aria-label="Hello ARIA World" role="img"></canvas>');
    const ctx = document.getElementById('chart').getContext('2d');

    const labels = data1.tags;
    const data = {
      labels: labels,
      datasets: [
        {
          label: 'Expenses',
          data: data1.count,
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',

        },
        {
          label: 'Income',
          data: data2.count,
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
        }
      ]
    };

    new Chart(ctx, 
       {
        type: 'line',
        data: data,
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: message + " records"
            }
          }
        },
    }
  );  

  } catch (error) {
    console.log("error", error);
  }
}


// Implementation of asycnhronous JavaScript technices

async function combinedBarChart(endpoint1, endpoint2, message) {
    try {
      const response1 = await fetch(endpoint1);
      const data1 = await response1.json();
  
      const response2 = await fetch(endpoint2);
      const data2 = await response2.json();
  
      console.log(data1);
      console.log(data2);
      
  
      const DATA_COUNT = data1.tags.length;
      const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};
  
  
      // Remove the previous views
      $('#chart').remove();
      $('.container').append('<canvas id="chart" width="400" height="400" aria-label="Hello ARIA World" role="img"></canvas>');
      const ctx = document.getElementById('chart').getContext('2d');
  
      const labels = data1.tags;
      const data = {
        labels: labels,
        datasets: [
            {
              label: 'Expenses',
              data: data1.count,
              borderColor: 'rgb(255, 99, 132)',
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
    
            },
            {
              label: 'Income',
              data: data2.count,
              borderColor: 'rgb(75, 192, 192)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
            }
        ]
      };
  
      new Chart(ctx, 
         {
            type: 'bar',
            data: data,
            options: {
              responsive: true,
              plugins: {
                legend: {
                  position: 'top',
                },
                title: {
                  display: true,
                  text: message + " records"
                }
              }
            },
      }
    );  
  
    } catch (error) {
      console.log("error", error);
    }
  }
  
  async function radarChart(endpoint1, endpoint2, message) {
    try {
      const response1 = await fetch(endpoint1);
      const data1 = await response1.json();
  
      const response2 = await fetch(endpoint2);
      const data2 = await response2.json();
  
      console.log(data1);
      console.log(data2);
      
  
      const DATA_COUNT = data1.tags.length;
      const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};
  
  
      // Remove the previous views
      $('#chart').remove();
      $('.container').append('<canvas id="chart" width="400" height="400" aria-label="Hello ARIA World" role="img"></canvas>');
      const ctx = document.getElementById('chart').getContext('2d');
  
      const labels = data1.tags;
      const data = {
        labels: labels,
        datasets: [
            {
              label: 'Expenses',
              data: data1.count,
              borderColor: 'rgb(255, 99, 132)',
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
    
            },
            {
              label: 'Income',
              data: data2.count,
              borderColor: 'rgb(75, 192, 192)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
            }
        ]
      };
  
      new Chart(ctx, 
         {
            type: 'radar',
            data: data,
            options: {
              responsive: true,
              plugins: {
                title: {
                  display: true,
                  text: message + ' records'
                }
              }
            }
      }
    );  
  
    } catch (error) {
      console.log("error", error);
    }
  }