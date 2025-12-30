"""
title: GraphRAG Integration
author: Assistant
author_url: https://github.com/open-webui/open-webui
funding_url: https://github.com/open-webui/open-webui
version: 0.1.0
requirements: graphrag
"""

import os
import sys
import json
import asyncio
import subprocess
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Add GraphRAG to Python path
GRAPHRAG_PATH = os.path.expanduser("~/Developments/simulation/graphrag")
sys.path.append(GRAPHRAG_PATH)

class Filter:
    pass

class UserValves:
    def __init__(self):
        self.graphrag_config_path = os.path.expanduser("~/Developments/simulation/graphrag/ragtest/settings.yaml")
        self.graphrag_data_path = os.path.expanduser("~/Developments/simulation/graphrag/ragtest")
        self.graphrag_venv_path = os.path.expanduser("~/Developments/simulation/graphrag/.venv/bin/activate")
        self.use_local_search = True  # Use local search (True) or global search (False)
        self.search_limit = 10  # Maximum number of search results to return

class Tools:
    def __init__(self):
        self.valves = UserValves()

    async def search_graphrag(
        self,
        query: str,
        __event_emitter__: callable = None,
        __user__: dict = None,
    ) -> str:
        """
        Search the GraphRAG knowledge graph for information related to the query.
        
        :param query: The search query
        :return: Search results from GraphRAG
        """
        
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": f"Searching GraphRAG for: {query}", "done": False},
                }
            )

        try:
            # Change to GraphRAG directory
            os.chdir(self.valves.graphrag_data_path)
            
            # Prepare the search command with virtual environment activation
            search_type = "local" if self.valves.use_local_search else "global"
            
            # Use bash to activate venv and run command
            cmd = f"cd {os.path.dirname(self.valves.graphrag_venv_path)} && " \
                  f"source {self.valves.graphrag_venv_path} && " \
                  f"cd {self.valves.graphrag_data_path} && " \
                  f"python -m graphrag query --method {search_type} --query '{query}'"
            
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status", 
                        "data": {"description": f"Executing {search_type} search...", "done": False},
                    }
                )
            
            # Execute the GraphRAG search
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
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
                
                return f"# GraphRAG Search Results\n\n**Query:** {query}\n\n**Results:**\n{response}"
            else:
                error_msg = result.stderr.strip() or "Unknown error occurred"
                
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {"description": f"GraphRAG search failed: {error_msg}", "done": True},
                        }
                    )
                
                return f"GraphRAG search failed: {error_msg}"
                
        except subprocess.TimeoutExpired:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": "GraphRAG search timed out", "done": True},
                    }
                )
            return "GraphRAG search timed out after 60 seconds"
            
        except Exception as e:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": f"Error: {str(e)}", "done": True},
                    }
                )
            return f"Error executing GraphRAG search: {str(e)}"

    async def index_documents(
        self,
        input_path: str = None,
        __event_emitter__: callable = None,
        __user__: dict = None,
    ) -> str:
        """
        Index documents into GraphRAG knowledge graph.
        
        :param input_path: Path to documents to index (optional, uses default input path if not provided)
        :return: Indexing status
        """
        
        if not input_path:
            input_path = os.path.join(self.valves.graphrag_data_path, "input")
        
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": f"Starting GraphRAG indexing from: {input_path}", "done": False},
                }
            )

        try:
            # Change to GraphRAG directory  
            os.chdir(self.valves.graphrag_data_path)
            
            # Prepare the indexing command with virtual environment activation
            cmd = f"cd {os.path.dirname(self.valves.graphrag_venv_path)} && " \
                  f"source {self.valves.graphrag_venv_path} && " \
                  f"cd {self.valves.graphrag_data_path} && " \
                  f"python -m graphrag index"
            
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": "Executing GraphRAG indexing...", "done": False},
                    }
                )
            
            # Execute the GraphRAG indexing
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for indexing
            )
            
            if result.returncode == 0:
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {"description": "GraphRAG indexing completed successfully", "done": True},
                        }
                    )
                
                return f"# GraphRAG Indexing Completed\n\n**Input Path:** {input_path}\n\n**Status:** Successfully indexed documents into GraphRAG knowledge graph.\n\n**Output:**\n{result.stdout}"
            else:
                error_msg = result.stderr.strip() or "Unknown error occurred"
                
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {"description": f"GraphRAG indexing failed: {error_msg}", "done": True},
                        }
                    )
                
                return f"GraphRAG indexing failed: {error_msg}"
                
        except subprocess.TimeoutExpired:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": "GraphRAG indexing timed out", "done": True},
                    }
                )
            return "GraphRAG indexing timed out after 10 minutes"
            
        except Exception as e:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": f"Error: {str(e)}", "done": True},
                    }
                )
            return f"Error executing GraphRAG indexing: {str(e)}"
