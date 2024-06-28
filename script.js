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
    fetch('plot_info.txt')
        .then(response => response.text())
        .then(data => {
            const infoContent = document.getElementById('info-content');
            infoContent.textContent = data;
        })
        .catch(error => {
            console.error('Error fetching plot info:', error);
        });
});
