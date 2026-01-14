# Adding Self-Learning Capabilities to Your AI Agent 🧠

## 🎯 What is Self-Learning?

Self-learning means your agent can:
- **Remember** past interactions and outcomes
- **Learn** from successful and failed attempts
- **Improve** its performance over time
- **Adapt** its behavior based on feedback
- **Personalize** responses to individual users

## 🔄 Current State vs Self-Learning

### Current Agent (Stateless)
```
Query 1: "Show tables" → Agent figures it out from scratch
Query 2: "Show tables" → Agent figures it out from scratch again
                          (Same work, no learning)
```

### Self-Learning Agent
```
Query 1: "Show tables" → Agent learns successful approach
Query 2: "Show tables" → Agent uses learned approach (faster!)
Query 3: User corrects → Agent updates its knowledge
```

## 🏗️ Self-Learning Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  SELF-LEARNING LAYERS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  1. MEMORY LAYER (Remember)                          │ │
│  │  - Conversation history                              │ │
│  │  - Tool usage patterns                               │ │
│  │  - Successful query templates                        │ │
│  │  - Error patterns and fixes                          │ │
│  └───────────────────────────────────────────────────────┘ │
│                           ↓                                 │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  2. LEARNING LAYER (Learn)                           │ │
│  │  - Pattern recognition                               │ │
│  │  - Success/failure tracking                          │ │
│  │  - User feedback integration                         │ │
│  │  - Query optimization                                │ │
│  └───────────────────────────────────────────────────────┘ │
│                           ↓                                 │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  3. ADAPTATION LAYER (Improve)                       │ │
│  │  - Adjust strategy based on history                  │ │
│  │  - Personalize to user preferences                   │ │
│  │  - Optimize tool selection                           │ │
│  │  - Cache frequent queries                            │ │
│  └───────────────────────────────────────────────────────┘ │
│                           ↓                                 │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  4. FEEDBACK LAYER (Refine)                          │ │
│  │  - User ratings (👍/👎)                               │ │
│  │  - Correction tracking                               │ │
│  │  - Performance metrics                               │ │
│  │  - Continuous improvement                            │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Implementation Strategies

### Strategy 1: Memory & Conversation History ⭐ (Easy)

**Add persistent conversation memory:**

```python
# File: memory_manager.py
from langchain.memory import ConversationBufferMemory
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class MemoryManager:
    def __init__(self):
        # Short-term memory (current session)
        self.conversation_memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Long-term memory (across sessions)
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma(
            collection_name="agent_memory",
            embedding_function=embeddings,
            persist_directory="./memory_db"
        )
        
        self.long_term_memory = VectorStoreRetrieverMemory(
            retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
        )
    
    def save_interaction(self, query: str, response: str, 
                        success: bool, tools_used: list):
        """Save interaction for future learning"""
        memory_entry = {
            "query": query,
            "response": response,
            "success": success,
            "tools": tools_used,
            "timestamp": datetime.now()
        }
        self.long_term_memory.save_context(
            {"input": query},
            {"output": response}
        )
    
    def recall_similar(self, query: str):
        """Retrieve similar past interactions"""
        return self.long_term_memory.load_memory_variables(
            {"prompt": query}
        )
```

**Integration:**

```python
# In agent_service.py
from memory_manager import MemoryManager

class AgentService:
    def __init__(self):
        self.memory = MemoryManager()
        # ... existing code ...
    
    async def run(self, query: str):
        # Check if we've seen similar queries before
        similar = self.memory.recall_similar(query)
        
        # Add context to the agent
        result = await self.agent.run(
            query, 
            context=similar  # Learn from past
        )
        
        # Save this interaction
        self.memory.save_interaction(
            query=query,
            response=result,
            success=True,
            tools_used=self.agent.tools_used
        )
        
        return result
```

---

### Strategy 2: Query Pattern Learning ⭐⭐ (Medium)

**Learn successful query patterns:**

```python
# File: pattern_learner.py
import json
from collections import defaultdict
from datetime import datetime

class PatternLearner:
    def __init__(self, db_path="patterns.json"):
        self.db_path = db_path
        self.patterns = self.load_patterns()
    
    def load_patterns(self):
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "successful_queries": [],
                "tool_sequences": defaultdict(list),
                "error_fixes": {},
                "user_preferences": {}
            }
    
    def save_patterns(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.patterns, f, indent=2)
    
    def record_success(self, query_type: str, tool_sequence: list, 
                       sql_query: str = None):
        """Record a successful interaction"""
        self.patterns["successful_queries"].append({
            "type": query_type,
            "tools": tool_sequence,
            "sql": sql_query,
            "timestamp": str(datetime.now()),
            "count": self.patterns.get(f"count_{query_type}", 0) + 1
        })
        self.save_patterns()
    
    def record_error_fix(self, error: str, fix: str):
        """Learn from errors and their fixes"""
        self.patterns["error_fixes"][error] = fix
        self.save_patterns()
    
    def suggest_approach(self, query_type: str):
        """Suggest best approach based on history"""
        successful = [
            p for p in self.patterns["successful_queries"]
            if p["type"] == query_type
        ]
        
        if successful:
            # Return most common successful approach
            return max(successful, key=lambda x: x.get("count", 0))
        return None
```

