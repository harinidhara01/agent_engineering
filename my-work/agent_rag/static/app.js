let currentChatId = null;
let pendingFile = null;
let currentCitations = [];

document.addEventListener('DOMContentLoaded', () => {
    loadChatList();
    loadKnowledgeBase();
    loadTraces();
});

// TAB SWITCHING
function switchTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));

    document.getElementById(`tab-btn-${tabName}`).classList.add('active');
    document.getElementById(`panel-${tabName}`).classList.add('active');

    if (tabName === 'trace') loadTraces();
    if (tabName === 'kb') loadKnowledgeBase();
}

// ASSISTANT CHAT LOGIC
function startNewChat() {
    fetch('/api/chats', { method: 'POST' })
        .then(res => res.json())
        .then(chat => {
            currentChatId = chat.id;
            loadChatList();
            renderEmptyChat();
        });
}

function loadChatList() {
    fetch('/api/chats')
        .then(res => res.json())
        .then(chats => {
            const listEl = document.getElementById('chat-list');
            listEl.innerHTML = '';
            if (chats.length === 0) {
                startNewChat();
                return;
            }
            if (!currentChatId && chats.length > 0) {
                currentChatId = chats[0].id;
            }
            chats.forEach(chat => {
                const li = document.createElement('li');
                li.className = `chat-item ${chat.id === currentChatId ? 'active' : ''}`;
                li.innerHTML = `<i class="fa-regular fa-message"></i> ${chat.title || 'New Conversation'}`;
                li.onclick = () => selectChat(chat.id);
                listEl.appendChild(li);
            });
            if (currentChatId) loadChatMessages(currentChatId);
        });
}

function selectChat(chatId) {
    currentChatId = chatId;
    loadChatList();
    loadChatMessages(chatId);
}

function loadChatMessages(chatId) {
    fetch(`/api/chats/${chatId}/messages`)
        .then(res => res.json())
        .then(messages => {
            const container = document.getElementById('chat-messages');
            container.innerHTML = '';
            if (messages.length === 0) {
                renderEmptyChat();
                return;
            }
            messages.forEach(msg => {
                appendMessageToUI(msg.role, msg.content, msg.citations, msg.trace_id);
            });
            container.scrollTop = container.scrollHeight;
        });
}

function renderEmptyChat() {
    const container = document.getElementById('chat-messages');
    container.innerHTML = `
        <div class="welcome-card">
            <div class="welcome-icon"><i class="fa-solid fa-robot"></i></div>
            <h2>Welcome to Employee Policy Assistant</h2>
            <p>Ask any question about leave policies, travel reimbursements, working hours, benefits, or official state holidays.</p>
        </div>
    `;
}

function useSampleQuestion(qText) {
    document.getElementById('question-input').value = qText;
}

function clearQuestionInput() {
    document.getElementById('question-input').value = '';
}

function sendQuestion() {
    const input = document.getElementById('question-input');
    const question = input.value.trim();
    if (!question) return;

    if (!currentChatId) {
        startNewChat();
        setTimeout(() => sendQuestion(), 300);
        return;
    }

    appendMessageToUI('user', question);
    input.value = '';

    // Typing placeholder
    const typingId = 'typing-' + Date.now();
    const container = document.getElementById('chat-messages');
    const typingBubble = document.createElement('div');
    typingBubble.id = typingId;
    typingBubble.className = 'msg-bubble assistant';
    typingBubble.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Agent searching policy database...';
    container.appendChild(typingBubble);
    container.scrollTop = container.scrollHeight;

    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, chat_id: currentChatId })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById(typingId).remove();
        currentCitations = data.citations || [];
        appendMessageToUI('assistant', data.answer, data.citations, data.trace_id, data.tool_evidence);
        loadChatList();
    })
    .catch(err => {
        document.getElementById(typingId).remove();
        appendMessageToUI('assistant', 'An error occurred while processing your request: ' + err);
    });
}

function appendMessageToUI(role, content, citations = [], traceId = null, toolEvidence = null) {
    const container = document.getElementById('chat-messages');
    // Remove welcome card if present
    const welcome = container.querySelector('.welcome-card');
    if (welcome) welcome.remove();

    const bubble = document.createElement('div');
    bubble.className = `msg-bubble ${role}`;

    let formattedText = content;
    // Format [Citation X] links
    formattedText = formattedText.replace(/\[Citation (\d+)\]/g, (match, p1) => {
        const citeIndex = parseInt(p1) - 1;
        return `<span class="citation-link" onclick="openEvidenceFromCitation('${traceId}', ${citeIndex})">[Citation ${p1}]</span>`;
    });

    bubble.innerHTML = formattedText;
    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
}

