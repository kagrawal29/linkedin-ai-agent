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

        try {
            const response = await fetch('/api/process_prompt_and_fetch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

            const data = await response.json();

            // Display command output
            if (data.command) {
                commandOutputDisplay.textContent = JSON.stringify(data.command, null, 2);
            } else {
                commandOutputDisplay.textContent = JSON.stringify(data, null, 2); // Fallback for old structure or errors
            }

            // Display error messages
            if (data.error) {
                const errorElement = document.createElement('p');
                errorElement.className = 'error-message'; // For styling
                errorElement.textContent = data.error;
                messagesOutput.appendChild(errorElement);
            } else if (data.harvester_message) { // Display harvester messages if no error
                const messageElement = document.createElement('p');
                messageElement.className = 'info-message'; // For styling
                messageElement.textContent = data.harvester_message;
                messagesOutput.appendChild(messageElement);
            }

            // Display fetched posts
            if (data.posts_data && Array.isArray(data.posts_data)) {
                if (data.posts_data.length === 0) {
                    postsOutput.innerHTML = '<p>No posts found or returned.</p>';
                } else {
                    data.posts_data.forEach(post => {
                        const postElement = document.createElement('div');
                        postElement.className = 'post-item'; // For styling
                        // Sanitize content before injecting as HTML if it comes from user input or external sources
                        // For now, assuming data from our backend is safe or will be simple text.
                        postElement.innerHTML = `
                            <p>
                                <strong>Author:</strong> 
                                ${post.author_url ? `<a href="${post.author_url}" target="_blank">${post.author_name || 'N/A'}</a>` : (post.author_name || 'N/A')}
                                (${post.author_headline || 'N/A'})
                            </p>
                            <p><strong>Content:</strong> ${post.content_text || 'No content available.'}</p>
                            <p>${post.post_url ? `<a href="${post.post_url}" target="_blank">View Post on LinkedIn</a>` : 'No post URL'}</p>
                            <p>
                                Likes: ${post.likes_count !== null ? post.likes_count : 'N/A'} |
                                Comments: ${post.comments_count !== null ? post.comments_count : 'N/A'} |
                                Reposts: ${post.reposts_count !== null ? post.reposts_count : 'N/A'} |
                                Views: ${post.views_count !== null ? post.views_count : 'N/A'}
                            </p>
                            <p><small>Posted: ${post.posted_timestamp_str || 'N/A'}</small></p>
                        `;
                        postsOutput.appendChild(postElement);
                        postsOutput.appendChild(document.createElement('hr'));
                    });
                }
            } else if (data.command && data.command.engagement_type && data.command.engagement_type.includes('fetch_posts') && !data.error) {
                // If it was a fetch_posts command but posts_data is null/undefined and no error, imply no posts found
                postsOutput.innerHTML = '<p>No posts data received, though it was a fetch command.</p>';
            }

        } catch (error) {
            commandOutputDisplay.textContent = `An error occurred: ${error.message}`;
            const errorElement = document.createElement('p');
            errorElement.className = 'error-message';
            errorElement.textContent = `Client-side error: ${error.message}`;
            messagesOutput.appendChild(errorElement);
        }
    });
});