**Integration:**

```python
# In agent_service.py
from pattern_learner import PatternLearner

class AgentService:
    def __init__(self):
        self.learner = PatternLearner()
        # ... existing code ...
    
    async def run(self, query: str):
        # Classify query type
        query_type = self.classify_query(query)
        
        # Check if we've learned a good approach
        suggested = self.learner.suggest_approach(query_type)
        
        if suggested:
            # Use learned approach
            result = await self.execute_learned_approach(suggested)
        else:
            # Let agent figure it out
            result = await self.agent.run(query)
        
        # Record success
        self.learner.record_success(
            query_type=query_type,
            tool_sequence=self.agent.tools_used,
            sql_query=self.extract_sql(result)
        )
        
        return result
```

---

### Strategy 3: User Feedback Loop ⭐⭐ (Medium)

**Learn from user ratings and corrections:**

```python
# File: feedback_system.py
class FeedbackSystem:
    def __init__(self):
        self.feedback_db = "feedback.json"
        self.feedback_data = self.load_feedback()
    
    def load_feedback(self):
        try:
            with open(self.feedback_db, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "ratings": [],
                "corrections": [],
                "preferences": {}
            }
    
    def record_rating(self, query_id: str, rating: str, 
                      query: str, response: str):
        """Record user rating (thumbs up/down)"""
        self.feedback_data["ratings"].append({
            "query_id": query_id,
            "rating": rating,  # "up" or "down"
            "query": query,
            "response": response,
            "timestamp": str(datetime.now())
        })
        self.save_feedback()
    
    def record_correction(self, query: str, wrong_response: str, 
                         correct_response: str):
        """Record when user corrects the agent"""
        self.feedback_data["corrections"].append({
            "query": query,
            "wrong": wrong_response,
            "correct": correct_response,
            "timestamp": str(datetime.now())
        })
        self.save_feedback()
    
    def get_improvement_suggestions(self):
        """Analyze feedback for improvement areas"""
        # Find patterns in negative ratings
        negative = [
            r for r in self.feedback_data["ratings"]
            if r["rating"] == "down"
        ]
        
        # Group by query type
        issues = defaultdict(list)
        for neg in negative:
            query_type = self.classify_query(neg["query"])
            issues[query_type].append(neg)
        
        return issues
```

**UI Integration:**

```python
# In ui_client.py
def chat(self, message: str, history: List) -> Tuple[str, List]:
    # ... existing chat code ...
    
    # Add feedback buttons
    query_id = str(uuid.uuid4())
    
    response_with_feedback = f"""
{response_text}

---
Was this helpful?
[Rate this response]
Query ID: {query_id}
"""
    
    history.append({
        "role": "assistant", 
        "content": response_with_feedback
    })
    
    return "", history

def handle_feedback(self, query_id: str, rating: str):
    """Handle user feedback"""
    self.feedback_system.record_rating(
        query_id=query_id,
        rating=rating,
        query=self.last_query,
        response=self.last_response
    )
```

---

### Strategy 4: Reinforcement Learning ⭐⭐⭐ (Advanced)

**Use RL to optimize tool selection:**

```python
# File: rl_optimizer.py
import numpy as np
from collections import defaultdict

class ReinforcementLearner:
    def __init__(self, learning_rate=0.1, discount_factor=0.9):
        self.lr = learning_rate
        self.gamma = discount_factor
        
        # Q-table: state -> action -> expected reward
        self.q_table = defaultdict(lambda: defaultdict(float))
        
        # Track action outcomes
        self.action_history = []
    
    def get_state(self, query: str, context: dict):
        """Convert query + context to state representation"""
        return (
            self.classify_query(query),
            len(context.get("history", [])),
            context.get("connected_servers", ())
        )
    
    def choose_action(self, state, available_tools, epsilon=0.1):
        """Choose best action (tool) based on Q-values"""
        # Exploration vs exploitation
        if np.random.random() < epsilon:
            # Explore: random tool
            return np.random.choice(available_tools)
        else:
            # Exploit: best known tool
            q_values = [
                self.q_table[state][tool] 
                for tool in available_tools
            ]
            best_idx = np.argmax(q_values)
            return available_tools[best_idx]
    
    def update_q_value(self, state, action, reward, next_state):
        """Update Q-value based on outcome"""
        # Q-learning update rule
        current_q = self.q_table[state][action]
        
        max_next_q = max(
            self.q_table[next_state].values(),
            default=0
        )
        
        new_q = current_q + self.lr * (
            reward + self.gamma * max_next_q - current_q
        )
        
        self.q_table[state][action] = new_q
    
    def calculate_reward(self, success: bool, execution_time: float,
                        user_rating: str = None):
        """Calculate reward for this action"""
        reward = 0
        
        if success:
            reward += 10
        else:
            reward -= 5
        
        # Penalize slow responses
        if execution_time > 5:
            reward -= 2
        
        # User feedback
        if user_rating == "up":
            reward += 15
        elif user_rating == "down":
            reward -= 10
        
        return reward
```

