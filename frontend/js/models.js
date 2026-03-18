/**
 * Model Management Module - Updated with Custom Models
 * Handles model selection, information display, and API calls
 */

const MODELS = {
    'openai/gpt-oss-120b': {
        name: 'GPT-OSS 120B',
        provider: 'OpenAI',
        context: '200,000 tokens',
        speed: 'Fast',
        cost: 'Medium',
        description: 'Most powerful open-source model - excellent reasoning & analysis',
        recommendations: 'Complex tasks, Deep analysis, Creative writing, Code generation'
    },
    'llama-3.3-70b-versatile': {
        name: 'Llama 3.3 70B',
        provider: 'Meta',
        context: '8,000 tokens',
        speed: 'Very fast',
        cost: 'Low',
        description: 'Versatile and balanced - great for most use cases',
        recommendations: 'General Q&A, Multi-task, Analysis, Summarization'
    },
    'llama-3.1-8b-instant': {
        name: 'Llama 3.1 8B',
        provider: 'Meta',
        context: '8,000 tokens',
        speed: 'Ultra-fast',
        cost: 'Very low',
        description: 'Lightweight and super fast - perfect for quick responses',
        recommendations: 'Quick answers, Simple tasks, High volume queries'
    }
};

class ModelManager {
    constructor() {
        this.currentModel = 'llama-3.3-70b-versatile'; // Default to balanced model
        this.modelSelector = document.getElementById('model-selector');
        this.modelInfoText = document.getElementById('model-info-text');
        this.modelSpecsDiv = document.getElementById('model-specs');
        this.currentModelDisplay = document.getElementById('current-model-display');
        
        this.setupEventListeners();
        this.updateModelDisplay();
        
        console.log('✅ ModelManager initialized with new models');
    }

    setupEventListeners() {
        if (this.modelSelector) {
            this.modelSelector.addEventListener('change', (e) => {
                this.selectModel(e.target.value);
            });
        }
    }

    selectModel(modelId) {
        if (!MODELS[modelId]) {
            console.error('❌ Unknown model:', modelId);
            return;
        }

        this.currentModel = modelId;
        localStorage.setItem('selectedModel', modelId);
        this.updateModelDisplay();
        
        console.log(`✅ Model selected: ${this.currentModel}`);
        
        // Show notification
        this.showModelNotification(MODELS[modelId].name);
    }

    updateModelDisplay() {
        const model = MODELS[this.currentModel];
        
        if (!model) return;

        // Update model selector
        if (this.modelSelector) {
            this.modelSelector.value = this.currentModel;
        }

        // Update model info in settings
        if (this.modelInfoText) {
            this.modelInfoText.innerHTML = `
                <strong>${model.name}</strong><br>
                Context: ${model.context}<br>
                Speed: ${model.speed}
            `;
        }

        // Update model specs in right sidebar
        if (this.modelSpecsDiv) {
            this.modelSpecsDiv.innerHTML = `
                <p><strong>${model.name}</strong></p>
                <p>Provider: ${model.provider}</p>
                <p>Context: ${model.context}</p>
                <p>Speed: ${model.speed}</p>
                <p>Cost: ${model.cost}</p>
                <p style="margin-top: 10px; font-size: 12px; opacity: 0.8;">
                    ${model.description}
                </p>
                <p style="margin-top: 8px; font-size: 11px; opacity: 0.7;">
                    📌 Best for: ${model.recommendations}
                </p>
            `;
        }

        // Update current model display
        if (this.currentModelDisplay) {
            this.currentModelDisplay.textContent = model.name;
        }
    }

    showModelNotification(modelName) {
        // Create temporary notification
        const notification = document.createElement('div');
        notification.className = 'model-notification';
        notification.textContent = `✅ Switched to ${modelName}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            color: var(--bg-primary);
            padding: 12px 20px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 13px;
            z-index: 9999;
            animation: slideInRight 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideInRight 0.3s ease reverse';
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    }

    getSelectedModel() {
        return this.currentModel;
    }

    getModelName(modelId) {
        return MODELS[modelId]?.name || 'Unknown';
    }

    getModelInfo(modelId) {
        return MODELS[modelId] || null;
    }

    loadSavedModel() {
        const saved = localStorage.getItem('selectedModel');
        if (saved && MODELS[saved]) {
            this.currentModel = saved;
            this.updateModelDisplay();
            console.log(`📂 Loaded saved model: ${saved}`);
        }
    }
}

// Create global model manager instance
const modelManager = new ModelManager();

// Load saved model on page load
document.addEventListener('DOMContentLoaded', () => {
    modelManager.loadSavedModel();
});