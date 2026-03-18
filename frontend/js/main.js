/**
 * NeuroAgent Main Application
 * Updated with model selection support
 */

class NeuroAgentApp {
    constructor() {
        this.chatHistory = [];
        this.uploadedFileId = null;
        this.temperature = 0.7;
        this.maxTokens = 1024;
        this.isLoading = false;

        this.initializeElements();
        this.setupEventListeners();
        this.loadSettings();
        this.updateAgentStats();
        
        // Refresh agent stats every 5 seconds
        setInterval(() => this.updateAgentStats(), 5000);
    }

    /**
     * Initialize DOM elements
     */
    initializeElements() {
        this.messagesContainer = document.getElementById('messages');
        this.inputTextarea = document.getElementById('input-textarea');
        this.sendBtn = document.getElementById('send-btn');
        this.clearBtn = document.getElementById('clear-btn');
        this.charCount = document.getElementById('char-count');
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.uploadZone = document.getElementById('upload-zone');
        this.pdfInput = document.getElementById('pdf-input');
        this.uploadStatus = document.getElementById('upload-status');
        this.temperatureSlider = document.getElementById('temperature');
        this.temperatureValue = document.getElementById('temp-value');
        this.maxTokensInput = document.getElementById('max-tokens');
        this.messageCount = document.getElementById('message-count');
        this.responseTime = document.getElementById('response-time');
        this.tokensUsed = document.getElementById('tokens-used');
        this.lastAgent = document.getElementById('last-agent');
        this.welcomeMessage = document.getElementById('welcome');
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.inputTextarea.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        this.inputTextarea.addEventListener('input', () => this.updateCharCount());
        this.clearBtn.addEventListener('click', () => this.clearChat());

        // PDF Upload
        this.uploadZone.addEventListener('click', () => this.pdfInput.click());
        this.uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadZone.style.borderColor = 'var(--accent-cyan)';
        });
        this.uploadZone.addEventListener('dragleave', () => {
            this.uploadZone.style.borderColor = 'var(--accent-cyan)';
        });
        this.uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadZone.style.borderColor = 'var(--accent-cyan)';
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handlePDFUpload(files[0]);
            }
        });
        this.pdfInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handlePDFUpload(e.target.files[0]);
            }
        });

        // Settings
        this.temperatureSlider.addEventListener('input', (e) => {
            this.temperature = parseFloat(e.target.value);
            this.temperatureValue.textContent = this.temperature.toFixed(1);
            localStorage.setItem('temperature', this.temperature);
        });
        this.maxTokensInput.addEventListener('change', (e) => {
            this.maxTokens = parseInt(e.target.value);
            localStorage.setItem('maxTokens', this.maxTokens);
        });
    }

    /**
     * Load settings from localStorage
     */
    loadSettings() {
        const savedTemp = localStorage.getItem('temperature');
        if (savedTemp) {
            this.temperature = parseFloat(savedTemp);
            this.temperatureSlider.value = this.temperature;
            this.temperatureValue.textContent = this.temperature.toFixed(1);
        }

        const savedTokens = localStorage.getItem('maxTokens');
        if (savedTokens) {
            this.maxTokens = parseInt(savedTokens);
            this.maxTokensInput.value = this.maxTokens;
        }
    }

    /**
     * Update character count
     */
    updateCharCount() {
        const length = this.inputTextarea.value.length;
        this.charCount.textContent = `${length} / 5000`;
    }

    /**
     * Handle PDF upload
     */
    async handlePDFUpload(file) {
        if (!file.type.includes('pdf')) {
            this.showUploadStatus('Invalid file type. Please upload a PDF.', false);
            return;
        }

        this.showUploadStatus('Uploading...', true);
        this.loadingOverlay.classList.add('active');

        try {
            const result = await api.uploadPDF(file);
            this.uploadedFileId = result.file_id;
            this.showUploadStatus(`✅ PDF uploaded: ${result.filename}`, true);
            setTimeout(() => {
                this.uploadStatus.style.display = 'none';
                this.uploadZone.innerHTML = `<div class="upload-icon">✅</div><p>${result.filename}</p>`;
            }, 2000);
        } catch (error) {
            this.showUploadStatus(`❌ Upload failed: ${error.message}`, false);
        } finally {
            this.loadingOverlay.classList.remove('active');
        }
    }

    /**
     * Show upload status
     */
    showUploadStatus(message, success) {
        this.uploadStatus.style.display = 'block';
        this.uploadStatus.textContent = message;
        this.uploadStatus.style.color = success ? 'var(--success)' : 'var(--error)';
    }

    /**
     * Send message with selected model
     */
    async sendMessage() {
        const query = this.inputTextarea.value.trim();
        if (!query) return;

        if (this.isLoading) return;
        this.isLoading = true;

        // Remove welcome message on first message
        if (this.welcomeMessage) {
            this.welcomeMessage.style.display = 'none';
        }

        // Add user message to chat
        this.addMessage(query, 'user', 'You');

        // Clear input
        this.inputTextarea.value = '';
        this.updateCharCount();

        // Show loading
        this.loadingOverlay.classList.add('active');

        const startTime = Date.now();

        try {
            // Add to chat history
            this.chatHistory.push({
                role: 'user',
                content: query
            });

            // Get selected model
            let selectedModel = "llama-3.3-70b-versatile";
            let modelName = "Llama 3.3";

if (typeof modelManager !== "undefined") {
    selectedModel = modelManager.getSelectedModel();
    modelName = modelManager.getModelName(selectedModel);
}

            // Send to API with model selection
            const response = await api.sendMessage(
                query,
                this.chatHistory,
                this.uploadedFileId,
                this.temperature,
                this.maxTokens,
                selectedModel  // Pass selected model to API
            );

            const processingTime = Date.now() - startTime;

            // Add assistant message with model info
            this.addMessage(
                response.response, 
                'assistant', 
                `${response.source || 'Assistant'} [${modelName}]`
            );

            // Add to chat history
            this.chatHistory.push({
                role: 'assistant',
                content: response.response
            });

            // Update stats
            this.updateStats(response, processingTime);

            // Update agent manager
            if (response.agent_used) {
                agentManager.updateFromResponse(response.agent_used);
            }

        } catch (error) {
            this.addMessage(`Error: ${error.message}`, 'assistant', 'Error');
        } finally {
            this.isLoading = false;
            this.loadingOverlay.classList.remove('active');
            this.inputTextarea.focus();
        }
    }

    /**
     * Add message to chat
     */
    addMessage(content, role, source) {
        const messageEl = document.createElement('div');
        messageEl.className = `message ${role}`;

        const avatar = role === 'user' ? '👤' : '🤖';
        
        messageEl.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                ${content}
                ${role === 'assistant' && source ? `<div class="message-source">📍 ${source}</div>` : ''}
            </div>
        `;

        this.messagesContainer.appendChild(messageEl);

        // Auto scroll to bottom
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    /**
     * Update statistics
     */
    updateStats(response, processingTime) {
        // Update message count
        const count = parseInt(this.messageCount.textContent) + 1;
        this.messageCount.textContent = count;

        // Update response time
        this.responseTime.textContent = `${processingTime}ms`;

        // Update tokens used
        const tokens = parseInt(this.tokensUsed.textContent) + response.tokens_used;
        this.tokensUsed.textContent = tokens;

        // Update last agent
        this.lastAgent.textContent = response.source || 'Unknown';
    }

    /**
     * Clear chat
     */
    async clearChat() {
        if (confirm('Clear all messages?')) {
            try {
                await api.clearConversation();
                this.messagesContainer.innerHTML = '';
                this.chatHistory = [];
                this.messageCount.textContent = '0';
                this.responseTime.textContent = '0ms';
                this.tokensUsed.textContent = '0';
                this.lastAgent.textContent = '—';
                
                if (this.welcomeMessage) {
                    this.welcomeMessage.style.display = 'flex';
                }
            } catch (error) {
                alert('Failed to clear conversation: ' + error.message);
            }
        }
    }

    /**
     * Update agent statistics
     */
    async updateAgentStats() {
        try {
            await agentManager.updateStats();
        } catch (error) {
            console.error('Failed to update agent stats:', error);
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new NeuroAgentApp();
});