**Integration:**

```python
# In agent_service.py
from rl_optimizer import ReinforcementLearner

class AgentService:
    def __init__(self):
        self.rl = ReinforcementLearner()
        # ... existing code ...
    
    async def run(self, query: str, user_rating: str = None):
        state = self.rl.get_state(query, self.context)
        available_tools = self.get_available_tools()
        
        # Agent suggests tool, but RL can override
        suggested_tool = self.rl.choose_action(state, available_tools)
        
        start_time = time.time()
        
        # Execute with suggested tool preference
        result = await self.agent.run(
            query,
            preferred_tool=suggested_tool
        )
        
        execution_time = time.time() - start_time
        
        # Calculate reward
        reward = self.rl.calculate_reward(
            success=result.get("success"),
            execution_time=execution_time,
            user_rating=user_rating
        )
        
        # Update Q-values
        next_state = self.rl.get_state(query, self.new_context)
        self.rl.update_q_value(
            state, suggested_tool, reward, next_state
        )
        
        return result
```

---

### Strategy 5: Fine-Tuning with User Data ⭐⭐⭐ (Advanced)

**Fine-tune the LLM on your specific use cases:**

```python
# File: model_trainer.py
from openai import OpenAI

class ModelTrainer:
    def __init__(self):
        self.client = OpenAI()
        self.training_data = []
    
    def collect_training_data(self, query: str, ideal_response: str,
                              tools_used: list):
        """Collect successful interactions for training"""
        self.training_data.append({
            "messages": [
                {
                    "role": "system",
                    "content": "You are a database and API assistant."
                },
                {
                    "role": "user",
                    "content": query
                },
                {
                    "role": "assistant",
                    "content": ideal_response,
                    "function_call": {
                        "name": tools_used[0],
                        "arguments": "{}"
                    }
                }
            ]
        })
    
    def export_training_file(self, output_path="training_data.jsonl"):
        """Export in OpenAI fine-tuning format"""
        with open(output_path, 'w') as f:
            for example in self.training_data:
                f.write(json.dumps(example) + '\n')
    
    def start_fine_tuning(self, training_file: str):
        """Start fine-tuning job"""
        with open(training_file, 'rb') as f:
            response = self.client.files.create(
                file=f,
                purpose='fine-tune'
            )
        
        fine_tune_job = self.client.fine_tuning.jobs.create(
            training_file=response.id,
            model="gpt-4o-mini"  # Or your preferred model
        )
        
        return fine_tune_job.id
```

---

## 📊 Complete Self-Learning System

Here's how to combine all strategies:

```python
# File: self_learning_agent.py
from memory_manager import MemoryManager
from pattern_learner import PatternLearner
from feedback_system import FeedbackSystem
from rl_optimizer import ReinforcementLearner
from model_trainer import ModelTrainer

class SelfLearningAgent:
    def __init__(self):
        # Initialize all learning components
        self.memory = MemoryManager()
        self.pattern_learner = PatternLearner()
        self.feedback = FeedbackSystem()
        self.rl = ReinforcementLearner()
        self.trainer = ModelTrainer()
        
        # Base agent
        self.agent = MCPAgent(...)
    
    async def process_query(self, query: str, user_id: str = None):
        """Process query with self-learning"""
        
        # 1. RECALL: Check memory
        similar_past = self.memory.recall_similar(query)
        learned_pattern = self.pattern_learner.suggest_approach(
            self.classify_query(query)
        )
        
        # 2. OPTIMIZE: Use RL for tool selection
        state = self.get_state(query)
        optimal_tool = self.rl.choose_action(state, self.get_tools())
        
        # 3. EXECUTE: Run with learned optimizations
        start_time = time.time()
        result = await self.agent.run(
            query,
            context=similar_past,
            preferred_pattern=learned_pattern,
            preferred_tool=optimal_tool
        )
        execution_time = time.time() - start_time
        
        # 4. LEARN: Update all learning systems
        self.memory.save_interaction(
            query, result, success=True, tools=self.agent.tools_used
        )
        
        self.pattern_learner.record_success(
            query_type=self.classify_query(query),
            tool_sequence=self.agent.tools_used
        )
        
        # 5. TRAIN: Collect for fine-tuning
        if result.get("user_rating") == "up":
            self.trainer.collect_training_data(
                query, result["response"], self.agent.tools_used
            )
        
        return result
    
    def incorporate_feedback(self, query_id: str, rating: str,
                            correction: str = None):
        """Learn from user feedback"""
        # Record feedback
        self.feedback.record_rating(query_id, rating, ...)
        
        # Update RL rewards
        reward = 15 if rating == "up" else -10
        self.rl.update_q_value(..., reward=reward)
        
        # If correction provided, learn from it
        if correction:
            self.feedback.record_correction(...)
            self.pattern_learner.record_error_fix(...)
    
    async def periodic_improvement(self):
        """Run periodic improvement tasks"""
        # Analyze feedback
        issues = self.feedback.get_improvement_suggestions()
        
        # Retrain on successful interactions
        if len(self.trainer.training_data) > 100:
            self.trainer.export_training_file()
            # Optionally start fine-tuning
```

