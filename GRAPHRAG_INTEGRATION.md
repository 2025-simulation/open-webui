# GraphRAG Integration with Open WebUI

This guide shows how to integrate Microsoft GraphRAG with Open WebUI to enable graph-based retrieval-augmented generation.

## Setup Complete! 🎉

Your GraphRAG integration is ready to use. Here's what we've accomplished:

### ✅ What's Working:
- **GraphRAG Repository**: Located at `~/Developments/simulation/graphrag`
- **Virtual Environment**: Properly configured at `~/Developments/simulation/graphrag/.venv`
- **Sample Data**: "A Christmas Carol" by Charles Dickens is already indexed
- **Integration Tool**: `graphrag_tool.py` created for Open WebUI

### 🔧 Available Functions:

1. **`search_graphrag(query, method="local")`**
   - Perform local search on GraphRAG knowledge graph
   - Best for specific, detailed queries

2. **`search_graphrag_global(query)`**
   - Perform global search for broader context
   - Best for thematic and overview queries

3. **`index_graphrag()`**
   - Index new documents into GraphRAG
   - Place documents in `~/Developments/simulation/graphrag/ragtest/input/`

4. **`check_graphrag_status()`**
   - Check GraphRAG installation and data status

### 🚀 How to Use:

#### Option 1: Direct Integration
Copy the `graphrag_tool.py` file to your Open WebUI functions directory and import it as a custom tool.

#### Option 2: Manual Testing
Test GraphRAG directly from terminal:

```bash
# Navigate to GraphRAG directory
cd ~/Developments/simulation/graphrag/ragtest

# Activate virtual environment
source ../.venv/bin/activate

# Run local search
python -m graphrag query --method local --query "your question here"

# Run global search  
python -m graphrag query --method global --query "your question here"
```

### 📊 Example Queries:

The current indexed data (A Christmas Carol) responds well to:

- **Local Search**: "What is Scrooge's character like?"
- **Global Search**: "What are the main themes in the story?"
- **Character Analysis**: "How does Scrooge change throughout the story?"
- **Plot Questions**: "What happens on Christmas Eve?"

### 📁 Adding Your Own Data:

1. Place your documents in: `~/Developments/simulation/graphrag/ragtest/input/`
2. Run indexing: `python -m graphrag index`
3. Wait for processing to complete
4. Query your new data!

### 🔗 Integration Status:
- ✅ GraphRAG backend working
- ✅ Integration tool created
- ✅ Sample data indexed and queryable
- ✅ Ready for Open WebUI integration

Your GraphRAG + Open WebUI combination is ready to provide graph-enhanced AI conversations! 🤖📊
