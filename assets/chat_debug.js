/**
 * Chat Debug - Help diagnose chat button click issues
 */

function checkChatComponents(label) {
    console.log(`[Chat Debug] ${label} - Checking for chat components...`);

    // Find all chat-related components
    const chatInputs = document.querySelectorAll('[id*="chat-input"]');
    const chatSendBtns = document.querySelectorAll('[id*="chat-send-btn"]');
    const chatMessages = document.querySelectorAll('[id*="chat-messages"]');

    console.log('[Chat Debug] Found components:');
    console.log('  - Chat inputs:', chatInputs.length);
    console.log('  - Send buttons:', chatSendBtns.length);
    console.log('  - Message containers:', chatMessages.length);

    // Log component IDs
    chatSendBtns.forEach((btn, idx) => {
        console.log(`  Button ${idx} ID:`, btn.id);

        // Add manual click listener for debugging (only once)
        if (!btn.dataset.debugListenerAdded) {
            btn.addEventListener('click', function(e) {
                console.log('[Chat Debug] Button clicked!', {
                    id: btn.id,
                    event: e
                });
            });
            btn.dataset.debugListenerAdded = 'true';
        }
    });

    chatInputs.forEach((input, idx) => {
        console.log(`  Input ${idx} ID:`, input.id);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('[Chat Debug] Page loaded');

    // Initial check after page load
    setTimeout(() => {
        checkChatComponents('Initial page load');
    }, 2000);

    // Watch for tab clicks
    setTimeout(() => {
        const tabButtons = document.querySelectorAll('[role="tab"]');
        console.log(`[Chat Debug] Found ${tabButtons.length} tab buttons`);

        tabButtons.forEach(tab => {
            tab.addEventListener('click', function(e) {
                const tabText = tab.textContent || tab.innerText;
                console.log(`[Chat Debug] Tab clicked: ${tabText}`);

                // Check for chat components after tab renders
                setTimeout(() => {
                    checkChatComponents(`After clicking "${tabText}" tab`);
                }, 500);
            });
        });
    }, 2000);

    // Add global function to manually check
    window.checkChatDebug = () => checkChatComponents('Manual check');
    console.log('[Chat Debug] Run window.checkChatDebug() in console to manually check for components');
});

console.log('[Chat Debug] Debug script loaded');
