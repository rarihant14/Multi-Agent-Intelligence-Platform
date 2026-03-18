
class APIClient {
    constructor() {
        this.baseURL = '/api';
        this.conversationId = localStorage.getItem('conversationId') || this.generateId();
        localStorage.setItem('conversationId', this.conversationId);
    }

    generateId() {
        return `conv-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Send a query to the server with model selection
     */
    async sendMessage(
        query, 
        chatHistory = [], 
        uploadedFileId = null, 
        temperature = 0.7, 
        maxTokens = 1024,
        model = 'mixtral-8x7b-32768'  // NEW: Model parameter
    ) {
        try {
            const response = await fetch(`${this.baseURL}/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query,
                    conversation_id: this.conversationId,
                    chat_history: chatHistory,
                    uploaded_file_id: uploadedFileId,
                    temperature,
                    max_tokens: maxTokens,
                    model  // NEW: Send selected model to backend
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to send message');
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Upload a PDF file
     */
    async uploadPDF(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${this.baseURL}/upload`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to upload PDF');
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('Upload Error:', error);
            throw error;
        }
    }

    /**
     * Get system health status
     */
    async getHealth() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            if (!response.ok) throw new Error('Health check failed');
            return await response.json();
        } catch (error) {
            console.error('Health Check Error:', error);
            throw error;
        }
    }

    /**
     * Get available models
     */
    async getModels() {
        try {
            const response = await fetch(`${this.baseURL}/models`);
            if (!response.ok) throw new Error('Failed to get models');
            return await response.json();
        } catch (error) {
            console.error('Models Error:', error);
            throw error;
        }
    }

    /**
     * Get system configuration
     */
    async getConfig() {
        try {
            const response = await fetch(`${this.baseURL}/config`);
            if (!response.ok) throw new Error('Failed to get config');
            return await response.json();
        } catch (error) {
            console.error('Config Error:', error);
            throw error;
        }
    }

    /**
     * Get agent status and statistics
     */
    async getAgentStatus() {
        try {
            const response = await fetch(`${this.baseURL}/agents/status`);
            if (!response.ok) throw new Error('Failed to get agent status');
            return await response.json();
        } catch (error) {
            console.error('Agent Status Error:', error);
            throw error;
        }
    }

    /**
     * Clear conversation
     */
    async clearConversation() {
        try {
            const response = await fetch(`${this.baseURL}/conversation/clear`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    conversation_id: this.conversationId
                })
            });

            if (!response.ok) throw new Error('Failed to clear conversation');
            
            this.conversationId = this.generateId();
            localStorage.setItem('conversationId', this.conversationId);
            
            return await response.json();

        } catch (error) {
            console.error('Clear Conversation Error:', error);
            throw error;
        }
    }
}

// Create global API client instance
const api = new APIClient();
