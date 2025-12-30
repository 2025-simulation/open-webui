"""
title: GraphRAG Search
author: Open WebUI
author_url: https://github.com/open-webui/open-webui
funding_url: https://github.com/open-webui/open-webui
version: 0.1.0
license: MIT
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
        description="Path to GraphRAG repository"
    )
    graphrag_data_path: str = Field(
        default=os.path.expanduser("~/Developments/simulation/graphrag/ragtest"),
        description="Path to GraphRAG data directory"
    )


class Tools:
    def __init__(self):
        self.valves = UserValves()

    async def search_graphrag(
        self,
        query: str,
        method: str = "local",
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], None]] = None,
    ) -> str:
        """
        Search the GraphRAG knowledge graph for information.

        :param query: The search query
        :param method: Search method - 'local' for specific context or 'global' for broader themes
        :return: Search results from GraphRAG
        """

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"🔍 Searching GraphRAG knowledge graph...",
                        "done": False,
                    },
                }
            )

        try:
            # Prepare the search command
            graphrag_venv = os.path.join(self.valves.graphrag_repo_path, ".venv", "bin", "activate")
            
            cmd = (
                f"bash -c 'source {graphrag_venv} && "
                f"cd {self.valves.graphrag_data_path} && "
                f"python -m graphrag query --method {method} --query \"{query}\"'"
            )

            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"📊 Executing {method} search...",
                            "done": False,
                        },
                    }
                )

            # Execute GraphRAG search
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,  # 60 second timeout
                cwd=self.valves.graphrag_data_path
            )

            if result.returncode == 0:
                # Extract just the response part (after "Local/Global Search Response:")
                output_lines = result.stdout.strip().split('\n')
                response_started = False
                response_lines = []
                
                for line in output_lines:
                    if "Search Response:" in line:
                        response_started = True
                        continue
                    if response_started:
                        response_lines.append(line)
                
                response = '\n'.join(response_lines).strip()

                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": "✅ GraphRAG search completed",
                                "done": True,
                            },
                        }
                    )

                return response if response else "No results found for your query."

            else:
                error_msg = result.stderr.strip() or "Unknown error occurred"
                
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": f"❌ Search failed: {error_msg}",
                                "done": True,
                            },
                        }
                    )
                
                return f"GraphRAG search failed: {error_msg}"

        except subprocess.TimeoutExpired:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "⏰ Search timed out",
                            "done": True,
                        },
                    }
                )
            return "GraphRAG search timed out after 60 seconds. Try a simpler query."

        except Exception as e:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"❌ Error: {str(e)}",
                            "done": True,
                        },
                    }
                )
            return f"Error executing GraphRAG search: {str(e)}"

    async def search_graphrag_global(
        self,
        query: str,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], None]] = None,
    ) -> str:
        """
        Search GraphRAG using global method for broad thematic analysis.

        :param query: The search query
        :return: Global search results from GraphRAG
        """
        return await self.search_graphrag(
            query, method="global", __user__=__user__, __event_emitter__=__event_emitter__
        )

    async def check_graphrag_status(
        self,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], None]] = None,
    ) -> str:
        """
        Check GraphRAG installation and data status.

        :return: Status information
        """

        status_info = []

        # Check GraphRAG repository
        if os.path.exists(self.valves.graphrag_repo_path):
            status_info.append("✅ GraphRAG repository found")
        else:
            status_info.append("❌ GraphRAG repository not found")

        # Check virtual environment
        venv_path = os.path.join(self.valves.graphrag_repo_path, ".venv", "bin", "activate")
        if os.path.exists(venv_path):
            status_info.append("✅ Virtual environment found")
        else:
            status_info.append("❌ Virtual environment not found")

        # Check data directory
        if os.path.exists(self.valves.graphrag_data_path):
            status_info.append("✅ Data directory found")

            # Check input files
            input_dir = os.path.join(self.valves.graphrag_data_path, "input")
            if os.path.exists(input_dir):
                input_files = os.listdir(input_dir)
                status_info.append(f"📁 Input files: {len(input_files)} documents")
            else:
                status_info.append("📁 No input directory found")

            # Check output/indexed data
            output_dir = os.path.join(self.valves.graphrag_data_path, "output")
            if os.path.exists(output_dir):
                status_info.append("📊 Indexed data available")
            else:
                status_info.append("📊 No indexed data (run indexing first)")
        else:
            status_info.append("❌ Data directory not found")

        return "**GraphRAG Status:**\n\n" + "\n".join(status_info)
