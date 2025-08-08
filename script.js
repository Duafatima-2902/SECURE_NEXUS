function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
    };
    return text.replace(/[&<>"']/g, function (m) { return map[m]; });
}

function formatMarkdownText(text) {
    // Escape HTML special chars first
    let escaped = escapeHtml(text);

    // Convert markdown elements to HTML:

    // Code blocks ```python ... ```
    escaped = escaped.replace(/```(.*?)```/gs, (match, code) => {
        return `<pre class="code-block">${code.trim()}</pre>`;
    });

    // Bold **text**
    escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Lists - lines starting with -
    escaped = escaped.replace(/(^|\n)- (.*)/g, '$1<ul><li>$2</li></ul>');
    // Combine multiple <ul> tags into one
    escaped = escaped.replace(/<\/ul>\n<ul>/g, '');

    // Convert new lines to <br>
    escaped = escaped.replace(/\n/g, '<br>');

    return escaped;
}

async function runAnalysis(type) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "Running test... please wait.";

    let url = "";
    let body = {};

    if (type === "code") {
        const code = document.getElementById("codeInput").value.trim();
        if (!code) {
            resultDiv.innerHTML = "Please paste some code first.";
            return;
        }
        url = "/analyze";
        body = { code: code };

    } else if (type === "phishing") {
        const message = document.getElementById("phishingInput").value.trim();
        if (!message) {
            resultDiv.innerHTML = "Please paste the email or message.";
            return;
        }
        url = "/phishing-check";
        body = { message: message };

    } else if (type === "web") {
        const urlInput = document.getElementById("webInput").value.trim();
        if (!urlInput) {
            resultDiv.innerHTML = "Please enter a website URL.";
            return;
        }
        url = "/scan-web";
        body = { url: urlInput };

    } else {
        resultDiv.innerHTML = "Invalid test type.";
        return;
    }

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            resultDiv.innerHTML = `Error: ${response.status} ${response.statusText}`;
            return;
        }

        const data = await response.json();

        // Extract the relevant text based on type
        let textToFormat = "";

        if (type === "code" && data.analysis) {
            textToFormat = data.analysis;
        } else if (type === "phishing" && data.result) {
            textToFormat = data.result;
        } else if (type === "web" && data.alerts) {
            textToFormat = JSON.stringify(data.alerts, null, 2);
        } else if (data.error) {
            textToFormat = "Error: " + data.error;
        } else {
            textToFormat = JSON.stringify(data, null, 2);
        }

        resultDiv.innerHTML = `<h3>Result:</h3>${formatMarkdownText(textToFormat)}`;
    } catch (error) {
        resultDiv.innerHTML = "Request failed: " + error.message;
    }
}
