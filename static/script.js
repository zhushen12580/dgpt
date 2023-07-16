document.getElementById('linkForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var links = document.getElementById('links').value.split('\n');
    var resultDiv = document.getElementById('result');
    resultDiv.innerHTML = 'Processing...';
    fetch('/processLinks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({links: links})
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerHTML = '';
        for (var i = 0; i < data.results.length; i++) {
            var result = data.results[i];
            resultDiv.innerHTML += '<p><strong>Product:</strong> ' + result.product + '</p>';
            resultDiv.innerHTML += '<p><strong>Rating:</strong> ' + result.rating + '</p>';
            resultDiv.innerHTML += '<p><strong>Reviews:</strong> ' + result.reviews + '</p>';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});