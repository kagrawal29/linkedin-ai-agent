document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prompt-form');
    const input = document.getElementById('prompt-input');
    const outputDisplay = document.getElementById('output-display').querySelector('code');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const prompt = input.value;

        if (!prompt) {
            alert('Please enter a prompt.');
            return;
        }

        try {
            const response = await fetch('/api/parse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

            const data = await response.json();

            if (response.ok) {
                outputDisplay.textContent = JSON.stringify(data, null, 2);
            } else {
                outputDisplay.textContent = JSON.stringify(data, null, 2);
            }
        } catch (error) {
            outputDisplay.textContent = `An error occurred: ${error.message}`;
        }
    });
});
