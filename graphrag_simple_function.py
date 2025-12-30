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


class Filter:
    pass


class Function:
    def __init__(self):
        # GraphRAG 路径配置
        self.graphrag_repo = os.path.expanduser("~/Developments/simulation/graphrag")
        self.graphrag_data = os.path.expanduser("~/Developments/simulation/graphrag/ragtest")
        self.venv_activate = os.path.join(self.graphrag_repo, ".venv", "bin", "activate")

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
        
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "🔍 正在使用 GraphRAG 本地搜索...",
                        "done": False,
                    },
                }
            )

        try:
            # 构建命令
            cmd = (
                f"bash -c 'source {self.venv_activate} && "
                f"cd {self.graphrag_data} && "
                f"python -m graphrag query --method local --query \"{query}\"'"
            )

            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "📊 执行本地搜索中...",
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
                    return f"## GraphRAG 本地搜索结果\n\n**查询:** {query}\n\n**结果:**\n\n{response}"
                else:
                    return f"未找到相关结果。请尝试调整查询词语。"

            else:
                error_msg = result.stderr.strip() or "未知错误"
                return f"❌ GraphRAG 搜索失败: {error_msg}"

        except subprocess.TimeoutExpired:
            return "⏰ 搜索超时，请尝试更简单的查询"

        except Exception as e:
            return f"❌ 执行 GraphRAG 搜索时出错: {str(e)}"

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
        
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "🔍 正在使用 GraphRAG 全局搜索...",
                        "done": False,
                    },
                }
            )

        try:
            # 构建命令
            cmd = (
                f"bash -c 'source {self.venv_activate} && "
                f"cd {self.graphrag_data} && "
                f"python -m graphrag query --method global --query \"{query}\"'"
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

                if response:
                    return f"## GraphRAG 全局搜索结果\n\n**查询:** {query}\n\n**结果:**\n\n{response}"
                else:
                    return f"未找到相关结果。请尝试调整查询词语。"

            else:
                error_msg = result.stderr.strip() or "未知错误"
                return f"❌ GraphRAG 搜索失败: {error_msg}"

        except Exception as e:
            return f"❌ 执行 GraphRAG 搜索时出错: {str(e)}"
