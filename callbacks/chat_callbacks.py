"""
Chat Callbacks for AI Documentation Assistant

Handles chat interactions using pattern-matching callbacks
to work across all documentation pages.

Version: 2.0 - Fixed callback registration
"""

import dash
from dash import callback, Output, Input, State, MATCH, ctx, html, dcc, clientside_callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("[Chat Callbacks] ========================================")
logger.info("[Chat Callbacks] Initializing chat callbacks module")
logger.info("[Chat Callbacks] ========================================")


# ============================================================================
# Python Callback: Add user message and AI placeholder, trigger SSE
# ============================================================================

@callback(
    Output({"type": "chat-messages", "page": MATCH, "viewport": MATCH}, "children"),
    Output({"type": "chat-send-btn", "page": MATCH, "viewport": MATCH}, "loading"),
    Output({"type": "chat-input", "page": MATCH, "viewport": MATCH}, "value"),
    Output({"type": "chat-sse-trigger", "page": MATCH, "viewport": MATCH}, "data"),  # Store for triggering SSE
    Input({"type": "chat-send-btn", "page": MATCH, "viewport": MATCH}, "n_clicks"),
    State({"type": "chat-input", "page": MATCH, "viewport": MATCH}, "value"),
    State({"type": "chat-messages", "page": MATCH, "viewport": MATCH}, "children"),
    State({"type": "chat-send-btn", "page": MATCH, "viewport": MATCH}, "id"),
    State({"type": "page-path-store", "page": MATCH}, "data"),  # Read actual page path from shared Store
    prevent_initial_call=True
)
def send_message(n_clicks, question, current_children, button_id, page_path):
    """Add user message and AI placeholder to chat, trigger SSE."""
    print(f"[Chat Callbacks] === CALLBACK TRIGGERED === n_clicks={n_clicks}, button_id={button_id}, question='{question}', page_path='{page_path}'")
    logger.info(f"[Chat Callbacks] send_message called: n_clicks={n_clicks}, question={question}, button_id={button_id}, page_path={page_path}")

    if not n_clicks or not question or not question.strip():
        logger.info(f"[Chat Callbacks] Ignoring click - no question or clicks")
        return current_children, False, question or "", dash.no_update

    question = question.strip()

    # Extract page_name and viewport with error handling
    if not button_id:
        logger.error(f"[Chat Callbacks] button_id is None!")
        return current_children, False, question, dash.no_update

    page_name = button_id.get('page')
    viewport = button_id.get('viewport')

    if not page_name:
        logger.error(f"[Chat Callbacks] page_name is None! button_id={button_id}")
        return current_children, False, question, dash.no_update

    if not viewport:
        logger.error(f"[Chat Callbacks] viewport is None! button_id={button_id}")
        return current_children, False, question, dash.no_update

    # Use the actual page_path from the Store (don't reconstruct it)
    if not page_path:
        logger.error(f"[Chat Callbacks] page_path is None! button_id={button_id}")
        return current_children, False, question, dash.no_update

    logger.info(f"[Chat Callbacks] Processing message for page: {page_name}, path: {page_path}")

    # Filter out info message if it exists
    new_messages = []
    if current_children:
        logger.info(f"[Chat Callbacks] Current messages count: {len(current_children)}")
        for i, child in enumerate(current_children):
            has_classname = hasattr(child, 'className')
            classname_val = str(child.className) if has_classname else "NO_CLASSNAME"
            is_info = 'info-message' in classname_val if has_classname else False
            logger.info(f"[Chat Callbacks] Child {i}: has_className={has_classname}, className={classname_val}, is_info={is_info}")

        new_messages = [
            child for child in current_children
            if not (hasattr(child, 'className') and 'info-message' in str(child.className))
        ]
        logger.info(f"[Chat Callbacks] After filtering: {len(new_messages)} messages remaining")

    # Add user message
    user_message = html.Div(
        className="chat-message-wrapper user-message-wrapper",
        children=[
            dmc.Paper(
                className="chat-message user-message elevation-1",
                p="md",
                radius="md",
                withBorder=True,
                children=[
                    dmc.Group(
                        gap="xs",
                        mb="xs",
                        children=[
                            DashIconify(
                                icon="tabler:user",
                                width=20,
                                color="var(--mantine-color-blue-6)"
                            ),
                            dmc.Text(
                                "You",
                                size="sm",
                                fw=600,
                            )
                        ]
                    ),
                    dmc.Text(
                        question,
                        size="sm",
                    )
                ]
            )
        ]
    )

    # Add AI placeholder
    ai_message = html.Div(
        className="chat-message-wrapper ai-message-wrapper",
        children=[
            dmc.Paper(
                className="chat-message ai-message elevation-1",
                p="md",
                radius="md",
                withBorder=True,
                children=[
                    dmc.Group(
                        gap="xs",
                        mb="xs",
                        children=[
                            DashIconify(
                                icon="tabler:robot",
                                width=20,
                                color="var(--mantine-color-teal-6)"
                            ),
                            dmc.Text(
                                "AI Assistant",
                                size="sm",
                                fw=600,
                            )
                        ]
                    ),
                    html.Div(
                        className="message-content",
                        children=[
                            dmc.Loader(
                                size="sm",
                                type="dots"
                            )
                        ]
                    )
                ]
            )
        ]
    )

    new_messages.append(user_message)
    new_messages.append(ai_message)

    # Trigger SSE via dcc.Store update
    sse_trigger = {
        'page_id': page_name,
        'page_path': page_path,
        'question': question,
        'viewport': viewport,
        'timestamp': n_clicks
    }

    return new_messages, False, "", sse_trigger

