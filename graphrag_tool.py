"""
title: GraphRAG Integration
author: Open WebUI Assistant  
version: 0.1.0
"""

import os
import subprocess
import asyncio
from typing import Optional, Dict, Any

class Tools:
    def __init__(self):
        # Configuration for GraphRAG paths
        self.graphrag_repo_path = os.path.expanduser("~/Developments/simulation/graphrag")
        self.graphrag_data_path = os.path.expanduser("~/Developments/simulation/graphrag/ragtest")
        self.graphrag_venv_activate = os.path.expanduser("~/Developments/simulation/graphrag/.venv/bin/activate")

    async def search_graphrag(
        self,
        query: str,
        method: str = "local",
        __event_emitter__: Optional[callable] = None,
        __user__: Optional[dict] = None,
    ) -> str:
        """
        Search the GraphRAG knowledge graph for information related to the query.
        
        :param query: The search query
        :param method: Search method - 'local' or 'global' (default: 'local')
        :return: Search results from GraphRAG
        """
        
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": f"Searching GraphRAG using {method} search for: {query}", "done": False},
                }
            )

        try:
            # Prepare the search command with virtual environment activation
            cmd = (
                f"bash -c 'source {self.graphrag_venv_activate} && "
                f"cd {self.graphrag_data_path} && "
                f"python -m graphrag query --method {method} --query \"{query}\"'"
            )
            
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status", 
                        "data": {"description": f"Executing {method} search...", "done": False},
                    }
                )
            
            # Execute the GraphRAG search
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,  # 60 second timeout
                cwd=self.graphrag_data_path
            )
            
            if result.returncode == 0:
                response = result.stdout.strip()
                
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {"description": "GraphRAG search completed successfully", "done": True},
                        }
                    )
                
                return f"# GraphRAG {method.title()} Search Results\n\n**Query:** {query}\n\n**Results:**\n\n{response}"
            else:
                error_msg = result.stderr.strip() or "Unknown error occurred"
                
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {"description": f"GraphRAG search failed: {error_msg}", "done": True},
                        }
                    )
                
                return f"❌ **GraphRAG search failed:**\n\n```\n{error_msg}\n```"
                
        except subprocess.TimeoutExpired:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": "GraphRAG search timed out", "done": True},
                    }
                )
            return "⏰ **GraphRAG search timed out** after 60 seconds"
            
        except Exception as e:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": f"Error: {str(e)}", "done": True},
                    }
                )
            return f"❌ **Error executing GraphRAG search:** {str(e)}"

    async def search_graphrag_global(
        self,
        query: str,
        __event_emitter__: Optional[callable] = None,
        __user__: Optional[dict] = None,
    ) -> str:
        """
        Search GraphRAG using global search method for broader context.
        
        :param query: The search query
        :return: Global search results from GraphRAG
        """
        return await self.search_graphrag(query, method="global", __event_emitter__=__event_emitter__, __user__=__user__)

    async def index_graphrag(
        self,
        __event_emitter__: Optional[callable] = None,
        __user__: Optional[dict] = None,
    ) -> str:
        """
        Index documents into GraphRAG knowledge graph.
        
        :return: Indexing status
        """
        
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": "Starting GraphRAG indexing process...", "done": False},
                }
            )

        try:
            # Prepare the indexing command with virtual environment activation
            cmd = (
                f"bash -c 'source {self.graphrag_venv_activate} && "
                f"cd {self.graphrag_data_path} && "
                f"python -m graphrag index'"
            )
            
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": "Executing GraphRAG indexing (this may take several minutes)...", "done": False},
                    }
                )
            
            # Execute the GraphRAG indexing
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600,  # 10 minute timeout for indexing
                cwd=self.graphrag_data_path
            )
            
            if result.returncode == 0:
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {"description": "GraphRAG indexing completed successfully", "done": True},
                        }
                    )
                
                return f"✅ **GraphRAG Indexing Completed Successfully**\n\n**Output:**\n```\n{result.stdout[-1000:]}\n```"  # Last 1000 chars
            else:
                error_msg = result.stderr.strip() or "Unknown error occurred"
                
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {"description": f"GraphRAG indexing failed: {error_msg}", "done": True},
                        }
                    )
                
                return f"❌ **GraphRAG indexing failed:**\n\n```\n{error_msg}\n```"
                
        except subprocess.TimeoutExpired:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": "GraphRAG indexing timed out", "done": True},
                    }
                )
            return "⏰ **GraphRAG indexing timed out** after 10 minutes"
            
        except Exception as e:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": f"Error: {str(e)}", "done": True},
                    }
                )
            return f"❌ **Error executing GraphRAG indexing:** {str(e)}"

    async def check_graphrag_status(
        self,
        __event_emitter__: Optional[callable] = None,
        __user__: Optional[dict] = None,
    ) -> str:
        """
        Check GraphRAG installation and data status.
        
        :return: Status information
        """
        
        status_info = []
        
        # Check if GraphRAG repo exists
        if os.path.exists(self.graphrag_repo_path):
            status_info.append("✅ GraphRAG repository found")
        else:
            status_info.append("❌ GraphRAG repository not found")
            
        # Check if virtual environment exists
        if os.path.exists(self.graphrag_venv_activate):
            status_info.append("✅ GraphRAG virtual environment found")
        else:
            status_info.append("❌ GraphRAG virtual environment not found")
            
        # Check if data directory exists
        if os.path.exists(self.graphrag_data_path):
            status_info.append("✅ GraphRAG data directory found")
            
            # Check for input data
            input_dir = os.path.join(self.graphrag_data_path, "input")
            if os.path.exists(input_dir):
                input_files = os.listdir(input_dir)
                status_info.append(f"📁 Input directory contains {len(input_files)} files")
            else:
                status_info.append("📁 Input directory not found")
                
            # Check for output data
            output_dir = os.path.join(self.graphrag_data_path, "output")
            if os.path.exists(output_dir):
                status_info.append("📊 Output directory exists (indexed data available)")
            else:
                status_info.append("📊 Output directory not found (no indexed data)")
        else:
            status_info.append("❌ GraphRAG data directory not found")
            
        return "# GraphRAG Status\n\n" + "\n".join(status_info)
