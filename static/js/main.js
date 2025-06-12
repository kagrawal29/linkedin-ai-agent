document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prompt-form');
    const input = document.getElementById('prompt-input');
    const commandOutputDisplay = document.getElementById('output-display').querySelector('code');
    const messagesOutput = document.getElementById('messages-output');
    const postsOutput = document.getElementById('posts-output');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const prompt = input.value.trim();

        if (!prompt) {
            alert('Please enter a prompt.');
            return;
        }

        // Clear previous outputs
        commandOutputDisplay.textContent = '{}';
        messagesOutput.innerHTML = '';
        postsOutput.innerHTML = '';

        // Show loading indicator
        const loadingElement = document.createElement('p');
        loadingElement.className = 'loading-message';
        loadingElement.textContent = '🤖 AI Agent is processing your request...';
        messagesOutput.appendChild(loadingElement);

        try {
            const response = await fetch('/api/process', {  // Updated endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

            const data = await response.json();

            // Remove loading indicator
            messagesOutput.removeChild(loadingElement);

            // Display enhanced prompt and results
            if (data.user_prompt && data.enhanced_prompt) {
                const promptInfo = {
                    user_prompt: data.user_prompt,
                    enhanced_prompt: data.enhanced_prompt,
                    status: response.ok ? 'success' : 'error'
                };
                commandOutputDisplay.textContent = JSON.stringify(promptInfo, null, 2);
            } else {
                commandOutputDisplay.textContent = JSON.stringify(data, null, 2);
            }

            // Display error messages
            if (data.error) {
                const errorElement = document.createElement('p');
                errorElement.className = 'error-message';
                errorElement.textContent = `❌ Error: ${data.error}`;
                messagesOutput.appendChild(errorElement);
            } else if (data.results) {
                // Display results - could be string or structured data
                const successElement = document.createElement('p');
                successElement.className = 'success-message';
                
                if (typeof data.results === 'string') {
                    successElement.textContent = `✅ ${data.results}`;
                    messagesOutput.appendChild(successElement);
                } else if (Array.isArray(data.results)) {
                    // Handle structured post data
                    successElement.textContent = `✅ Found ${data.results.length} results:`;
                    messagesOutput.appendChild(successElement);
                    
                    displayPosts(data.results);
                } else {
                    successElement.textContent = `✅ Task completed successfully`;
                    messagesOutput.appendChild(successElement);
                    
                    // Display any structured data
                    const dataElement = document.createElement('pre');
                    dataElement.className = 'result-data';
                    dataElement.textContent = JSON.stringify(data.results, null, 2);
                    postsOutput.appendChild(dataElement);
                }
            }

        } catch (error) {
            // Remove loading indicator if still present
            if (messagesOutput.contains(loadingElement)) {
                messagesOutput.removeChild(loadingElement);
            }
            
            commandOutputDisplay.textContent = `An error occurred: ${error.message}`;
            const errorElement = document.createElement('p');
            errorElement.className = 'error-message';
            errorElement.textContent = `❌ Client-side error: ${error.message}`;
            messagesOutput.appendChild(errorElement);
        }
    });

    // Helper function to display posts
    function displayPosts(posts) {
        if (!posts || posts.length === 0) {
            postsOutput.innerHTML = '<p>No posts found or returned.</p>';
            return;
        }

        posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.className = 'post-item';
            
            // Handle both structured posts and simple objects
            if (post.author_name || post.content_text) {
                // Structured LinkedIn post data
                postElement.innerHTML = `
                    <div class="post-header">
                        <strong>Author:</strong> 
                        ${post.author_url ? `<a href="${post.author_url}" target="_blank">${post.author_name || 'N/A'}</a>` : (post.author_name || 'N/A')}
                        ${post.author_headline ? `<br><small>${post.author_headline}</small>` : ''}
                    </div>
                    <div class="post-content">
                        <strong>Content:</strong> ${post.content_text || 'No content available.'}
                    </div>
                    <div class="post-link">
                        ${post.post_url ? `<a href="${post.post_url}" target="_blank">🔗 View Post on LinkedIn</a>` : ''}
                    </div>
                    <div class="post-stats">
                        👍 ${post.likes_count || 0} | 
                        💬 ${post.comments_count || 0} | 
                        🔄 ${post.reposts_count || 0} | 
                        👁️ ${post.views_count || 0}
                    </div>
                    <div class="post-timestamp">
                        <small>📅 Posted: ${post.posted_timestamp_str || 'N/A'}</small>
                    </div>
                `;
            } else {
                // Simple object or string
                postElement.innerHTML = `<pre>${JSON.stringify(post, null, 2)}</pre>`;
            }
            
            postsOutput.appendChild(postElement);
            postsOutput.appendChild(document.createElement('hr'));
        });
    }
});