logger.info("[Chat Callbacks] ✓ Registered send_message callback")

# ============================================================================
# Python Callback: Clear Chat
# ============================================================================

@callback(
    Output({"type": "chat-messages", "page": MATCH, "viewport": MATCH}, "children", allow_duplicate=True),
    Output({"type": "chat-input", "page": MATCH, "viewport": MATCH}, "value", allow_duplicate=True),
    Input({"type": "chat-clear-btn", "page": MATCH, "viewport": MATCH}, "n_clicks"),
    prevent_initial_call=True
)
def clear_chat(n_clicks):
    """Clear chat history and reset to initial state."""
    logger.info(f"[Chat Callbacks] clear_chat called: n_clicks={n_clicks}")

    if not n_clicks:
        return dash.no_update, dash.no_update

    # Return initial welcome message
    initial_message = dmc.Paper(
        [
            dmc.Group(
                [
                    DashIconify(
                        icon="tabler:info-circle",
                        width=20,
                        color="var(--mantine-color-blue-6)"
                    ),
                    dmc.Text(
                        "Ask questions about this documentation page",
                        size="sm",
                        fw=500,
                    ),
                ],
                gap="xs",
            ),
            dmc.Text(
                "Your conversation history will appear here. Use the input below to start chatting.",
                size="xs",
                c="dimmed",
                mt="xs",
            ),
        ],
        p="md",
        withBorder=True,
        radius="md",
        className="elevation-1 info-message",
    )

    return [initial_message], ""

logger.info("[Chat Callbacks] ✓ Registered clear_chat callback")

# ============================================================================
# Clientside Callback: Trigger SSE when store updates
# ============================================================================

clientside_callback(
    """
    function(trigger_data) {
        console.log('[Chat Clientside] Callback triggered:', trigger_data);

        // Don't process if no trigger data
        if (!trigger_data || !trigger_data.question) {
            console.log('[Chat Clientside] Skipping - no trigger data');
            return window.dash_clientside.no_update;
        }

        const page_name = trigger_data.page_id;
        const page_path = trigger_data.page_path;
        const question = trigger_data.question;
        const viewport = trigger_data.viewport;

        console.log('[Chat Clientside] Starting SSE for:', {page_name, page_path, question, viewport});

        // Retry mechanism to wait for chat.js to load
        function tryStartSSE(retries = 0, maxRetries = 10) {
            if (typeof window.startChatSSE === 'function') {
                console.log('[Chat] startChatSSE function found, starting chat...');
                window.startChatSSE(page_name, page_path, question, viewport);
            } else if (retries < maxRetries) {
                const delay = Math.min(100 * Math.pow(2, retries), 2000); // Exponential backoff, max 2s
                console.log(`[Chat] Waiting for startChatSSE (attempt ${retries + 1}/${maxRetries}, delay: ${delay}ms)...`);
                setTimeout(() => tryStartSSE(retries + 1, maxRetries), delay);
            } else {
                console.error('[Chat] startChatSSE function not found after', maxRetries, 'retries. chat.js may not have loaded.');
            }
        }

        tryStartSSE();

        return window.dash_clientside.no_update;
    }
    """,
    Output({"type": "chat-sse-trigger", "page": MATCH, "viewport": MATCH}, "storage_type"),  # Dummy output
    Input({"type": "chat-sse-trigger", "page": MATCH, "viewport": MATCH}, "data"),  # Watch trigger Store updates
    prevent_initial_call=True
)

logger.info("[Chat Callbacks] ✓ Registered clientside SSE trigger callback")
logger.info("[Chat Callbacks] ========================================")
logger.info("[Chat Callbacks] All callbacks registered successfully!")
logger.info("[Chat Callbacks] ========================================")

print("[Chat Callbacks] Loaded chat callbacks module")