---

## 🎯 Implementation Roadmap

### Phase 1: Basic Memory (Week 1)
- ✅ Add conversation history
- ✅ Store successful queries
- ✅ Basic pattern matching

### Phase 2: Feedback Loop (Week 2)
- ✅ Add rating buttons (👍/👎)
- ✅ Collect user corrections
- ✅ Track success metrics

### Phase 3: Pattern Learning (Week 3)
- ✅ Analyze successful patterns
- ✅ Suggest optimized approaches
- ✅ Cache frequent queries

### Phase 4: Advanced Learning (Week 4+)
- ✅ Implement RL for tool selection
- ✅ Fine-tune model on your data
- ✅ Personalization per user

---

## 📈 Measuring Learning Progress

Track these metrics:

```python
class LearningMetrics:
    def track_improvement(self):
        return {
            # Speed improvements
            "avg_response_time": self.calculate_avg_time(),
            "time_improvement": self.compare_to_baseline(),
            
            # Accuracy improvements
            "success_rate": self.calculate_success_rate(),
            "error_reduction": self.compare_errors(),
            
            # User satisfaction
            "positive_ratings": self.count_positive_ratings(),
            "rating_trend": self.analyze_rating_trend(),
            
            # Learning efficiency
            "patterns_learned": len(self.pattern_learner.patterns),
            "memory_size": self.memory.count_entries(),
            "reuse_rate": self.calculate_pattern_reuse()
        }
```

---

## 🚀 Quick Start Implementation

Want to start simple? Here's the minimal code:

```python
# 1. Add to requirements.txt
"""
chromadb>=0.4.0
langchain-community>=0.0.1
"""

# 2. Create simple memory (memory_simple.py)
from langchain.memory import ConversationBufferMemory
import json

class SimpleMemory:
    def __init__(self):
        self.memory = ConversationBufferMemory()
        self.patterns = {}
    
    def remember(self, query, response, success):
        self.memory.save_context(
            {"input": query},
            {"output": response}
        )
        
        if success:
            query_type = query.split()[0]  # First word
            if query_type not in self.patterns:
                self.patterns[query_type] = []
            self.patterns[query_type].append(response)
    
    def recall(self, query):
        return self.memory.load_memory_variables({})

# 3. Use in agent_service.py
from memory_simple import SimpleMemory

class AgentService:
    def __init__(self):
        self.memory = SimpleMemory()
        # ... rest of code
    
    async def run(self, query: str):
        # Check memory
        context = self.memory.recall(query)
        
        # Run agent with context
        result = await self.agent.run(query)
        
        # Save to memory
        self.memory.remember(query, result, success=True)
        
        return result
```

That's it! You now have basic learning! 🎉

---

## 💡 Best Practices

1. **Start Simple**: Begin with conversation memory, add complexity gradually
2. **Track Metrics**: Measure improvement to validate learning
3. **User Feedback**: Make it easy for users to provide feedback
4. **Privacy**: Be careful with sensitive data in memory
5. **Persistence**: Save learned patterns to disk
6. **Versioning**: Track which version of the agent learned what

---

## 🎓 Learning Resources

- LangChain Memory: https://python.langchain.com/docs/modules/memory/
- OpenAI Fine-tuning: https://platform.openai.com/docs/guides/fine-tuning
- RL for LLMs: https://huggingface.co/blog/rlhf
- Vector Databases: https://www.pinecone.io/learn/vector-database/

---

**Your agent will get smarter with every interaction! 🧠✨**
