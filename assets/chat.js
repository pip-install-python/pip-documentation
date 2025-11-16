/**
 * Chat Feature - SSE Streaming and UI Updates
 *
 * Handles real-time AI chat with streaming responses
 * using Server-Sent Events (SSE)
 */

// Initialize marked.js for markdown rendering if not already loaded
if (typeof marked === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
    script.async = true;
    document.head.appendChild(script);
}

/**
 * Store for managing active EventSource connections
 * Key: page_name, Value: EventSource instance
 */
window.chatConnections = window.chatConnections || {};

/**
 * Store for tracking session IDs
 * Key: page_name, Value: session_id
 */
window.chatSessions = window.chatSessions || {};

/**
 * Start SSE connection for a chat message
 * This is called after the user and AI placeholder messages are added to the DOM
 */
window.startChatSSE = function(pageId, pagePath, question, viewport) {
    console.log('[Chat SSE] Starting with viewport:', viewport);

    // Get or create session ID (viewport-specific)
    const sessionKey = `chat_session_${pageId}_${viewport}`;
    if (!window.chatSessions[sessionKey]) {
        window.chatSessions[sessionKey] = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    const sessionId = window.chatSessions[sessionKey];

    // Close existing connection if any (viewport-specific)
    const connectionKey = `${pageId}_${viewport}`;
    if (window.chatConnections[connectionKey]) {
        window.chatConnections[connectionKey].close();
    }

    // Build SSE URL
    const baseUrl = window.location.origin;
    const params = new URLSearchParams({
        page: pagePath,
        question: question,
        format: 'markdown',
        session: sessionId
    });
    const sseUrl = `${baseUrl}/api/page-chat-stream?${params.toString()}`;

    // Create EventSource for SSE
    const eventSource = new EventSource(sseUrl);
    window.chatConnections[connectionKey] = eventSource;

    let accumulatedContent = '';
    let suggestions = [];

    // Find the AI message container for this specific viewport
    const findAIMessage = () => {
        // Find all elements with .ai-message-wrapper class
        const allAIWrappers = document.querySelectorAll('.ai-message-wrapper');

        // Filter to find ones that belong to this page AND viewport
        // Check if wrapper is inside a chat-messages container for this page and viewport
        for (let i = allAIWrappers.length - 1; i >= 0; i--) {
            const wrapper = allAIWrappers[i];
            // Find the parent chat-messages container
            const chatMessages = wrapper.closest('[id*="chat-messages"]');
            if (chatMessages &&
                chatMessages.id.includes(`"page":"${pageId}"`) &&
                chatMessages.id.includes(`"viewport":"${viewport}"`)) {
                console.log('[Chat] Found AI message wrapper for page:', pageId, 'viewport:', viewport);
                return wrapper;
            }
        }

        console.warn('[Chat] Could not find AI message wrapper for page:', pageId, 'viewport:', viewport);
        return null;
    };

    eventSource.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            const aiMessageWrapper = findAIMessage();

            if (data.type === 'progress') {
                // Show progress message
                console.log('[Chat Progress]:', data.message || 'Processing...');

            } else if (data.type === 'chunk') {
                // Accumulate markdown chunks
                accumulatedContent += data.content;

                // Update AI message content
                if (aiMessageWrapper) {
                    const contentDiv = aiMessageWrapper.querySelector('.message-content');
                    if (contentDiv) {
                        if (typeof marked !== 'undefined') {
                            contentDiv.innerHTML = marked.parse(accumulatedContent);
                        } else {
                            contentDiv.textContent = accumulatedContent;
                        }

                        // Scroll to bottom
                        const scrollArea = aiMessageWrapper.closest('[id*="chat-area-"]');
                        if (scrollArea) {
                            scrollArea.scrollTop = scrollArea.scrollHeight;
                        }
                    }
                }

            } else if (data.type === 'complete') {
                // Final formatted response
                if (data.formatted && data.formatted.content) {
                    accumulatedContent = data.formatted.content;

                    if (aiMessageWrapper) {
                        const contentDiv = aiMessageWrapper.querySelector('.message-content');
                        if (contentDiv && typeof marked !== 'undefined') {
                            contentDiv.innerHTML = marked.parse(accumulatedContent);
                        }
                    }
                }

            } else if (data.type === 'suggestions') {
                // Section suggestions
                suggestions = data.suggestions || [];
                console.log('[Chat] Section suggestions:', suggestions);

            } else if (data.type === 'done') {
                // Stream complete
                eventSource.close();
                delete window.chatConnections[connectionKey];

                // Remove loader and add suggestions
                if (aiMessageWrapper) {
                    const loader = aiMessageWrapper.querySelector('[class*="Loader"]');
                    if (loader) {
                        loader.remove();
                    }

                    // Add suggestions if available
                    if (suggestions.length > 0) {
                        const aiMessage = aiMessageWrapper.querySelector('.ai-message');
                        if (aiMessage) {
                            const suggestionsDiv = document.createElement('div');
                            suggestionsDiv.className = 'section-suggestions';
                            suggestionsDiv.innerHTML = '<div class="suggestions-title">Related sections:</div>';

                            suggestions.forEach(sug => {
                                const btn = document.createElement('button');
                                btn.className = 'suggestion-btn';
                                btn.textContent = sug.title;
                                btn.onclick = () => {
                                    // Smooth scroll to hash
                                    window.location.hash = sug.hash;
                                    const target = document.querySelector(sug.hash);
                                    if (target) {
                                        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                                    }
                                };
                                suggestionsDiv.appendChild(btn);
                            });

                            aiMessage.appendChild(suggestionsDiv);
                        }
                    }
                }

            } else if (data.type === 'error') {
                // Error occurred
                console.error('[Chat Error]:', data.message);
                eventSource.close();
                delete window.chatConnections[connectionKey];

                if (aiMessageWrapper) {
                    const contentDiv = aiMessageWrapper.querySelector('.message-content');
                    if (contentDiv) {
                        contentDiv.innerHTML = `<div class="error-message">Error: ${data.message}</div>`;
                    }
                }
            }

        } catch (error) {
            console.error('[Chat] Error parsing SSE data:', error, event.data);
        }
    };

    eventSource.onerror = function(error) {
        console.error('[Chat] SSE Error:', error);
        eventSource.close();
        delete window.chatConnections[connectionKey];

        const aiMessageWrapper = findAIMessage();
        if (aiMessageWrapper) {
            const contentDiv = aiMessageWrapper.querySelector('.message-content');
            if (contentDiv) {
                contentDiv.innerHTML = '<div class="error-message">Connection error. Please try again.</div>';
            }
        }
    };
};

/**
 * Smooth scroll to section when hash changes
 */
window.addEventListener('hashchange', function() {
    const hash = window.location.hash;
    if (hash) {
        const target = document.querySelector(hash);
        if (target) {
            setTimeout(() => {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);
        }
    }
});

console.log('[Chat] Client-side chat module loaded successfully');
console.log('[Chat] window.startChatSSE function available:', typeof window.startChatSSE === 'function');