// EVIDENCE LOGIC
function openEvidenceFromCitation(traceId, citeIndex) {
    switchTab('evidence');
    fetch(`/api/evidence/${traceId}`)
        .then(res => res.json())
        .then(data => {
            const userBox = document.getElementById('evidence-user-query');
            const assistantBox = document.getElementById('evidence-assistant-resp');
            const rightTitle = document.getElementById('evidence-right-title');
            const badge = document.getElementById('evidence-type-badge');
            const contentBox = document.getElementById('evidence-source-content');

            userBox.innerHTML = `<strong>User Question:</strong><br>${data.user_request}`;
            assistantBox.innerHTML = `<strong>Assistant Answer:</strong><br>${data.final_response}`;

            if (data.agent_decision === 'tool_execution' || data.tool_name === 'regional_holiday_tool') {
                badge.innerText = 'Tool Evidence';
                badge.className = 'badge warning';
                rightTitle.innerHTML = `<i class="fa-solid fa-wrench"></i> Tool Evidence (${data.tool_name})`;
                
                contentBox.innerHTML = `
                    <p><strong>Tool Name:</strong> ${data.tool_name}</p>
                    <p><strong>Input Arguments:</strong> <code>${data.tool_input}</code></p>
                    <div class="highlight-box">
                        <strong>Returned Information / Evidence:</strong>\n${data.tool_output}
                    </div>
                `;
            } else {
                badge.innerText = 'Document Evidence';
                badge.className = 'badge primary';
                rightTitle.innerHTML = `<i class="fa-solid fa-file-contract"></i> Document Evidence`;

                const chunks = JSON.parse(data.retrieved_chunks || '[]');
                const selectedChunk = chunks[citeIndex] || chunks[0];

                if (selectedChunk) {
                    contentBox.innerHTML = `
                        <p><strong>Document:</strong> ${selectedChunk.filename}</p>
                        <p><strong>Page:</strong> ${selectedChunk.page} | <strong>Section:</strong> ${selectedChunk.section}</p>
                        <p><strong>Relevance Similarity Score:</strong> ${selectedChunk.score}</p>
                        <div class="highlight-box">
                            <strong>Retrieved Text Chunk:</strong>\n"${selectedChunk.text}"
                        </div>
                    `;
                } else {
                    contentBox.innerHTML = `<p>No document chunk evidence available for this citation.</p>`;
                }
            }
        });
}

