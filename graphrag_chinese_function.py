"""
title: GraphRAG 本地调用
author: Open WebUI Assistant
version: 1.0.0
description: 通过 Open WebUI 界面调用本地 GraphRAG 进行知识图谱搜索
"""

import os
import subprocess
import asyncio
from typing import Optional, Callable
from pydantic import BaseModel, Field


class Filter:
    pass


class UserValves(BaseModel):
    graphrag_repo_path: str = Field(
        default=os.path.expanduser("~/Developments/simulation/graphrag"),
        description="GraphRAG 仓库路径"
    )
    graphrag_data_path: str = Field(
        default=os.path.expanduser("~/Developments/simulation/graphrag/ragtest"),
        description="GraphRAG 数据目录路径"
    )


class Function:
    def __init__(self):
        # GraphRAG 路径配置
        self.valves = UserValves()
        self.graphrag_repo = self.valves.graphrag_repo_path
        self.graphrag_data = self.valves.graphrag_data_path
        self.venv_activate = os.path.join(self.graphrag_repo, ".venv", "bin", "activate")

    async def graphrag_search(
        self,
        query: str,
        search_type: str = "local",
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], None]] = None,
    ) -> str:
        """
        使用 GraphRAG 搜索知识图谱
        
        :param query: 搜索查询
        :param search_type: 搜索类型 - "local" 或 "global"
        :return: GraphRAG 搜索结果
        """
        
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"🔍 正在使用 GraphRAG {search_type} 搜索...",
                        "done": False,
                    },
                }
            )

        try:
            # 构建命令
            cmd = (
                f"bash -c 'source {self.venv_activate} && "
                f"cd {self.graphrag_data} && "
                f"python -m graphrag query --method {search_type} --query \"{query}\"'"
            )

            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"📊 执行 {search_type} 搜索中...",
                            "done": False,
                        },
                    }
                )

            # 执行 GraphRAG 搜索
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,  # 2分钟超时
                cwd=self.graphrag_data
            )

            if result.returncode == 0:
                # 提取搜索结果
                output_lines = result.stdout.strip().split('\n')
                response_lines = []
                response_started = False
                
                for line in output_lines:
                    if "Search Response:" in line:
                        response_started = True
                        continue
                    if response_started and line.strip():
                        response_lines.append(line)
                
                response = '\n'.join(response_lines).strip()

                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": "✅ GraphRAG 搜索完成",
                                "done": True,
                            },
                        }
                    )

                if response:
                    return f"## GraphRAG {search_type.upper()} 搜索结果\n\n**查询:** {query}\n\n**结果:**\n\n{response}"
                else:
                    return f"未找到相关结果。请尝试调整查询词语。"

            else:
                error_msg = result.stderr.strip() or "未知错误"
                return f"❌ GraphRAG 搜索失败: {error_msg}"

        except subprocess.TimeoutExpired:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "⏰ 搜索超时",
                            "done": True,
                        },
                    }
                )
            return "⏰ 搜索超时，请尝试更简单的查询"

        except Exception as e:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"❌ 错误: {str(e)}",
                            "done": True,
                        },
                    }
                )
            return f"❌ 执行 GraphRAG 搜索时出错: {str(e)}"

    async def graphrag_local_search(
        self,
        query: str,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], None]] = None,
    ) -> str:
        """
        GraphRAG 本地搜索 - 用于具体问题
        
        :param query: 搜索查询
        :return: 本地搜索结果
        """
        return await self.graphrag_search(
            query, search_type="local", __user__=__user__, __event_emitter__=__event_emitter__
        )

    async def graphrag_global_search(
        self,
        query: str,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], None]] = None,
    ) -> str:
        """
        GraphRAG 全局搜索 - 用于主题分析
        
        :param query: 搜索查询
        :return: 全局搜索结果
        """
        return await self.graphrag_search(
            query, search_type="global", __user__=__user__, __event_emitter__=__event_emitter__
        )

    async def graphrag_status(
        self,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], None]] = None,
    ) -> str:
        """
        检查 GraphRAG 状态
        
        :return: 状态信息
        """
        
        status_info = []

        # 检查 GraphRAG 仓库
        if os.path.exists(self.graphrag_repo):
            status_info.append("✅ GraphRAG 仓库已找到")
        else:
            status_info.append("❌ GraphRAG 仓库未找到")

        # 检查虚拟环境
        if os.path.exists(self.venv_activate):
            status_info.append("✅ 虚拟环境已找到")
        else:
            status_info.append("❌ 虚拟环境未找到")

        # 检查数据目录
        if os.path.exists(self.graphrag_data):
            status_info.append("✅ 数据目录已找到")

            # 检查输入文件
            input_dir = os.path.join(self.graphrag_data, "input")
            if os.path.exists(input_dir):
                input_files = [f for f in os.listdir(input_dir) if f.endswith(('.txt', '.md', '.pdf'))]
                status_info.append(f"📁 输入文件: {len(input_files)} 个文档")
                if input_files:
                    status_info.append(f"   - {', '.join(input_files[:3])}{'...' if len(input_files) > 3 else ''}")
            else:
                status_info.append("📁 输入目录未找到")

            # 检查索引数据
            output_dir = os.path.join(self.graphrag_data, "output")
            if os.path.exists(output_dir):
                status_info.append("📊 已有索引数据，可以进行搜索")
            else:
                status_info.append("📊 无索引数据（需要先运行索引）")
        else:
            status_info.append("❌ 数据目录未找到")

        return "## 📊 GraphRAG 状态检查\n\n" + "\n".join(status_info)

    async def graphrag_index(
        self,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], None]] = None,
    ) -> str:
        """
        运行 GraphRAG 索引
        
        :return: 索引结果
        """
        
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "🚀 开始 GraphRAG 索引过程...",
                        "done": False,
                    },
                }
            )

        try:
            cmd = (
                f"bash -c 'source {self.venv_activate} && "
                f"cd {self.graphrag_data} && "
                f"python -m graphrag index'"
            )

            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "📊 正在执行索引（可能需要几分钟）...",
                            "done": False,
                        },
                    }
                )

            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600,  # 10分钟超时
                cwd=self.graphrag_data
            )

            if result.returncode == 0:
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": "✅ GraphRAG 索引完成",
                                "done": True,
                            },
                        }
                    )
                
                return "✅ **GraphRAG 索引成功完成！**\n\n现在可以使用搜索功能了。"
            else:
                error_msg = result.stderr.strip() or "未知错误"
                return f"❌ GraphRAG 索引失败: {error_msg}"

        except subprocess.TimeoutExpired:
            return "⏰ 索引超时（10分钟），请检查数据大小"

        except Exception as e:
            return f"❌ 执行索引时出错: {str(e)}"
