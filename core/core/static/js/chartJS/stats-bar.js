// Bar chart 
function displayBarChart(route, message) {
    // Fetch and promise to the categories point
    fetch(route)
    .then(response => response.json())
    .then(data => {
      // Process the expenses summary dictionary
    // Extract the categories and amounts from the expenses summary dictionary
    const categories = Object.keys(data);
    const amounts = Object.values(data);
    
    // Remove the previous views
    $('.canvas').remove();
    $('.container').append('<canvas id="chart" class="canvas" width="400" height="400"></canvas>');
    
    // Create a chart using Chart.js
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: categories,
        datasets: [{
          label: 'Total '+ message,
          data: amounts,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(201, 203, 207, 0.2)'
          ],
          borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });     
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

  //Doughnut Chart
function displayDoughnutChart(route, message) {
    // Fetch and promise to the categories point
    fetch(route)
    .then(response => response.json())
    .then(data => {
      // Process the expenses summary dictionary
    // Extract the categories and amounts from the expenses summary dictionary
    const categories = Object.keys(data);
    const amounts = Object.values(data);
    
    // Remove the previous views
    $('.canvas').remove();
    $('.container').append('<canvas id="chart" class="canvas" width="400" height="400"></canvas>');
    
    // Create a chart using Chart.js
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: categories,
        datasets: [{
          label: 'Total ' + message,
          data: amounts,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(201, 203, 207, 0.2)'
          ],
          borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });     
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

function  displayPolarChart(route,message) {
    // Fetch and promise to the categories point
    fetch(route)
    .then(response => response.json())
    .then(data => {
      // Process the expenses summary dictionary
    // Extract the categories and amounts from the expenses summary dictionary
    const categories = Object.keys(data);
    const amounts = Object.values(data);
    
    // Remove the previous views
    $('.canvas').remove();
    $('.container').append('<canvas id="chart" class="canvas" width="400" height="400"></canvas>');
    
    // Create a chart using Chart.js
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
      type: 'polarArea',
      data: {
        labels: categories,
        datasets: [{
          label: 'Total ' + message,
          data: amounts,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(201, 203, 207, 0.2)'
          ],
          borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });     
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

