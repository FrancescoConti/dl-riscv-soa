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

            // Function to handle clicks on plot points
            window.addEventListener('message', function(event) {
                if (event.data.type === 'plotly_click') {
                    const pointIndex = event.data.pointIndex;
                    table.rows().deselect();  // Deselect any previously selected rows
                    table.row(pointIndex).select();  // Select the clicked row
                }
            }, false);

            // Function to handle table search and highlight plot points
            $('#data-table').on('search.dt', function() {
                const searchTerm = $('.dataTables_filter input').val().toLowerCase();
                const highlightedIds = table.rows({ search: 'applied' }).data().map(row => row.id);

                const plotIframe = document.getElementById('plot-frame');
                plotIframe.contentWindow.postMessage({ type: 'highlight_points', ids: highlightedIds }, '*');
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
});
