document.addEventListener('DOMContentLoaded', (event) => {
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
});
