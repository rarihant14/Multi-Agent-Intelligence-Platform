/**
 * Agent Manager
 * Tracks agent status and updates UI
 */

class AgentManager {
    constructor() {
        this.agents = {
            knowledge: { name: 'Knowledge', status: 'ready', success: 0, errors: 0 },
            research: { name: 'Research', status: 'ready', success: 0, errors: 0 },
            document: { name: 'Document', status: 'ready', success: 0, errors: 0 },
            summary: { name: 'Summary', status: 'ready', success: 0, errors: 0 }
        };
        this.agentHistory = [];
    }

    /**
     * Update agent from API response
     */
    updateFromResponse(agentId) {
        if (this.agents[agentId]) {
            this.agentHistory.push({
                agent: agentId,
                timestamp: new Date(),
                status: 'executed'
            });
        }
    }

    /**
     * Fetch and update agent statistics
     */
    async updateStats() {
        try {
            const data = await api.getAgentStatus();
            
            if (data && data.agents) {
                data.agents.forEach(agent => {
                    if (this.agents[agent.id]) {
                        this.agents[agent.id].success = agent.success;
                        this.agents[agent.id].errors = agent.errors;
                        this.updateAgentCard(agent.id);
                    }
                });
            }
        } catch (error) {
            console.error('Failed to update agent stats:', error);
        }
    }

    /**
     * Update agent card in UI
     */
    updateAgentCard(agentId) {
        const element = document.getElementById(`${agentId}-stat`);
        if (element) {
            const agent = this.agents[agentId];
            const total = agent.success + agent.errors;
            element.textContent = `${total} queries`;
        }
    }

    /**
     * Get all agents
     */
    getAll() {
        return this.agents;
    }

    /**
     * Get agent by ID
     */
    getAgent(agentId) {
        return this.agents[agentId];
    }
}

// Create global agent manager instance
const agentManager = new AgentManager();
