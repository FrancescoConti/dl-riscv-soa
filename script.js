document.addEventListener('DOMContentLoaded', (event) => {
    // Fetch and display the plot image
    fetch('plot.png')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.blob();
        })
        .then(blob => {
            const img = document.getElementById('plot');
            img.src = URL.createObjectURL(blob);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });

    // Fetch and display the plot info
    const plotInfoDiv = document.getElementById('plot-info');
    fetch('plot_info.txt')
        .then(response => response.text())
        .then(data => {
            plotInfoDiv.innerHTML = data.replace(/\n/g, '<br>');
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    });
