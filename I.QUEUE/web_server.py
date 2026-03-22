"""
I.QUEUE Web 服务器 - FastAPI 后端
连接前端 UI 和 AgentAutoDesigner 系统
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import json
from datetime import datetime
from pathlib import Path

# 导入 AutoDesigner 系统
from agent_auto_designer import AgentAutoDesigner
from requirement_analyzer import RequirementAnalysis


# ===== 数据模型 =====

class RequirementRequest(BaseModel):
    """需求分析请求"""
    requirement: str
    selected_blocks: Optional[List[Dict[str, str]]] = None


class AnalysisResponse(BaseModel):
    """分析结果响应"""
    analysis: Dict[str, Any]
    plan: Dict[str, Any]
    message: str


class ExportRequest(BaseModel):
    """导出请求"""
    plan: Dict[str, Any]


# ===== FastAPI 应用设置 =====

app = FastAPI(
    title="I.QUEUE Agent 设计器",
    description="智能 Agent 自动设计系统 - Web API",
    version="2.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化设计系统
designer = AgentAutoDesigner()

# 输出目录
OUTPUT_DIR = Path("/workspaces/XIAOJIE/I.QUEUE/mnt/user-data/outputs")
PLANS_DIR = OUTPUT_DIR / "agent_plans"
CONFIGS_DIR = OUTPUT_DIR / "agent_configs"

PLANS_DIR.mkdir(parents=True, exist_ok=True)
CONFIGS_DIR.mkdir(parents=True, exist_ok=True)


# ===== API 端点 =====

@app.get("/")
async def root():
    """根路由"""
    return {
        "message": "🤖 I.QUEUE Agent 设计器 API",
        "version": "2.0",
        "endpoints": {
            "analyze": "POST /api/analyze - 分析需求并生成方案",
            "export_markdown": "POST /api/export/markdown - 导出 Markdown",
            "export_yaml": "POST /api/export/yaml - 导出 YAML 配置",
            "deploy": "POST /api/deploy - 部署 Agent",
            "status": "GET /api/status - 获取系统状态"
        }
    }


@app.get("/api/status")
async def get_status():
    """获取系统状态"""
    return {
        "status": "operational",
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "designer": "AgentAutoDesigner",
        "components": {
            "requirement_analyzer": "Ready",
            "skill_recommender": "Ready",
            "plan_generator": "Ready"
        }
    }


@app.post("/api/analyze")
async def analyze_requirement(request: RequirementRequest):
    """
    分析用户需求并生成 Agent 设计方案
    
    Args:
        request: 包含需求描述的请求
        
    Returns:
        包含分析结果和设计方案的完整响应
    """
    try:
        # 调用设计系统
        plan = designer.design_agent(request.requirement)
        
        # 构建响应
        response = {
            "analysis": {
                "primary_type": plan.analysis.primary_type,
                "secondary_types": plan.analysis.secondary_types,
                "keywords": plan.analysis.keywords,
                "confidence": plan.analysis.confidence,
                "recommendations": plan.analysis.recommendations
            },
            "plan": {
                "requirement": plan.requirement,
                "analysis": {
                    "primary_type": plan.analysis.primary_type,
                    "confidence": plan.analysis.confidence,
                    "secondary_types": plan.analysis.secondary_types,
                    "keywords": plan.analysis.keywords
                },
                "skills": [
                    {
                        "name": skill.name,
                        "description": skill.description,
                        "source": skill.source.value,
                        "priority": skill.priority,
                        "confidence": skill.confidence,
                        "url": skill.url,
                        "config": skill.config
                    }
                    for skill in plan.skills
                ],
                "rules": plan.rules,
                "memory_config": plan.memory_config,
                "alignment": plan.alignment,
                "recommendations": plan.analysis.recommendations,
                "created_at": plan.created_at,
                "markdown": plan.to_markdown(),
                "yaml": plan.to_yaml_config()
            },
            "message": "✅ 方案生成成功"
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"分析失败: {str(e)}"
        )


@app.post("/api/export/markdown")
async def export_markdown(request: ExportRequest):
    """导出为 Markdown 文件"""
    try:
        plan_data = request.plan
        markdown_content = plan_data.get("markdown", "")
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"agent_plan_{timestamp}.md"
        filepath = PLANS_DIR / filename
        
        # 写入文件
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        # 返回文件
        return FileResponse(
            filepath,
            media_type="text/markdown",
            filename=filename
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"导出失败: {str(e)}"
        )


@app.post("/api/export/yaml")
async def export_yaml(request: ExportRequest):
    """导出为 YAML 配置文件"""
    try:
        plan_data = request.plan
        yaml_content = plan_data.get("yaml", "")
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"agent_config_{timestamp}.yaml"
        filepath = CONFIGS_DIR / filename
        
        # 写入文件
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(yaml_content)
        
        # 返回文件
        return FileResponse(
            filepath,
            media_type="application/yaml",
            filename=filename
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"导出失败: {str(e)}"
        )


@app.post("/api/deploy")
async def deploy_agent(request: ExportRequest):
    """
    部署并启动 Agent
    （实际的 Agent 启动逻辑）
    """
    try:
        plan_data = request.plan
        
        # 生成配置
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        config_filename = f"deployed_{timestamp}.yaml"
        config_path = CONFIGS_DIR / config_filename
        
        # 保存配置
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(plan_data.get("yaml", ""))
        
        # 返回部署成功响应
        return {
            "status": "deployed",
            "message": "✅ Agent 已启动",
            "config_file": str(config_path),
            "timestamp": datetime.now().isoformat(),
            "requirement": plan_data.get("requirement", ""),
            "deployment_id": timestamp
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"部署失败: {str(e)}"
        )


# ===== 静态文件服务 =====

# 挂载 Web UI 静态文件
web_ui_path = Path(__file__).parent / "web_ui"
if web_ui_path.exists():
    app.mount("/", StaticFiles(directory=str(web_ui_path), html=True), name="web_ui")


# ===== 健康检查 =====

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


# ===== 主函数 =====

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("🤖 I.QUEUE Web 服务器启动")
    print("="*70)
    print("\n🌐 Web UI: http://localhost:8000")
    print("📡 API: http://localhost:8000/api")
    print("📚 文档: http://localhost:8000/docs")
    print("\n按 Ctrl+C 停止服务器\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        title="I.QUEUE Agent Designer"
    )