// EXECUTION TRACE LOGIC
function loadTraces() {
    fetch('/api/traces')
        .then(res => res.json())
        .then(traces => {
            const container = document.getElementById('trace-cards-container');
            container.innerHTML = '';

            if (traces.length === 0) {
                container.innerHTML = '<p class="placeholder-text">No execution traces logged yet. Ask a question in the Assistant tab to generate a trace.</p>';
                return;
            }

            traces.forEach(t => {
                const card = document.createElement('div');
                card.className = 'evidence-card';
                card.style.marginBottom = '20px';

                let retrievedOrToolSection = '';
                if (t.agent_decision === 'tool_execution') {
                    retrievedOrToolSection = `
                        <div style="margin-top:10px;">
                            <strong>Tool Calls & Inputs:</strong> <code>${t.tool_name}</code> (${t.tool_input})
                            <div class="highlight-box" style="margin-top:6px; font-size:0.85rem;">
                                <strong>Tool Result:</strong>\n${t.tool_output}
                            </div>
                        </div>
                    `;
                } else {
                    const chunks = JSON.parse(t.retrieved_chunks || '[]');
                    retrievedOrToolSection = `
                        <div style="margin-top:10px;">
                            <strong>Retrieved Documents / Chunks (${chunks.length}):</strong>
                            ${chunks.map(c => `
                                <div class="chunk-card" style="margin-top:6px;">
                                    <strong>Document:</strong> ${c.filename} | <strong>Page:</strong> ${c.page} | <strong>Section:</strong> ${c.section} (Score: ${c.score})<br>
                                    "${c.text}"
                                </div>
                            `).join('')}
                        </div>
                    `;
                }

                card.innerHTML = `
                    <div style="display:flex; justify-content:space-between; border-bottom:1px solid var(--card-border); padding-bottom:8px; margin-bottom:12px;">
                        <div><strong>Trace ID:</strong> <code>${t.id}</code></div>
                        <div><strong>Timestamp:</strong> ${t.created_at}</div>
                        <div><strong>Component:</strong> <span class="badge primary">Agent</span></div>
                        <div><strong>Status:</strong> <span class="badge ${t.status === 'success' ? 'success' : 'danger'}">${t.status}</span></div>
                        <div><strong>Duration:</strong> ${t.duration_ms} ms</div>
                    </div>

                    <div style="margin-bottom:8px;">
                        <strong>User Request:</strong> ${t.user_request}
                    </div>

                    <div style="margin-bottom:8px;">
                        <strong>Path / Decision:</strong> <span class="badge">${t.agent_decision}</span> | 
                        <strong>Gemini Model:</strong> <code>${t.gemini_model}</code>
                    </div>

                    ${retrievedOrToolSection}

                    <div style="margin-top:12px; border-top:1px dashed var(--card-border); padding-top:10px;">
                        <strong>Final Response:</strong>
                        <div style="background:var(--bg-dark); padding:10px; border-radius:6px; margin-top:6px; font-size:0.9rem;">
                            ${t.final_response}
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        });
}

// KNOWLEDGE BASE LOGIC
function loadKnowledgeBase() {
    fetch('/api/documents')
        .then(res => res.json())
        .then(data => {
            document.getElementById('stat-docs-count').innerText = data.documents.length;
            document.getElementById('stat-chunks-count').innerText = data.total_chunks;

            const tbody = document.getElementById('documents-table-body');
            tbody.innerHTML = '';
            data.documents.forEach(doc => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${doc.filename}</strong></td>
                    <td>${doc.file_type}</td>
                    <td>${(doc.file_size / 1024).toFixed(1)} KB</td>
                    <td><span class="badge">${doc.chunk_count} chunks</span></td>
                    <td><code style="font-size:0.75rem">${doc.file_hash.substring(0, 16)}...</code></td>
                    <td>
                        <button class="btn btn-secondary" onclick="viewDocumentChunks('${doc.id}', '${doc.filename}')">
                            <i class="fa-solid fa-list-ul"></i> View Chunks
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        });
}

function handleDocumentUpload(e, replace = false) {
    if (e) e.preventDefault();
    const fileInput = document.getElementById('doc-file-input');
    const file = pendingFile || fileInput.files[0];
    if (!file) return;

    const progress = document.getElementById('upload-progress');
    const statusText = document.getElementById('upload-status-text');
    progress.classList.remove('hidden');
    statusText.innerText = 'Extracting text, chunking & storing vectors...';

    const formData = new FormData();
    formData.append('file', file);
    if (replace) formData.append('replace', 'true');

    fetch('/api/documents/upload', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        progress.classList.add('hidden');
        pendingFile = null;
        if (data.status === 'duplicate') {
            document.getElementById('dup-modal-message').innerText = data.message;
            pendingFile = file;
            document.getElementById('dup-modal').classList.remove('hidden');
        } else if (data.status === 'success') {
            alert(data.message);
            fileInput.value = '';
            loadKnowledgeBase();
        } else {
            alert('Upload error: ' + (data.error || data.message));
        }
    })
    .catch(err => {
        progress.classList.add('hidden');
        alert('Upload failed: ' + err);
    });
}

function cancelDupUpload() {
    pendingFile = null;
    document.getElementById('dup-modal').classList.add('hidden');
}

function confirmReplaceUpload() {
    document.getElementById('dup-modal').classList.add('hidden');
    handleDocumentUpload(null, true);
}

function closeDupModal() {
    document.getElementById('dup-modal').classList.add('hidden');
}

function viewDocumentChunks(docId, filename) {
    fetch(`/api/documents/chunks/${docId}`)
        .then(res => res.json())
        .then(chunks => {
            document.getElementById('modal-doc-title').innerText = `Chunks for ${filename}`;
            const modalBody = document.getElementById('modal-chunks-body');
            modalBody.innerHTML = '';
            chunks.forEach(c => {
                const div = document.createElement('div');
                div.className = 'chunk-card';
                div.innerHTML = `
                    <div style="margin-bottom:6px; color:var(--primary); font-weight:600;">
                        Chunk #${c.chunk_index} | Page ${c.page} | Section: ${c.section}
                    </div>
                    <div>${c.text}</div>
                `;
                modalBody.appendChild(div);
            });
            document.getElementById('chunk-modal').classList.remove('hidden');
        });
}

function closeChunkModal() {
    document.getElementById('chunk-modal').classList.add('hidden');
}
