document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prompt-form');
    const promptInput = document.getElementById('prompt-input');
    const outputDisplay = document.getElementById('output-display');
    const messagesOutput = document.getElementById('messages-output');
    const postsOutput = document.getElementById('posts-output');
    
    // New elements for debugging visibility
    const originalPromptDisplay = document.getElementById('original-prompt-display');
    const transformedPromptDisplay = document.getElementById('transformed-prompt-display');
    const agentLogsDisplay = document.getElementById('agent-logs-display');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const prompt = promptInput.value.trim();
        if (!prompt) {
            showMessage('Please enter a prompt.', 'error');
            return;
        }

        // Clear previous results and show loading state
        clearDisplays();
        showMessage('🤖 AI Agent is processing your request...', 'info');
        
        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt })
            });

            const data = await response.json();
            
            if (response.ok && data.status === 'success') {
                // Display debugging information
                displayPromptComparison(data.original_prompt, data.transformed_prompt);
                displayAgentLogs(data.agent_logs || []);
                displayResult(data.result);
                displayExtractedPosts(data.extracted_posts || []);
                showMessage(data.message || '✅ Processing completed successfully', 'success');
            } else {
                // Handle errors with debugging info
                if (data.original_prompt) {
                    displayPromptComparison(data.original_prompt, data.transformed_prompt || '');
                }
                displayAgentLogs(data.agent_logs || []);
                showMessage(data.error || data.message || '❌ Processing failed', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('❌ Network error occurred. Please try again.', 'error');
        }
    });

    function clearDisplays() {
        outputDisplay.innerHTML = '<code>{}</code>';
        messagesOutput.innerHTML = '';
        postsOutput.innerHTML = '';
        originalPromptDisplay.textContent = '';
        transformedPromptDisplay.textContent = '';
        agentLogsDisplay.innerHTML = '<p class="logs-placeholder">Agent actions will appear here during execution...</p>';
    }

    function displayPromptComparison(originalPrompt, transformedPrompt) {
        originalPromptDisplay.textContent = originalPrompt || '';
        transformedPromptDisplay.textContent = transformedPrompt || originalPrompt || '';
        
        // Add visual indicator if prompt was enhanced
        if (transformedPrompt && transformedPrompt !== originalPrompt) {
            transformedPromptDisplay.classList.add('enhanced');
        }
    }

    function displayAgentLogs(logs) {
        if (!logs || logs.length === 0) {
            agentLogsDisplay.innerHTML = '<p class="logs-placeholder">No agent actions logged yet.</p>';
            return;
        }

        const logsHtml = logs.map((log, index) => {
            const status = log.status || 'unknown';
            const statusClass = status === 'success' ? 'log-success' : 
                               status === 'error' ? 'log-error' : 'log-info';
            
            return `
                <div class="agent-log-entry ${statusClass}">
                    <span class="log-step">Step ${log.step || index + 1}:</span>
                    <span class="log-action">${log.action || 'Unknown action'}</span>
                    <span class="log-details">${formatLogDetails(log)}</span>
                    <span class="log-status">[${status.toUpperCase()}]</span>
                </div>
            `;
        }).join('');

        agentLogsDisplay.innerHTML = logsHtml;
    }

    function formatLogDetails(log) {
        const details = [];
        if (log.url) details.push(`URL: ${log.url}`);
        if (log.query) details.push(`Query: "${log.query}"`);
        if (log.count) details.push(`Count: ${log.count}`);
        if (log.element) details.push(`Element: ${log.element}`);
        
        return details.length > 0 ? `(${details.join(', ')})` : '';
    }

    function displayResult(result) {
        if (!result) return;
        
        try {
            // Try to format as JSON if it's an object/array
            const formatted = typeof result === 'string' ? result : JSON.stringify(result, null, 2);
            outputDisplay.innerHTML = `<code>${escapeHtml(formatted)}</code>`;
        } catch (e) {
            outputDisplay.innerHTML = `<code>${escapeHtml(String(result))}</code>`;
        }
    }

    function displayExtractedPosts(posts) {
        if (!posts || posts.length === 0) {
            postsOutput.innerHTML = '<p class="no-posts">No posts extracted from this request.</p>';
            return;
        }

        const postsHtml = posts.map(post => {
            return `
                <div class="post-card">
                    <div class="post-header">
                        <strong>${escapeHtml(post.author_name || 'Unknown Author')}</strong>
                        ${post.author_url ? `<a href="${escapeHtml(post.author_url)}" target="_blank" class="author-link">Profile</a>` : ''}
                    </div>
                    <div class="post-content">
                        ${escapeHtml(post.content_text || 'No content available')}
                    </div>
                    <div class="post-footer">
                        <span class="post-likes">❤️ ${post.likes_count || 0}</span>
                        <span class="post-time">${escapeHtml(post.posted_timestamp_str || '')}</span>
                        ${post.post_url ? `<a href="${escapeHtml(post.post_url)}" target="_blank" class="post-link">View Post</a>` : ''}
                    </div>
                </div>
            `;
        }).join('');

        postsOutput.innerHTML = `
            <div class="posts-header">
                <h3>📝 Extracted Posts (${posts.length})</h3>
            </div>
            <div class="posts-container">
                ${postsHtml}
            </div>
        `;
    }

    function showMessage(message, type = 'info') {
        const messageClass = `message-${type}`;
        messagesOutput.innerHTML = `<div class="${messageClass}">${escapeHtml(message)}</div>`;
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
