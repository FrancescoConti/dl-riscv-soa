document.addEventListener('DOMContentLoaded', (event) => {
    const plotContainer = document.getElementById('static-plot-container');
    const plotInfoDiv = document.getElementById('plot-info');
    
    // Fetch and display the plot image
    const img = document.createElement('img');
    img.id = 'plot';
    img.alt = 'Generated Plot';
    fetch('plot.png')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.blob();
        })
        .then(blob => {
            img.src = URL.createObjectURL(blob);
            plotContainer.appendChild(img);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });

    // Fetch and display the table.html content
    fetch('table.html')
        .then(response => response.text())
        .then(data => {
            plotInfoDiv.innerHTML = data;
            // Initialize DataTables
            const table = new DataTable('#data-table', {
                pageLength: 100,
                order: [],
                dom: 'Bfrtip',
                select: true
            });

        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
});
