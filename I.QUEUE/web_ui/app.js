/* I.QUEUE 智能 Agent 设计器 - 前端逻辑 */

class AgentDesignerApp {
    constructor() {
        this.apiEndpoint = '/api';
        this.currentPlan = null;
        this.setupEventListeners();
    }

    setupEventListeners() {
        // 主要按钮
        document.getElementById('analyze-btn').addEventListener('click', () => this.analyzeRequirement());
        document.getElementById('clear-btn').addEventListener('click', () => this.clearInput());
        document.getElementById('export-md-btn').addEventListener('click', () => this.exportMarkdown());
        document.getElementById('export-yaml-btn').addEventListener('click', () => this.exportYAML());
        document.getElementById('deploy-btn').addEventListener('click', () => this.deployAgent());

        // 回车提交
        document.getElementById('requirement-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                this.analyzeRequirement();
            }
        });
    }

    async analyzeRequirement() {
        const requirement = document.getElementById('requirement-input').value.trim();
        
        if (!requirement) {
            this.showError('请输入需求描述');
            return;
        }

        this.setLoading(true);
        this.setStatus('正在智能分析需求...');

        try {
            // 调用后端 API
            const response = await fetch(`${this.apiEndpoint}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    requirement: requirement,
                    selected_blocks: tetrisVisualizer.getSelectedBlocks()
                })
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            const data = await response.json();
            this.currentPlan = data.plan;

            // 更新分析摘要
            this.displayAnalysisSummary(data.analysis);

            // 显示设计报告
            this.displayReport(data.plan);

            // 启用导出和部署按钮
            this.enableButtons(['export-md-btn', 'export-yaml-btn', 'deploy-btn']);

            this.setStatus('✅ 分析完成！');
            this.showSuccess('智能设计完成，请查看报告');

        } catch (error) {
            console.error('分析失败:', error);
            this.setStatus('❌ 分析失败');
            this.showError(`分析失败: ${error.message}`);
        } finally {
            this.setLoading(false);
        }
    }

    displayAnalysisSummary(analysis) {
        const summary = document.getElementById('analysis-summary');
        
        document.getElementById('type-result').textContent = analysis.primary_type.toUpperCase();
        document.getElementById('confidence-result').textContent = `${(analysis.confidence * 100).toFixed(0)}%`;
        document.getElementById('keywords-result').textContent = analysis.keywords.slice(0, 3).join(', ') || '-';

        summary.style.display = 'flex';
    }

    displayReport(plan) {
        const container = document.getElementById('report-container');
        
        container.innerHTML = `
            <div class="report-content">
                ${this.generateReportHTML(plan)}
            </div>
        `;
    }

    generateReportHTML(plan) {
        let html = '';

        // 需求信息
        html += `
            <div class="report-section">
                <div class="report-section-title">📌 用户需求</div>
                <div class="report-item-content">${plan.requirement}</div>
            </div>
        `;

        // 分析结果
        if (plan.analysis) {
            html += `
                <div class="report-section">
                    <div class="report-section-title">🔍 分析结果</div>
                    <div class="report-item">
                        <div class="report-item-icon">📊</div>
                        <div class="report-item-content">类型: <strong>${plan.analysis.primary_type}</strong> (${(plan.analysis.confidence * 100).toFixed(0)}% 信心)</div>
                    </div>
                </div>
            `;
        }

        // 推荐技能
        if (plan.skills && plan.skills.length > 0) {
            html += '<div class="report-section">';
            html += '<div class="report-section-title">✨ 推荐技能</div>';
            
            const localSkills = plan.skills.filter(s => s.source === 'LOCAL');
            const openSourceSkills = plan.skills.filter(s => s.source !== 'LOCAL');

            localSkills.forEach(skill => {
                html += `
                    <div class="report-item">
                        <div class="report-item-icon">📦</div>
                        <div class="report-item-content">
                            <strong>${skill.name}</strong>
                            <div style="font-size: 0.8rem; color: var(--text-tertiary); margin-top: 0.25rem;">
                                优先级 P${skill.priority} • ${(skill.confidence * 100).toFixed(0)}% 匹配度
                            </div>
                        </div>
                    </div>
                `;
            });

            if (openSourceSkills.length > 0) {
                html += '<div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid var(--border-color);">';
                html += '<div style="font-size: 0.85rem; color: var(--text-tertiary); margin-bottom: 0.5rem;">+' + openSourceSkills.length + ' 个开源推荐</div>';
                openSourceSkills.slice(0, 2).forEach(skill => {
                    html += `
                        <div class="report-item" style="font-size: 0.8rem;">
                            <div class="report-item-icon">🔗</div>
                            <div class="report-item-content">${skill.name}</div>
                        </div>
                    `;
                });
                html += '</div>';
            }

            html += '</div>';
        }

        // 记忆配置
        if (plan.memory_config) {
            html += `
                <div class="report-section">
                    <div class="report-section-title">🧠 记忆配置</div>
                    <div class="report-item">
                        <div class="report-item-icon">📅</div>
                        <div class="report-item-content">保留期: ${plan.memory_config.retention_days || 7} 天</div>
                    </div>
                    <div class="report-item">
                        <div class="report-item-icon">📚</div>
                        <div class="report-item-content">${plan.memory_config.learn_from_feedback ? '智能学习: 启用' : '智能学习: 禁用'}</div>
                    </div>
                </div>
            `;
        }

        // 能力对齐
        if (plan.alignment) {
            html += '<div class="report-section">';
            html += '<div class="report-section-title">🎯 能力对齐</div>';
            
            Object.entries(plan.alignment).forEach(([key, value]) => {
                const barWidth = Math.round(value * 100);
                html += `
                    <div class="report-item">
                        <div class="report-item-content" style="flex: 1;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                                <span>${key}</span>
                                <span style="font-weight: 600;">${Math.round(value * 100)}%</span>
                            </div>
                            <div style="height: 6px; background: var(--bg-primary); border-radius: 3px; overflow: hidden;">
                                <div style="height: 100%; width: ${barWidth}%; background: var(--primary-color);"></div>
                            </div>
                        </div>
                    </div>
                `;
            });

            html += '</div>';
        }

        // 下一步建议
        if (plan.recommendations) {
            html += '<div class="report-section">';
            html += '<div class="report-section-title">💡 建议</div>';
            
            plan.recommendations.forEach(rec => {
                html += `
                    <div class="report-item">
                        <div class="report-item-icon">→</div>
                        <div class="report-item-content">${rec}</div>
                    </div>
                `;
            });

            html += '</div>';
        }

        return html;
    }

    async exportMarkdown() {
        if (!this.currentPlan) {
            this.showError('没有设计方案可导出');
            return;
        }

        try {
            const response = await fetch(`${this.apiEndpoint}/export/markdown`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.currentPlan)
            });

            if (!response.ok) throw new Error('导出失败');

            const blob = await response.blob();
            this.downloadFile(blob, `agent_plan_${Date.now()}.md`);
            this.showSuccess('已下载 Markdown 文件');

        } catch (error) {
            this.showError(`导出失败: ${error.message}`);
        }
    }

    async exportYAML() {
        if (!this.currentPlan) {
            this.showError('没有设计方案可导出');
            return;
        }

        try {
            const response = await fetch(`${this.apiEndpoint}/export/yaml`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.currentPlan)
            });

            if (!response.ok) throw new Error('导出失败');

            const blob = await response.blob();
            this.downloadFile(blob, `agent_config_${Date.now()}.yaml`);
            this.showSuccess('已下载配置 YAML 文件');

        } catch (error) {
            this.showError(`导出失败: ${error.message}`);
        }
    }

    async deployAgent() {
        if (!this.currentPlan) {
            this.showError('没有要部署的 Agent');
            return;
        }

        const confirmed = confirm('确认要启动 Agent 吗？这将立即开始执行。');
        if (!confirmed) return;

        this.setLoading(true);
        this.setStatus('正在启动 Agent...');

        try {
            const response = await fetch(`${this.apiEndpoint}/deploy`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.currentPlan)
            });

            if (!response.ok) throw new Error('部署失败');

            this.setStatus('✅ Agent 已启动！');
            this.showSuccess('Agent 已成功启动，立即开始处理');

        } catch (error) {
            this.setStatus('❌ 部署失败');
            this.showError(`部署失败: ${error.message}`);
        } finally {
            this.setLoading(false);
        }
    }

    clearInput() {
        document.getElementById('requirement-input').value = '';
        document.getElementById('analysis-summary').style.display = 'none';
        tetrisVisualizer.clearCanvas();
        this.disableButtons(['export-md-btn', 'export-yaml-btn', 'deploy-btn']);
        this.setStatus('就绪');
    }

    downloadFile(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.click();
        window.URL.revokeObjectURL(url);
    }

    setLoading(isLoading) {
        const indicator = document.getElementById('loading-indicator');
        indicator.style.display = isLoading ? 'flex' : 'none';
    }

    setStatus(message) {
        const statusText = document.getElementById('status-text');
        if (statusText) {
            statusText.textContent = message;
        }
    }

    enableButtons(buttonIds) {
        buttonIds.forEach(id => {
            const btn = document.getElementById(id);
            if (btn) btn.disabled = false;
        });
    }

    disableButtons(buttonIds) {
        buttonIds.forEach(id => {
            const btn = document.getElementById(id);
            if (btn) btn.disabled = true;
        });
    }

    showSuccess(message) {
        console.log('✅ ' + message);
        // 实际应用可以添加 toast 通知
    }

    showError(message) {
        console.error('❌ ' + message);
        alert(message);
    }
}

// 初始化应用
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new AgentDesignerApp();
});
