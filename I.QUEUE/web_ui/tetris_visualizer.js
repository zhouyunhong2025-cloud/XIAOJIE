/* 俄罗斯方块组件可视化 */

class TetrisVisualizer {
    constructor(canvasSelector) {
        this.canvas = document.querySelector(canvasSelector);
        this.blocks = [];
        this.gridSize = 50;
        this.setupDragAndDrop();
    }

    setupDragAndDrop() {
        document.addEventListener('dragstart', (e) => {
            if (e.target.classList.contains('block')) {
                const blockType = e.target.dataset.type;
                const blockLabel = e.target.querySelector('.block-label').textContent;
                const blockIcon = e.target.querySelector('.block-icon').textContent;
                
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('blockType', blockType);
                e.dataTransfer.setData('blockLabel', blockLabel);
                e.dataTransfer.setData('blockIcon', blockIcon);
            }
        });

        this.canvas.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            this.canvas.style.background = 'var(--bg-tertiary)';
        });

        this.canvas.addEventListener('dragleave', (e) => {
            if (e.target === this.canvas) {
                this.canvas.style.background = 'var(--bg-primary)';
            }
        });

        this.canvas.addEventListener('drop', (e) => {
            e.preventDefault();
            this.canvas.style.background = 'var(--bg-primary)';

            const blockType = e.dataTransfer.getData('blockType');
            const blockLabel = e.dataTransfer.getData('blockLabel');
            const blockIcon = e.dataTransfer.getData('blockIcon');

            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            this.addBlock(blockType, blockLabel, blockIcon, x, y);
        });
    }

    addBlock(type, label, icon, x, y) {
        const blockId = `block-${Date.now()}`;
        
        const blockElement = document.createElement('div');
        blockElement.id = blockId;
        blockElement.className = `canvas-block ${type}-block`;
        blockElement.innerHTML = `
            <div class="canvas-block-content">
                <div class="canvas-block-icon">${icon}</div>
                <div class="canvas-block-label">${label}</div>
            </div>
            <button class="canvas-block-remove" onclick="tetrisVisualizer.removeBlock('${blockId}')">✕</button>
        `;
        blockElement.style.position = 'absolute';
        blockElement.style.left = `${Math.max(0, x - 30)}px`;
        blockElement.style.top = `${Math.max(0, y - 30)}px`;

        this.canvas.appendChild(blockElement);
        
        this.blocks.push({
            id: blockId,
            type: type,
            label: label,
            icon: icon,
            x: x,
            y: y
        });

        this.updateBlockCount();
        this.updatePlaceholder();
    }

    removeBlock(blockId) {
        const element = document.getElementById(blockId);
        if (element) {
            element.remove();
        }
        this.blocks = this.blocks.filter(b => b.id !== blockId);
        this.updateBlockCount();
        this.updatePlaceholder();
    }

    updateBlockCount() {
        const countElement = document.getElementById('selected-count');
        if (countElement) {
            countElement.textContent = this.blocks.length;
        }
    }

    updatePlaceholder() {
        const placeholder = this.canvas.querySelector('.canvas-placeholder');
        if (this.blocks.length === 0) {
            if (!placeholder) {
                const p = document.createElement('div');
                p.className = 'canvas-placeholder';
                p.textContent = '拖拽组件到这里';
                this.canvas.appendChild(p);
            }
        } else {
            if (placeholder) {
                placeholder.remove();
            }
        }
    }

    getSelectedBlocks() {
        return this.blocks.map(b => ({
            type: b.type,
            label: b.label,
            icon: b.icon
        }));
    }

    clearCanvas() {
        this.canvas.innerHTML = '<div class="canvas-placeholder">拖拽组件到这里</div>';
        this.blocks = [];
        this.updateBlockCount();
    }
}

// 初始化可视化
let tetrisVisualizer;

document.addEventListener('DOMContentLoaded', () => {
    tetrisVisualizer = new TetrisVisualizer('#canvas');
});
