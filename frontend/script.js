document.getElementById('submit-btn').addEventListener('click', () => {
    const code = document.getElementById('code').value;
    const language = document.getElementById('language').value;
    const resultsDiv = document.getElementById('results');

    resultsDiv.innerHTML = 'Analyzing...';

    fetch('http://127.0.0.1:8000/api/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code, language }),
    })
    .then(response => response.json())
    .then(data => {
        resultsDiv.innerHTML = formatResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        resultsDiv.innerHTML = 'An error occurred while analyzing the code.';
    });
});

function formatResults(data) {
    let html = '<h3>Bugs:</h3>';
    if (data.bugs && data.bugs.length > 0) {
        html += '<ul>';
        data.bugs.forEach(bug => {
            html += `<li>Line ${bug.line}: ${bug.description}</li>`;
        });
        html += '</ul>';
    } else {
        html += '<p>No bugs found.</p>';
    }

    html += '<h3>Explanation:</h3>';
    html += `<p>${data.explanation}</p>`;

    html += '<h3>Fix Suggestions:</h3>';
    if (data.fix_suggestions && data.fix_suggestions.length > 0) {
        data.fix_suggestions.forEach(fix => {
            html += `<h4>${fix.description}</h4>`;
            html += `<pre><code>${escapeHtml(fix.code)}</code></pre>`;
        });
    } else {
        html += '<p>No fix suggestions available.</p>';
    }

    html += '<h3>Optimized Code:</h3>';
    html += `<pre><code>${escapeHtml(data.optimized_code)}</code></pre>`;

    return html;
}

function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}
